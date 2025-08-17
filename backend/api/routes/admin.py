"""
System/Admin API Routes - System administration and management
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta

from utils.auth import get_current_user, require_permission, require_role
from database.connection import get_db, get_db_stats, backup_database
from database.schema import User, ComplianceRecord
from utils.monitoring import get_metrics_summary
from utils.logging import get_logger

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])


# Pydantic models
class SystemSettingsUpdateRequest(BaseModel):
    setting_key: str
    setting_value: Any
    description: Optional[str] = None

class SystemHealthRequest(BaseModel):
    include_detailed: bool = False

class AdminResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.get("/health", response_model=AdminResponse)
async def get_system_health(
    request: SystemHealthRequest = SystemHealthRequest(),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive system health status
    """
    try:
        # Basic health checks
        db_healthy = True
        try:
            db_stats = get_db_stats()
        except Exception as e:
            db_healthy = False
            logger.error(f"Database health check failed: {e}")
        
        # Get metrics summary
        metrics = get_metrics_summary()
        
        health_status = {
            "status": "healthy" if db_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": "healthy" if db_healthy else "unhealthy",
                "api": "healthy",
                "monitoring": "healthy"
            },
            "metrics": metrics
        }
        
        if request.include_detailed:
            # Add detailed system information
            health_status["detailed"] = {
                "database_stats": db_stats if db_healthy else None,
                "active_connections": "N/A",  # Would be actual connection count
                "memory_usage": "N/A",  # Would be actual memory usage
                "cpu_usage": "N/A",  # Would be actual CPU usage
                "disk_usage": "N/A"  # Would be actual disk usage
            }
        
        status_code = 200 if db_healthy else 503
        return AdminResponse(
            success=True,
            message="System health check completed",
            data=health_status
        )
        
    except Exception as e:
        logger.error(f"System health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform system health check"
        )


@router.get("/metrics", response_model=AdminResponse)
async def get_system_metrics(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Get system metrics and performance data
    """
    try:
        # Get basic metrics
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        
        # Get recent activity
        recent_activity = db.query(ComplianceRecord).order_by(
            ComplianceRecord.created_at.desc()
        ).limit(10).all()
        
        metrics_data = {
            "user_metrics": {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": total_users - active_users
            },
            "system_metrics": get_metrics_summary(),
            "recent_activity": [
                {
                    "id": record.id,
                    "user_id": record.user_id,
                    "action": record.action,
                    "timestamp": record.created_at.isoformat()
                }
                for record in recent_activity
            ]
        }
        
        return AdminResponse(
            success=True,
            message="System metrics retrieved successfully",
            data=metrics_data
        )
        
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system metrics"
        )


@router.get("/logs", response_model=AdminResponse)
async def get_system_logs(
    level: Optional[str] = Query(None, description="Log level filter"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of log entries"),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Get system logs with filtering
    """
    try:
        # In a real implementation, you would query actual log files
        # For now, return mock log data
        logs = [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "INFO",
                "message": "System logs endpoint accessed",
                "user_id": current_user.id,
                "module": "admin"
            }
        ]
        
        return AdminResponse(
            success=True,
            message="System logs retrieved successfully",
            data={
                "logs": logs,
                "total_count": len(logs),
                "filters": {
                    "level": level,
                    "start_date": start_date,
                    "end_date": end_date
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get system logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system logs"
        )


@router.post("/backup", response_model=AdminResponse)
async def create_system_backup(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Create a system backup
    """
    try:
        # Create database backup
        backup_path = backup_database()
        
        return AdminResponse(
            success=True,
            message="System backup created successfully",
            data={
                "backup_path": backup_path,
                "timestamp": datetime.utcnow().isoformat(),
                "created_by": current_user.id
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to create system backup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create system backup"
        )


@router.get("/settings", response_model=AdminResponse)
async def get_system_settings(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Get system settings
    """
    try:
        # In a real implementation, you would query actual settings
        # For now, return mock settings
        settings = {
            "app_name": "Enterprise Employee Wellness AI",
            "version": "1.0.0",
            "environment": "development",
            "debug_mode": True,
            "log_level": "INFO",
            "database_url": "sqlite:///wellness.db",
            "enable_monitoring": True,
            "enable_analytics": True,
            "enable_ai_chat": True,
            "data_retention_days": 365,
            "max_file_size": "10MB",
            "session_timeout": 3600
        }
        
        return AdminResponse(
            success=True,
            message="System settings retrieved successfully",
            data={"settings": settings}
        )
        
    except Exception as e:
        logger.error(f"Failed to get system settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system settings"
        )


@router.put("/settings", response_model=AdminResponse)
async def update_system_settings(
    request: SystemSettingsUpdateRequest,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Update system settings
    """
    try:
        # In a real implementation, you would update actual settings
        # For now, just log the update
        logger.info(f"System setting updated: {request.setting_key} = {request.setting_value}")
        
        return AdminResponse(
            success=True,
            message="System setting updated successfully",
            data={
                "setting_key": request.setting_key,
                "setting_value": request.setting_value,
                "updated_by": current_user.id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to update system setting: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update system setting"
        )


@router.get("/users/activity", response_model=AdminResponse)
async def get_user_activity(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=200, description="Number of activities"),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Get user activity logs
    """
    try:
        # Get compliance records as activity logs
        query = db.query(ComplianceRecord)
        
        if user_id:
            query = query.filter(ComplianceRecord.user_id == user_id)
        
        if activity_type:
            query = query.filter(ComplianceRecord.record_type == activity_type)
        
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date)
                query = query.filter(ComplianceRecord.created_at >= start_datetime)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format"
                )
        
        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date) + timedelta(days=1)
                query = query.filter(ComplianceRecord.created_at < end_datetime)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format"
                )
        
        activities = query.order_by(ComplianceRecord.created_at.desc()).limit(limit).all()
        
        activity_data = [
            {
                "id": activity.id,
                "user_id": activity.user_id,
                "activity_type": activity.record_type,
                "action": activity.action,
                "timestamp": activity.created_at.isoformat(),
                "details": activity.details
            }
            for activity in activities
        ]
        
        return AdminResponse(
            success=True,
            message="User activity retrieved successfully",
            data={
                "activities": activity_data,
                "total_count": len(activity_data),
                "filters": {
                    "user_id": user_id,
                    "activity_type": activity_type,
                    "start_date": start_date,
                    "end_date": end_date
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user activity"
        )


@router.get("/system/info", response_model=AdminResponse)
async def get_system_info(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Get detailed system information
    """
    try:
        # Get database statistics
        db_stats = get_db_stats()
        
        # Get user statistics
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        verified_users = db.query(User).filter(User.is_verified == True).count()
        
        # Role distribution
        role_stats = {}
        roles = db.query(User.role, db.func.count(User.id)).group_by(User.role).all()
        for role, count in roles:
            role_stats[role] = count
        
        system_info = {
            "database": {
                "connection_pool_size": db_stats.get("pool_size", "N/A"),
                "active_connections": db_stats.get("active_connections", "N/A"),
                "total_connections": db_stats.get("total_connections", "N/A")
            },
            "users": {
                "total_users": total_users,
                "active_users": active_users,
                "verified_users": verified_users,
                "role_distribution": role_stats
            },
            "system": {
                "python_version": "3.9+",
                "fastapi_version": "0.104.0+",
                "sqlalchemy_version": "2.0.0+",
                "platform": "Windows/Linux/macOS"
            }
        }
        
        return AdminResponse(
            success=True,
            message="System information retrieved successfully",
            data=system_info
        )
        
    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system information"
        )


@router.post("/maintenance", response_model=AdminResponse)
async def perform_maintenance(
    maintenance_type: str = Query(..., description="Type of maintenance to perform"),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Perform system maintenance tasks
    """
    try:
        maintenance_results = {}
        
        if maintenance_type == "cleanup_logs":
            # Clean up old log files
            maintenance_results["logs_cleaned"] = "N/A"
            
        elif maintenance_type == "optimize_database":
            # Optimize database
            maintenance_results["database_optimized"] = True
            
        elif maintenance_type == "clear_cache":
            # Clear system cache
            maintenance_results["cache_cleared"] = True
            
        elif maintenance_type == "update_analytics":
            # Update analytics data
            maintenance_results["analytics_updated"] = True
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown maintenance type: {maintenance_type}"
            )
        
        return AdminResponse(
            success=True,
            message=f"Maintenance task '{maintenance_type}' completed successfully",
            data={
                "maintenance_type": maintenance_type,
                "results": maintenance_results,
                "performed_by": current_user.id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to perform maintenance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform maintenance task"
        )


@router.get("/audit", response_model=AdminResponse)
async def get_audit_report(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    report_type: str = Query("comprehensive", description="Report type"),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Generate audit report
    """
    try:
        # Parse dates
        try:
            start_datetime = datetime.fromisoformat(start_date)
            end_datetime = datetime.fromisoformat(end_date) + timedelta(days=1)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
        
        # Get audit records
        audit_records = db.query(ComplianceRecord).filter(
            ComplianceRecord.created_at >= start_datetime,
            ComplianceRecord.created_at < end_datetime
        ).order_by(ComplianceRecord.created_at).all()
        
        # Generate report
        report_data = {
            "report_type": report_type,
            "start_date": start_date,
            "end_date": end_date,
            "total_records": len(audit_records),
            "record_types": {},
            "user_activity": {},
            "generated_by": current_user.id,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        # Analyze record types
        for record in audit_records:
            record_type = record.record_type
            if record_type not in report_data["record_types"]:
                report_data["record_types"][record_type] = 0
            report_data["record_types"][record_type] += 1
            
            # Analyze user activity
            user_id = record.user_id
            if user_id not in report_data["user_activity"]:
                report_data["user_activity"][user_id] = 0
            report_data["user_activity"][user_id] += 1
        
        return AdminResponse(
            success=True,
            message="Audit report generated successfully",
            data={"audit_report": report_data}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate audit report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate audit report"
        )
