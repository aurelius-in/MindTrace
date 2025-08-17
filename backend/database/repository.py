"""
Database Repository Layer - Clean data access patterns for the wellness application
"""

from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, or_, desc, asc, func
from datetime import datetime, date, timedelta
import logging

from database.schema import (
    User, WellnessEntry, Conversation, Resource, ResourceInteraction,
    AnalyticsEvent, RiskAssessment, Notification, TeamAnalytics,
    ComplianceRecord, WellnessGoal, Intervention, Team, TeamMember,
    WellnessProgram, ProgramParticipant, AnalyticsReport, SystemSettings
)
from database.connection import get_db_context

logger = logging.getLogger(__name__)


class BaseRepository:
    """Base repository with common CRUD operations"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def create(self, data: Dict[str, Any]) -> Any:
        """Create a new record"""
        try:
            with get_db_context() as db:
                instance = self.model_class(**data)
                db.add(instance)
                db.commit()
                db.refresh(instance)
                return instance
        except Exception as e:
            logger.error(f"Error creating {self.model_class.__name__}: {e}")
            raise
    
    def get_by_id(self, record_id: str) -> Optional[Any]:
        """Get record by ID"""
        try:
            with get_db_context() as db:
                return db.query(self.model_class).filter(
                    self.model_class.id == record_id
                ).first()
        except Exception as e:
            logger.error(f"Error getting {self.model_class.__name__} by ID: {e}")
            return None
    
    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Any]:
        """Get all records with optional pagination"""
        try:
            with get_db_context() as db:
                query = db.query(self.model_class)
                if offset:
                    query = query.offset(offset)
                if limit:
                    query = query.limit(limit)
                return query.all()
        except Exception as e:
            logger.error(f"Error getting all {self.model_class.__name__}: {e}")
            return []
    
    def update(self, record_id: str, data: Dict[str, Any]) -> Optional[Any]:
        """Update a record"""
        try:
            with get_db_context() as db:
                instance = db.query(self.model_class).filter(
                    self.model_class.id == record_id
                ).first()
                if instance:
                    for key, value in data.items():
                        if hasattr(instance, key):
                            setattr(instance, key, value)
                    instance.updated_at = datetime.utcnow()
                    db.commit()
                    db.refresh(instance)
                    return instance
                return None
        except Exception as e:
            logger.error(f"Error updating {self.model_class.__name__}: {e}")
            return None
    
    def delete(self, record_id: str) -> bool:
        """Delete a record"""
        try:
            with get_db_context() as db:
                instance = db.query(self.model_class).filter(
                    self.model_class.id == record_id
                ).first()
                if instance:
                    db.delete(instance)
                    db.commit()
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting {self.model_class.__name__}: {e}")
            return False
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters"""
        try:
            with get_db_context() as db:
                query = db.query(self.model_class)
                if filters:
                    for key, value in filters.items():
                        if hasattr(self.model_class, key):
                            query = query.filter(getattr(self.model_class, key) == value)
                return query.count()
        except Exception as e:
            logger.error(f"Error counting {self.model_class.__name__}: {e}")
            return 0


class UserRepository(BaseRepository):
    """User-specific repository operations"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            with get_db_context() as db:
                return db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def get_by_department(self, department: str) -> List[User]:
        """Get users by department"""
        try:
            with get_db_context() as db:
                return db.query(User).filter(
                    User.department == department,
                    User.is_active == True
                ).all()
        except Exception as e:
            logger.error(f"Error getting users by department: {e}")
            return []
    
    def get_team_members(self, manager_id: str) -> List[User]:
        """Get team members for a manager"""
        try:
            with get_db_context() as db:
                return db.query(User).filter(
                    User.manager_id == manager_id,
                    User.is_active == True
                ).all()
        except Exception as e:
            logger.error(f"Error getting team members: {e}")
            return []
    
    def get_active_users(self) -> List[User]:
        """Get all active users"""
        try:
            with get_db_context() as db:
                return db.query(User).filter(User.is_active == True).all()
        except Exception as e:
            logger.error(f"Error getting active users: {e}")
            return []
    
    def update_last_login(self, user_id: str) -> bool:
        """Update user's last login time"""
        try:
            with get_db_context() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.last_login = datetime.utcnow()
                    user.last_activity = datetime.utcnow()
                    db.commit()
                    return True
                return False
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            return False


class WellnessEntryRepository(BaseRepository):
    """Wellness entry-specific repository operations"""
    
    def __init__(self):
        super().__init__(WellnessEntry)
    
    def get_user_entries(self, user_id: str, limit: Optional[int] = None) -> List[WellnessEntry]:
        """Get wellness entries for a user"""
        try:
            with get_db_context() as db:
                query = db.query(WellnessEntry).filter(
                    WellnessEntry.user_id == user_id
                ).order_by(desc(WellnessEntry.created_at))
                if limit:
                    query = query.limit(limit)
                return query.all()
        except Exception as e:
            logger.error(f"Error getting user wellness entries: {e}")
            return []
    
    def get_entries_by_type(self, user_id: str, entry_type: str, days: int = 30) -> List[WellnessEntry]:
        """Get wellness entries by type within a time period"""
        try:
            with get_db_context() as db:
                start_date = datetime.utcnow() - timedelta(days=days)
                return db.query(WellnessEntry).filter(
                    WellnessEntry.user_id == user_id,
                    WellnessEntry.entry_type == entry_type,
                    WellnessEntry.created_at >= start_date
                ).order_by(desc(WellnessEntry.created_at)).all()
        except Exception as e:
            logger.error(f"Error getting entries by type: {e}")
            return []
    
    def get_department_averages(self, department: str, days: int = 30) -> Dict[str, float]:
        """Get average wellness scores for a department"""
        try:
            with get_db_context() as db:
                start_date = datetime.utcnow() - timedelta(days=days)
                
                # Get users in department
                user_ids = [user.id for user in db.query(User).filter(
                    User.department == department,
                    User.is_active == True
                ).all()]
                
                if not user_ids:
                    return {}
                
                # Calculate averages
                result = db.query(
                    WellnessEntry.entry_type,
                    func.avg(WellnessEntry.value).label('average_value')
                ).filter(
                    WellnessEntry.user_id.in_(user_ids),
                    WellnessEntry.created_at >= start_date
                ).group_by(WellnessEntry.entry_type).all()
                
                return {row.entry_type: float(row.average_value) for row in result}
        except Exception as e:
            logger.error(f"Error getting department averages: {e}")
            return {}
    
    def get_trend_data(self, user_id: str, entry_type: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get trend data for wellness entries"""
        try:
            with get_db_context() as db:
                start_date = datetime.utcnow() - timedelta(days=days)
                entries = db.query(WellnessEntry).filter(
                    WellnessEntry.user_id == user_id,
                    WellnessEntry.entry_type == entry_type,
                    WellnessEntry.created_at >= start_date
                ).order_by(asc(WellnessEntry.created_at)).all()
                
                return [entry.to_dict() for entry in entries]
        except Exception as e:
            logger.error(f"Error getting trend data: {e}")
            return []


class ResourceRepository(BaseRepository):
    """Resource-specific repository operations"""
    
    def __init__(self):
        super().__init__(Resource)
    
    def get_by_category(self, category: str) -> List[Resource]:
        """Get resources by category"""
        try:
            with get_db_context() as db:
                return db.query(Resource).filter(
                    Resource.category == category,
                    Resource.is_active == True
                ).all()
        except Exception as e:
            logger.error(f"Error getting resources by category: {e}")
            return []
    
    def get_by_difficulty(self, difficulty: str) -> List[Resource]:
        """Get resources by difficulty level"""
        try:
            with get_db_context() as db:
                return db.query(Resource).filter(
                    Resource.difficulty_level == difficulty,
                    Resource.is_active == True
                ).all()
        except Exception as e:
            logger.error(f"Error getting resources by difficulty: {e}")
            return []
    
    def search_resources(self, query: str) -> List[Resource]:
        """Search resources by title or description"""
        try:
            with get_db_context() as db:
                return db.query(Resource).filter(
                    and_(
                        Resource.is_active == True,
                        or_(
                            Resource.title.ilike(f"%{query}%"),
                            Resource.description.ilike(f"%{query}%")
                        )
                    )
                ).all()
        except Exception as e:
            logger.error(f"Error searching resources: {e}")
            return []
    
    def get_popular_resources(self, limit: int = 10) -> List[Resource]:
        """Get most popular resources by rating"""
        try:
            with get_db_context() as db:
                return db.query(Resource).filter(
                    Resource.is_active == True
                ).order_by(desc(Resource.rating)).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting popular resources: {e}")
            return []


class RiskAssessmentRepository(BaseRepository):
    """Risk assessment-specific repository operations"""
    
    def __init__(self):
        super().__init__(RiskAssessment)
    
    def get_user_assessments(self, user_id: str) -> List[RiskAssessment]:
        """Get risk assessments for a user"""
        try:
            with get_db_context() as db:
                return db.query(RiskAssessment).filter(
                    RiskAssessment.user_id == user_id
                ).order_by(desc(RiskAssessment.created_at)).all()
        except Exception as e:
            logger.error(f"Error getting user risk assessments: {e}")
            return []
    
    def get_high_risk_users(self) -> List[RiskAssessment]:
        """Get all high-risk assessments"""
        try:
            with get_db_context() as db:
                return db.query(RiskAssessment).filter(
                    RiskAssessment.risk_level.in_(['high', 'critical']),
                    RiskAssessment.status == 'active'
                ).order_by(desc(RiskAssessment.risk_score)).all()
        except Exception as e:
            logger.error(f"Error getting high risk users: {e}")
            return []
    
    def get_department_risk_summary(self, department: str) -> Dict[str, Any]:
        """Get risk summary for a department"""
        try:
            with get_db_context() as db:
                # Get users in department
                user_ids = [user.id for user in db.query(User).filter(
                    User.department == department,
                    User.is_active == True
                ).all()]
                
                if not user_ids:
                    return {}
                
                # Get risk assessments
                assessments = db.query(RiskAssessment).filter(
                    RiskAssessment.user_id.in_(user_ids),
                    RiskAssessment.status == 'active'
                ).all()
                
                if not assessments:
                    return {}
                
                # Calculate summary
                total_assessments = len(assessments)
                high_risk_count = len([a for a in assessments if a.risk_level in ['high', 'critical']])
                avg_risk_score = sum(a.risk_score for a in assessments) / total_assessments
                
                return {
                    'total_assessments': total_assessments,
                    'high_risk_count': high_risk_count,
                    'high_risk_percentage': (high_risk_count / total_assessments) * 100,
                    'average_risk_score': avg_risk_score
                }
        except Exception as e:
            logger.error(f"Error getting department risk summary: {e}")
            return {}


class NotificationRepository(BaseRepository):
    """Notification-specific repository operations"""
    
    def __init__(self):
        super().__init__(Notification)
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        """Get notifications for a user"""
        try:
            with get_db_context() as db:
                query = db.query(Notification).filter(Notification.user_id == user_id)
                if unread_only:
                    query = query.filter(Notification.is_read == False)
                return query.order_by(desc(Notification.created_at)).all()
        except Exception as e:
            logger.error(f"Error getting user notifications: {e}")
            return []
    
    def mark_as_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        try:
            with get_db_context() as db:
                notification = db.query(Notification).filter(
                    Notification.id == notification_id
                ).first()
                if notification:
                    notification.is_read = True
                    db.commit()
                    return True
                return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return False
    
    def mark_all_as_read(self, user_id: str) -> bool:
        """Mark all notifications as read for a user"""
        try:
            with get_db_context() as db:
                db.query(Notification).filter(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                ).update({'is_read': True})
                db.commit()
                return True
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return False


class TeamRepository(BaseRepository):
    """Team-specific repository operations"""
    
    def __init__(self):
        super().__init__(Team)
    
    def get_teams_by_manager(self, manager_id: str) -> List[Team]:
        """Get teams managed by a user"""
        try:
            with get_db_context() as db:
                return db.query(Team).filter(
                    Team.manager_id == manager_id,
                    Team.is_active == True
                ).all()
        except Exception as e:
            logger.error(f"Error getting teams by manager: {e}")
            return []
    
    def get_team_members(self, team_id: str) -> List[User]:
        """Get all members of a team"""
        try:
            with get_db_context() as db:
                return db.query(User).join(TeamMember).filter(
                    TeamMember.team_id == team_id,
                    TeamMember.is_active == True,
                    User.is_active == True
                ).all()
        except Exception as e:
            logger.error(f"Error getting team members: {e}")
            return []
    
    def update_team_wellness_score(self, team_id: str) -> bool:
        """Update team wellness score based on member data"""
        try:
            with get_db_context() as db:
                # Get team members
                member_ids = [tm.user_id for tm in db.query(TeamMember).filter(
                    TeamMember.team_id == team_id,
                    TeamMember.is_active == True
                ).all()]
                
                if not member_ids:
                    return False
                
                # Calculate average wellness score from recent entries
                start_date = datetime.utcnow() - timedelta(days=30)
                avg_score = db.query(func.avg(WellnessEntry.value)).filter(
                    WellnessEntry.user_id.in_(member_ids),
                    WellnessEntry.created_at >= start_date
                ).scalar()
                
                if avg_score:
                    team = db.query(Team).filter(Team.id == team_id).first()
                    if team:
                        team.wellness_score = float(avg_score)
                        team.last_assessment = datetime.utcnow()
                        db.commit()
                        return True
                
                return False
        except Exception as e:
            logger.error(f"Error updating team wellness score: {e}")
            return False


class AnalyticsRepository(BaseRepository):
    """Analytics-specific repository operations"""
    
    def __init__(self):
        super().__init__(AnalyticsReport)
    
    def get_reports_by_type(self, report_type: str, limit: int = 10) -> List[AnalyticsReport]:
        """Get analytics reports by type"""
        try:
            with get_db_context() as db:
                return db.query(AnalyticsReport).filter(
                    AnalyticsReport.report_type == report_type
                ).order_by(desc(AnalyticsReport.created_at)).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting reports by type: {e}")
            return []
    
    def create_wellness_trend_report(self, start_date: datetime, end_date: datetime) -> Optional[AnalyticsReport]:
        """Create a wellness trend report"""
        try:
            with get_db_context() as db:
                # Calculate metrics
                total_entries = db.query(WellnessEntry).filter(
                    WellnessEntry.created_at.between(start_date, end_date)
                ).count()
                
                avg_wellness_score = db.query(func.avg(WellnessEntry.value)).filter(
                    WellnessEntry.created_at.between(start_date, end_date)
                ).scalar()
                
                # Create report
                report_data = {
                    "report_type": "wellness_trends",
                    "title": f"Wellness Trends Report ({start_date.date()} - {end_date.date()})",
                    "description": "Automated wellness trends analysis",
                    "data_period": "daily",
                    "start_date": start_date,
                    "end_date": end_date,
                    "metrics": {
                        "total_entries": total_entries,
                        "average_wellness_score": float(avg_wellness_score) if avg_wellness_score else 0.0,
                        "period_days": (end_date - start_date).days
                    },
                    "insights": [],
                    "recommendations": []
                }
                
                report = AnalyticsReport(**report_data)
                db.add(report)
                db.commit()
                db.refresh(report)
                return report
        except Exception as e:
            logger.error(f"Error creating wellness trend report: {e}")
            return None


class SystemSettingsRepository(BaseRepository):
    """System settings-specific repository operations"""
    
    def __init__(self):
        super().__init__(SystemSettings)
    
    def get_setting(self, key: str) -> Optional[SystemSettings]:
        """Get a system setting by key"""
        try:
            with get_db_context() as db:
                return db.query(SystemSettings).filter(
                    SystemSettings.setting_key == key
                ).first()
        except Exception as e:
            logger.error(f"Error getting system setting: {e}")
            return None
    
    def get_settings_by_category(self, category: str) -> List[SystemSettings]:
        """Get system settings by category"""
        try:
            with get_db_context() as db:
                return db.query(SystemSettings).filter(
                    SystemSettings.category == category
                ).all()
        except Exception as e:
            logger.error(f"Error getting settings by category: {e}")
            return []
    
    def update_setting(self, key: str, value: str, updated_by: str = None) -> bool:
        """Update a system setting"""
        try:
            with get_db_context() as db:
                setting = db.query(SystemSettings).filter(
                    SystemSettings.setting_key == key
                ).first()
                if setting:
                    setting.setting_value = value
                    setting.updated_by = updated_by
                    setting.updated_at = datetime.utcnow()
                    db.commit()
                    return True
                return False
        except Exception as e:
            logger.error(f"Error updating system setting: {e}")
            return False


# Repository instances
user_repo = UserRepository()
wellness_entry_repo = WellnessEntryRepository()
resource_repo = ResourceRepository()
risk_assessment_repo = RiskAssessmentRepository()
notification_repo = NotificationRepository()
team_repo = TeamRepository()
analytics_repo = AnalyticsRepository()
system_settings_repo = SystemSettingsRepository()
