"""
Team Management API Routes - Team and organizational structure management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging

from utils.auth import get_current_user, require_permission, require_role
from database.connection import get_db
from database.schema import User, TeamAnalytics

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/teams", tags=["teams"])


# Pydantic models
class TeamCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: str
    department: str
    members: List[str] = []

class TeamUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[str] = None
    department: Optional[str] = None

class TeamMemberRequest(BaseModel):
    user_id: str
    role: str = "member"  # member, lead, observer

class TeamResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.get("/", response_model=TeamResponse)
async def get_teams(
    department: Optional[str] = Query(None, description="Filter by department"),
    manager_id: Optional[str] = Query(None, description="Filter by manager"),
    limit: int = Query(20, ge=1, le=100, description="Number of teams to return"),
    offset: int = Query(0, ge=0, description="Number of teams to skip"),
    current_user: User = Depends(require_permission("manage_teams")),
    db: Session = Depends(get_db)
):
    """
    Get teams with filtering and pagination
    """
    try:
        # In a real implementation, you would have a Team model
        # For now, we'll simulate team data based on user relationships
        
        # Get users grouped by department and manager
        query = db.query(User).filter(User.is_active == True)
        
        if department:
            query = query.filter(User.department == department)
        
        if manager_id:
            query = query.filter(User.manager_id == manager_id)
        
        users = query.all()
        
        # Group users into teams
        teams = {}
        for user in users:
            team_key = f"{user.department}_{user.manager_id}"
            if team_key not in teams:
                teams[team_key] = {
                    "id": team_key,
                    "name": f"{user.department} Team",
                    "description": f"Team for {user.department} department",
                    "manager_id": user.manager_id,
                    "department": user.department,
                    "members": []
                }
            teams[team_key]["members"].append({
                "id": user.id,
                "name": f"{user.first_name} {user.last_name}",
                "role": user.role,
                "email": user.email
            })
        
        team_list = list(teams.values())
        total_count = len(team_list)
        
        # Apply pagination
        paginated_teams = team_list[offset:offset + limit]
        
        return TeamResponse(
            success=True,
            message="Teams retrieved successfully",
            data={
                "teams": paginated_teams,
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get teams: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve teams"
        )


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific team by ID
    """
    try:
        # Parse team_id (format: department_manager_id)
        if '_' not in team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid team ID format"
            )
        
        department, manager_id = team_id.split('_', 1)
        
        # Get team members
        team_members = db.query(User).filter(
            User.department == department,
            User.manager_id == manager_id,
            User.is_active == True
        ).all()
        
        if not team_members:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Get manager info
        manager = db.query(User).filter(User.id == manager_id).first()
        
        team_data = {
            "id": team_id,
            "name": f"{department} Team",
            "description": f"Team for {department} department",
            "manager": {
                "id": manager.id if manager else None,
                "name": f"{manager.first_name} {manager.last_name}" if manager else "Unknown",
                "email": manager.email if manager else None
            },
            "department": department,
            "members": [
                {
                    "id": member.id,
                    "name": f"{member.first_name} {member.last_name}",
                    "role": member.role,
                    "email": member.email,
                    "position": member.position
                }
                for member in team_members
            ],
            "member_count": len(team_members)
        }
        
        return TeamResponse(
            success=True,
            message="Team retrieved successfully",
            data={"team": team_data}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get team {team_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team"
        )


@router.post("/", response_model=TeamResponse)
async def create_team(
    request: TeamCreateRequest,
    current_user: User = Depends(require_permission("manage_teams")),
    db: Session = Depends(get_db)
):
    """
    Create a new team
    """
    try:
        # Validate manager exists
        manager = db.query(User).filter(User.id == request.manager_id).first()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager not found"
            )
        
        # Validate all members exist
        if request.members:
            members = db.query(User).filter(User.id.in_(request.members)).all()
            if len(members) != len(request.members):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more team members not found"
                )
            
            # Update members' manager and department
            for member in members:
                member.manager_id = request.manager_id
                member.department = request.department
        
        db.commit()
        
        team_id = f"{request.department}_{request.manager_id}"
        
        return TeamResponse(
            success=True,
            message="Team created successfully",
            data={"team_id": team_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create team: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create team"
        )


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: str,
    request: TeamUpdateRequest,
    current_user: User = Depends(require_permission("manage_teams")),
    db: Session = Depends(get_db)
):
    """
    Update an existing team
    """
    try:
        # Parse team_id
        if '_' not in team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid team ID format"
            )
        
        department, manager_id = team_id.split('_', 1)
        
        # Get team members
        team_members = db.query(User).filter(
            User.department == department,
            User.manager_id == manager_id,
            User.is_active == True
        ).all()
        
        if not team_members:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Update team members
        for member in team_members:
            if request.department:
                member.department = request.department
            if request.manager_id:
                member.manager_id = request.manager_id
        
        db.commit()
        
        return TeamResponse(
            success=True,
            message="Team updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update team {team_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update team"
        )


@router.post("/{team_id}/members", response_model=TeamResponse)
async def add_team_member(
    team_id: str,
    request: TeamMemberRequest,
    current_user: User = Depends(require_permission("manage_teams")),
    db: Session = Depends(get_db)
):
    """
    Add a member to a team
    """
    try:
        # Parse team_id
        if '_' not in team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid team ID format"
            )
        
        department, manager_id = team_id.split('_', 1)
        
        # Validate user exists
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        
        # Update user's team assignment
        user.department = department
        user.manager_id = manager_id
        
        db.commit()
        
        return TeamResponse(
            success=True,
            message="Team member added successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add team member: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add team member"
        )


@router.delete("/{team_id}/members/{user_id}", response_model=TeamResponse)
async def remove_team_member(
    team_id: str,
    user_id: str,
    current_user: User = Depends(require_permission("manage_teams")),
    db: Session = Depends(get_db)
):
    """
    Remove a member from a team
    """
    try:
        # Parse team_id
        if '_' not in team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid team ID format"
            )
        
        department, manager_id = team_id.split('_', 1)
        
        # Validate user exists and is in the team
        user = db.query(User).filter(
            User.id == user_id,
            User.department == department,
            User.manager_id == manager_id
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in team"
            )
        
        # Remove user from team (set to null values)
        user.department = None
        user.manager_id = None
        
        db.commit()
        
        return TeamResponse(
            success=True,
            message="Team member removed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove team member: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove team member"
        )


@router.get("/{team_id}/analytics", response_model=TeamResponse)
async def get_team_analytics(
    team_id: str,
    timeframe: str = Query("30d", description="Timeframe for analytics (7d, 30d, 90d)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get team analytics and wellness insights
    """
    try:
        # Parse team_id
        if '_' not in team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid team ID format"
            )
        
        department, manager_id = team_id.split('_', 1)
        
        # Get team members
        team_members = db.query(User).filter(
            User.department == department,
            User.manager_id == manager_id,
            User.is_active == True
        ).all()
        
        if not team_members:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Get wellness data for team members
        member_ids = [member.id for member in team_members]
        
        # In a real implementation, you would query wellness data
        # For now, return mock analytics
        analytics_data = {
            "team_id": team_id,
            "timeframe": timeframe,
            "member_count": len(team_members),
            "wellness_metrics": {
                "average_mood": 7.2,
                "stress_level": "moderate",
                "engagement_score": 8.1,
                "burnout_risk": "low"
            },
            "trends": {
                "mood_trend": "improving",
                "stress_trend": "stable",
                "engagement_trend": "improving"
            },
            "recommendations": [
                "Consider team building activities",
                "Monitor workload distribution",
                "Encourage work-life balance"
            ]
        }
        
        return TeamResponse(
            success=True,
            message="Team analytics retrieved successfully",
            data={"analytics": analytics_data}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get team analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team analytics"
        )


@router.get("/departments", response_model=TeamResponse)
async def get_departments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all departments
    """
    try:
        departments = db.query(User.department).distinct().filter(
            User.department.isnot(None),
            User.is_active == True
        ).all()
        
        return TeamResponse(
            success=True,
            message="Departments retrieved successfully",
            data={"departments": [dept[0] for dept in departments]}
        )
        
    except Exception as e:
        logger.error(f"Failed to get departments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve departments"
        )


@router.get("/stats", response_model=TeamResponse)
async def get_team_stats(
    current_user: User = Depends(require_permission("manage_teams")),
    db: Session = Depends(get_db)
):
    """
    Get team statistics
    """
    try:
        # Get basic stats
        total_users = db.query(User).filter(User.is_active == True).count()
        
        # Department distribution
        dept_stats = {}
        departments = db.query(User.department, db.func.count(User.id)).filter(
            User.department.isnot(None),
            User.is_active == True
        ).group_by(User.department).all()
        
        for dept, count in departments:
            dept_stats[dept] = count
        
        # Manager distribution
        manager_stats = {}
        managers = db.query(User.manager_id, db.func.count(User.id)).filter(
            User.manager_id.isnot(None),
            User.is_active == True
        ).group_by(User.manager_id).all()
        
        for manager_id, count in managers:
            manager_stats[manager_id] = count
        
        stats = {
            "total_users": total_users,
            "department_distribution": dept_stats,
            "manager_distribution": manager_stats,
            "total_teams": len(dept_stats)
        }
        
        return TeamResponse(
            success=True,
            message="Team statistics retrieved successfully",
            data={"statistics": stats}
        )
        
    except Exception as e:
        logger.error(f"Failed to get team stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team statistics"
        )
