"""
Notifications API Routes - User notifications and alerts management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from utils.auth import get_current_user, require_permission
from database.connection import get_db
from database.schema import User, Notification

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


# Pydantic models
class NotificationCreateRequest(BaseModel):
    user_id: str
    title: str
    message: str
    notification_type: str = "info"  # info, warning, success, error
    action_url: Optional[str] = None

class NotificationUpdateRequest(BaseModel):
    is_read: Optional[bool] = None

class NotificationResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.get("/", response_model=NotificationResponse)
async def get_notifications(
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    notification_type: Optional[str] = Query(None, description="Filter by notification type"),
    limit: int = Query(20, ge=1, le=100, description="Number of notifications to return"),
    offset: int = Query(0, ge=0, description="Number of notifications to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's notifications
    """
    try:
        query = db.query(Notification).filter(Notification.user_id == current_user.id)
        
        # Apply filters
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        
        if notification_type:
            query = query.filter(Notification.notification_type == notification_type)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination and ordering
        notifications = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()
        
        return NotificationResponse(
            success=True,
            message="Notifications retrieved successfully",
            data={
                "notifications": [notification.to_dict() for notification in notifications],
                "total_count": total_count,
                "unread_count": db.query(Notification).filter(
                    Notification.user_id == current_user.id,
                    Notification.is_read == False
                ).count(),
                "limit": limit,
                "offset": offset
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get notifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notifications"
        )


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific notification
    """
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        return NotificationResponse(
            success=True,
            message="Notification retrieved successfully",
            data={"notification": notification.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get notification {notification_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notification"
        )


@router.post("/", response_model=NotificationResponse)
async def create_notification(
    request: NotificationCreateRequest,
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Create a new notification
    """
    try:
        # Verify target user exists
        target_user = db.query(User).filter(User.id == request.user_id).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Target user not found"
            )
        
        notification = Notification(
            user_id=request.user_id,
            title=request.title,
            message=request.message,
            notification_type=request.notification_type,
            action_url=request.action_url,
            is_read=False
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        return NotificationResponse(
            success=True,
            message="Notification created successfully",
            data={"notification": notification.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create notification: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification"
        )


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: str,
    request: NotificationUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a notification (mark as read/unread)
    """
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        # Update fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(notification, field, value)
        
        db.commit()
        db.refresh(notification)
        
        return NotificationResponse(
            success=True,
            message="Notification updated successfully",
            data={"notification": notification.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update notification {notification_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification"
        )


@router.delete("/{notification_id}", response_model=NotificationResponse)
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a notification
    """
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        db.delete(notification)
        db.commit()
        
        return NotificationResponse(
            success=True,
            message="Notification deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete notification {notification_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete notification"
        )


@router.post("/mark-all-read", response_model=NotificationResponse)
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all notifications as read
    """
    try:
        # Update all unread notifications for the user
        updated_count = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ).update({"is_read": True})
        
        db.commit()
        
        return NotificationResponse(
            success=True,
            message=f"Marked {updated_count} notifications as read",
            data={"updated_count": updated_count}
        )
        
    except Exception as e:
        logger.error(f"Failed to mark notifications as read: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark notifications as read"
        )


@router.get("/stats", response_model=NotificationResponse)
async def get_notification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get notification statistics for current user
    """
    try:
        total_notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id
        ).count()
        
        unread_notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ).count()
        
        # Type distribution
        type_stats = {}
        types = db.query(Notification.notification_type, db.func.count(Notification.id)).filter(
            Notification.user_id == current_user.id
        ).group_by(Notification.notification_type).all()
        
        for notification_type, count in types:
            type_stats[notification_type] = count
        
        # Recent notifications (last 7 days)
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.created_at >= week_ago
        ).count()
        
        return NotificationResponse(
            success=True,
            message="Notification statistics retrieved successfully",
            data={
                "total_notifications": total_notifications,
                "unread_notifications": unread_notifications,
                "read_notifications": total_notifications - unread_notifications,
                "type_distribution": type_stats,
                "recent_notifications": recent_notifications
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get notification stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notification statistics"
        )


@router.post("/bulk-create", response_model=NotificationResponse)
async def create_bulk_notifications(
    user_ids: List[str],
    title: str,
    message: str,
    notification_type: str = "info",
    action_url: Optional[str] = None,
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Create notifications for multiple users
    """
    try:
        # Verify all target users exist
        target_users = db.query(User).filter(User.id.in_(user_ids)).all()
        if len(target_users) != len(user_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more target users not found"
            )
        
        notifications = []
        for user_id in user_ids:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                action_url=action_url,
                is_read=False
            )
            notifications.append(notification)
        
        db.add_all(notifications)
        db.commit()
        
        return NotificationResponse(
            success=True,
            message=f"Created {len(notifications)} notifications successfully",
            data={"created_count": len(notifications)}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create bulk notifications: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create bulk notifications"
        )


@router.delete("/bulk-delete", response_model=NotificationResponse)
async def delete_bulk_notifications(
    notification_ids: List[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete multiple notifications
    """
    try:
        # Get notifications that belong to the current user
        notifications = db.query(Notification).filter(
            Notification.id.in_(notification_ids),
            Notification.user_id == current_user.id
        ).all()
        
        if not notifications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No notifications found to delete"
            )
        
        # Delete notifications
        for notification in notifications:
            db.delete(notification)
        
        db.commit()
        
        return NotificationResponse(
            success=True,
            message=f"Deleted {len(notifications)} notifications successfully",
            data={"deleted_count": len(notifications)}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete bulk notifications: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete bulk notifications"
        )
