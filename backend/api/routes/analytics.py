"""
Analytics API Routes - Organizational health and team analytics
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from utils.auth import get_current_user, require_permission, require_role
from database.connection import get_db
from database.schema import User, WellnessEntry, TeamAnalytics, RiskAssessment
from utils.analytics import WellnessAnalytics

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# Initialize analytics engine
analytics_engine = WellnessAnalytics()


# Pydantic models
class AnalyticsRequest(BaseModel):
    timeframe: str = "30d"  # 7d, 30d, 90d
    filters: Optional[dict] = None

class TeamAnalyticsRequest(BaseModel):
    team_id: str
    period_start: str
    period_end: str

class AnalyticsResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.get("/organizational-health", response_model=AnalyticsResponse)
async def get_organizational_health(
    timeframe: str = Query("30d", description="Timeframe for analysis"),
    current_user: User = Depends(require_permission("read_analytics")),
    db: Session = Depends(get_db)
):
    """
    Get organizational health analytics
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        if timeframe == "7d":
            start_date = end_date - timedelta(days=7)
        elif timeframe == "30d":
            start_date = end_date - timedelta(days=30)
        elif timeframe == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get all wellness entries in the timeframe
        entries = db.query(WellnessEntry).filter(
            WellnessEntry.created_at >= start_date,
            WellnessEntry.created_at <= end_date
        ).all()
        
        # Convert to dict format for analytics engine
        entries_data = [entry.to_dict() for entry in entries]
        
        # Generate organizational analytics
        org_analytics = analytics_engine.generate_user_analytics(entries_data, timeframe)
        
        # Calculate additional organizational metrics
        total_users = db.query(User).filter(User.is_active == True).count()
        active_users = db.query(WellnessEntry.user_id).distinct().filter(
            WellnessEntry.created_at >= start_date
        ).count()
        
        # Department breakdown
        department_stats = {}
        for entry in entries:
            user = db.query(User).filter(User.id == entry.user_id).first()
            if user and user.department:
                if user.department not in department_stats:
                    department_stats[user.department] = {
                        "entries": [],
                        "user_count": 0,
                        "users": set()
                    }
                department_stats[user.department]["entries"].append(entry.to_dict())
                department_stats[user.department]["users"].add(user.id)
        
        # Calculate department averages
        for dept, stats in department_stats.items():
            stats["user_count"] = len(stats["users"])
            if stats["entries"]:
                dept_analytics = analytics_engine.generate_user_analytics(stats["entries"], timeframe)
                stats["analytics"] = dept_analytics
                stats["average_score"] = dept_analytics["summary"]["overall_average"]
            else:
                stats["analytics"] = None
                stats["average_score"] = 0
            stats["users"] = list(stats["users"])  # Convert set to list for JSON serialization
        
        return AnalyticsResponse(
            success=True,
            message="Organizational health analytics retrieved successfully",
            data={
                "timeframe": timeframe,
                "total_users": total_users,
                "active_users": active_users,
                "participation_rate": round((active_users / total_users * 100), 2) if total_users > 0 else 0,
                "overall_analytics": org_analytics,
                "department_breakdown": department_stats,
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get organizational health analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve organizational health analytics"
        )


@router.get("/team/{team_id}", response_model=AnalyticsResponse)
async def get_team_analytics(
    team_id: str,
    timeframe: str = Query("30d", description="Timeframe for analysis"),
    current_user: User = Depends(require_permission("read_team_analytics")),
    db: Session = Depends(get_db)
):
    """
    Get team-specific analytics
    """
    try:
        # Get team members (users with the same manager or in the same department)
        team_members = db.query(User).filter(
            (User.manager_id == team_id) | (User.department == team_id),
            User.is_active == True
        ).all()
        
        if not team_members:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found or no members"
            )
        
        # Calculate date range
        end_date = datetime.utcnow()
        if timeframe == "7d":
            start_date = end_date - timedelta(days=7)
        elif timeframe == "30d":
            start_date = end_date - timedelta(days=30)
        elif timeframe == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get team wellness entries
        team_user_ids = [member.id for member in team_members]
        team_entries = db.query(WellnessEntry).filter(
            WellnessEntry.user_id.in_(team_user_ids),
            WellnessEntry.created_at >= start_date,
            WellnessEntry.created_at <= end_date
        ).all()
        
        # Convert to dict format
        entries_data = [entry.to_dict() for entry in team_entries]
        
        # Generate team analytics
        team_analytics = analytics_engine.generate_user_analytics(entries_data, timeframe)
        
        # Individual member analytics
        member_analytics = {}
        for member in team_members:
            member_entries = [entry.to_dict() for entry in team_entries if entry.user_id == member.id]
            if member_entries:
                member_analytics[member.id] = {
                    "user": {
                        "id": member.id,
                        "name": f"{member.first_name} {member.last_name}",
                        "email": member.email,
                        "role": member.role
                    },
                    "analytics": analytics_engine.generate_user_analytics(member_entries, timeframe)
                }
        
        return AnalyticsResponse(
            success=True,
            message="Team analytics retrieved successfully",
            data={
                "team_id": team_id,
                "timeframe": timeframe,
                "team_size": len(team_members),
                "active_members": len([m for m in team_members if m.id in [e.user_id for e in team_entries]]),
                "overall_analytics": team_analytics,
                "member_analytics": member_analytics,
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get team analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team analytics"
        )


@router.get("/risk-assessment", response_model=AnalyticsResponse)
async def get_risk_assessment(
    timeframe: str = Query("30d", description="Timeframe for analysis"),
    current_user: User = Depends(require_permission("read_analytics")),
    db: Session = Depends(get_db)
):
    """
    Get organizational risk assessment
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        if timeframe == "7d":
            start_date = end_date - timedelta(days=7)
        elif timeframe == "30d":
            start_date = end_date - timedelta(days=30)
        elif timeframe == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get all wellness entries in the timeframe
        entries = db.query(WellnessEntry).filter(
            WellnessEntry.created_at >= start_date,
            WellnessEntry.created_at <= end_date
        ).all()
        
        # Convert to dict format
        entries_data = [entry.to_dict() for entry in entries]
        
        # Generate risk assessment
        risk_analytics = analytics_engine.generate_user_analytics(entries_data, timeframe)
        
        # Get existing risk assessments
        risk_assessments = db.query(RiskAssessment).filter(
            RiskAssessment.created_at >= start_date
        ).all()
        
        # Calculate risk distribution
        risk_distribution = {"low": 0, "medium": 0, "high": 0}
        for assessment in risk_assessments:
            risk_distribution[assessment.risk_level] += 1
        
        # Identify high-risk users
        high_risk_users = []
        for assessment in risk_assessments:
            if assessment.risk_level == "high":
                user = db.query(User).filter(User.id == assessment.user_id).first()
                if user:
                    high_risk_users.append({
                        "user_id": user.id,
                        "name": f"{user.first_name} {user.last_name}",
                        "department": user.department,
                        "risk_score": assessment.risk_score,
                        "risk_factors": assessment.risk_factors,
                        "assessed_at": assessment.created_at.isoformat()
                    })
        
        return AnalyticsResponse(
            success=True,
            message="Risk assessment retrieved successfully",
            data={
                "timeframe": timeframe,
                "overall_risk_analytics": risk_analytics["risk_assessment"],
                "risk_distribution": risk_distribution,
                "high_risk_users": high_risk_users,
                "total_assessments": len(risk_assessments),
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get risk assessment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve risk assessment"
        )


@router.get("/trends", response_model=AnalyticsResponse)
async def get_wellness_trends(
    timeframe: str = Query("30d", description="Timeframe for analysis"),
    metric: str = Query("mood", description="Metric to analyze"),
    current_user: User = Depends(require_permission("read_analytics")),
    db: Session = Depends(get_db)
):
    """
    Get wellness trends over time
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        if timeframe == "7d":
            start_date = end_date - timedelta(days=7)
        elif timeframe == "30d":
            start_date = end_date - timedelta(days=30)
        elif timeframe == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get entries for the specific metric
        entries = db.query(WellnessEntry).filter(
            WellnessEntry.entry_type == metric,
            WellnessEntry.created_at >= start_date,
            WellnessEntry.created_at <= end_date
        ).order_by(WellnessEntry.created_at).all()
        
        # Group by date and calculate daily averages
        daily_data = {}
        for entry in entries:
            date_key = entry.created_at.date().isoformat()
            if date_key not in daily_data:
                daily_data[date_key] = {"values": [], "count": 0}
            daily_data[date_key]["values"].append(entry.value)
            daily_data[date_key]["count"] += 1
        
        # Calculate daily averages
        trend_data = []
        for date, data in sorted(daily_data.items()):
            avg_value = sum(data["values"]) / len(data["values"])
            trend_data.append({
                "date": date,
                "average": round(avg_value, 2),
                "count": data["count"]
            })
        
        # Calculate overall trend
        if len(trend_data) >= 2:
            first_avg = trend_data[0]["average"]
            last_avg = trend_data[-1]["average"]
            trend_direction = "increasing" if last_avg > first_avg else "decreasing" if last_avg < first_avg else "stable"
            trend_magnitude = abs(last_avg - first_avg)
        else:
            trend_direction = "stable"
            trend_magnitude = 0
        
        return AnalyticsResponse(
            success=True,
            message="Wellness trends retrieved successfully",
            data={
                "metric": metric,
                "timeframe": timeframe,
                "trend_data": trend_data,
                "trend_direction": trend_direction,
                "trend_magnitude": round(trend_magnitude, 2),
                "total_entries": len(entries),
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get wellness trends: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve wellness trends"
        )


@router.get("/comparison", response_model=AnalyticsResponse)
async def compare_analytics(
    group1: str = Query(..., description="First group (department or team)"),
    group2: str = Query(..., description="Second group (department or team)"),
    timeframe: str = Query("30d", description="Timeframe for analysis"),
    current_user: User = Depends(require_permission("read_analytics")),
    db: Session = Depends(get_db)
):
    """
    Compare analytics between two groups
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        if timeframe == "7d":
            start_date = end_date - timedelta(days=7)
        elif timeframe == "30d":
            start_date = end_date - timedelta(days=30)
        elif timeframe == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get users for each group
        group1_users = db.query(User).filter(
            (User.department == group1) | (User.manager_id == group1),
            User.is_active == True
        ).all()
        
        group2_users = db.query(User).filter(
            (User.department == group2) | (User.manager_id == group2),
            User.is_active == True
        ).all()
        
        # Get entries for each group
        group1_user_ids = [user.id for user in group1_users]
        group2_user_ids = [user.id for user in group2_users]
        
        group1_entries = db.query(WellnessEntry).filter(
            WellnessEntry.user_id.in_(group1_user_ids),
            WellnessEntry.created_at >= start_date,
            WellnessEntry.created_at <= end_date
        ).all()
        
        group2_entries = db.query(WellnessEntry).filter(
            WellnessEntry.user_id.in_(group2_user_ids),
            WellnessEntry.created_at >= start_date,
            WellnessEntry.created_at <= end_date
        ).all()
        
        # Generate analytics for each group
        group1_analytics = analytics_engine.generate_user_analytics(
            [entry.to_dict() for entry in group1_entries], timeframe
        )
        
        group2_analytics = analytics_engine.generate_user_analytics(
            [entry.to_dict() for entry in group2_entries], timeframe
        )
        
        # Calculate comparison metrics
        comparison = {
            "participation_rate": {
                "group1": round((len(set(e.user_id for e in group1_entries)) / len(group1_users)) * 100, 2) if group1_users else 0,
                "group2": round((len(set(e.user_id for e in group2_entries)) / len(group2_users)) * 100, 2) if group2_users else 0
            },
            "average_score": {
                "group1": group1_analytics["summary"]["overall_average"],
                "group2": group2_analytics["summary"]["overall_average"]
            },
            "consistency_score": {
                "group1": group1_analytics["summary"]["consistency_score"],
                "group2": group2_analytics["summary"]["consistency_score"]
            }
        }
        
        return AnalyticsResponse(
            success=True,
            message="Analytics comparison retrieved successfully",
            data={
                "group1": {
                    "name": group1,
                    "user_count": len(group1_users),
                    "entry_count": len(group1_entries),
                    "analytics": group1_analytics
                },
                "group2": {
                    "name": group2,
                    "user_count": len(group2_users),
                    "entry_count": len(group2_entries),
                    "analytics": group2_analytics
                },
                "comparison": comparison,
                "timeframe": timeframe,
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to compare analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compare analytics"
        )


@router.get("/export", response_model=AnalyticsResponse)
async def export_analytics(
    report_type: str = Query(..., description="Type of report to export"),
    timeframe: str = Query("30d", description="Timeframe for analysis"),
    format: str = Query("json", description="Export format (json, csv)"),
    current_user: User = Depends(require_permission("read_analytics")),
    db: Session = Depends(get_db)
):
    """
    Export analytics data
    """
    try:
        # This would typically generate and return a file
        # For now, we'll return the data structure
        return AnalyticsResponse(
            success=True,
            message="Analytics export generated successfully",
            data={
                "report_type": report_type,
                "timeframe": timeframe,
                "format": format,
                "export_url": f"/exports/{report_type}_{timeframe}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{format}",
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to export analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export analytics"
        )
