"""
Database Schema - SQLAlchemy models for the Enterprise Employee Wellness AI application
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON, ForeignKey, Table, Enum, Date, Time, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from datetime import datetime, date
import uuid
import enum

Base = declarative_base()


# Enums for better type safety
class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR = "hr"
    ADMIN = "admin"
    EXECUTIVE = "executive"


class WellnessEntryType(enum.Enum):
    MOOD = "mood"
    STRESS = "stress"
    ENERGY = "energy"
    SLEEP_QUALITY = "sleep_quality"
    WORK_LIFE_BALANCE = "work_life_balance"
    COMPREHENSIVE = "comprehensive"
    QUICK_CHECK = "quick_check"


class RiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationType(enum.Enum):
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"
    ALERT = "alert"


class ResourceCategory(enum.Enum):
    MENTAL_HEALTH = "mental_health"
    PHYSICAL_HEALTH = "physical_health"
    STRESS_MANAGEMENT = "stress_management"
    WORK_LIFE_BALANCE = "work_life_balance"
    MINDFULNESS = "mindfulness"
    EXERCISE = "exercise"
    NUTRITION = "nutrition"
    SLEEP = "sleep"
    RELATIONSHIPS = "relationships"
    CAREER_DEVELOPMENT = "career_development"
    FINANCIAL_WELLNESS = "financial_wellness"
    SOCIAL_WELLNESS = "social_wellness"


class DifficultyLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class User(Base):
    """Enhanced User model for authentication and profile management"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    department = Column(String(100), index=True)
    position = Column(String(100))
    manager_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    company = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    hire_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, nullable=True)
    preferences = Column(JSON, default=dict)  # User preferences and settings
    wellness_profile = Column(JSON, default=dict)  # Wellness preferences and history
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    wellness_entries = relationship("WellnessEntry", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    resource_interactions = relationship("ResourceInteraction", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="user", cascade="all, delete-orphan")
    team_members = relationship("User", backref=backref("manager", remote_side=[id]))
    wellness_goals = relationship("WellnessGoal", back_populates="user", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": f"{self.first_name} {self.last_name}",
            "role": self.role.value if self.role else None,
            "department": self.department,
            "position": self.position,
            "company": self.company,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "manager_id": self.manager_id,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "preferences": self.preferences,
            "wellness_profile": self.wellness_profile,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class WellnessEntry(Base):
    """Enhanced Wellness check-in entries"""
    __tablename__ = "wellness_entries"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    entry_type = Column(Enum(WellnessEntryType), nullable=False)
    value = Column(Float, nullable=False)  # 1-10 scale
    description = Column(Text, nullable=True)
    mood_score = Column(Float, nullable=True)  # 1-10 scale
    stress_score = Column(Float, nullable=True)  # 1-10 scale
    energy_score = Column(Float, nullable=True)  # 1-10 scale
    sleep_hours = Column(Float, nullable=True)
    sleep_quality = Column(Float, nullable=True)  # 1-10 scale
    work_life_balance = Column(Float, nullable=True)  # 1-10 scale
    social_support = Column(Float, nullable=True)  # 1-10 scale
    physical_activity = Column(Float, nullable=True)  # 1-10 scale
    nutrition_quality = Column(Float, nullable=True)  # 1-10 scale
    productivity_level = Column(Float, nullable=True)  # 1-10 scale
    tags = Column(JSON, default=list)  # List of tags
    factors = Column(JSON, default=dict)  # Contributing factors
    recommendations = Column(JSON, default=list)  # AI-generated recommendations
    risk_indicators = Column(JSON, default=list)  # Risk indicators detected
    metadata = Column(JSON, default=dict)  # Additional data
    is_anonymous = Column(Boolean, default=False)  # For anonymous check-ins
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="wellness_entries")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "entry_type": self.entry_type.value if self.entry_type else None,
            "value": self.value,
            "description": self.description,
            "mood_score": self.mood_score,
            "stress_score": self.stress_score,
            "energy_score": self.energy_score,
            "sleep_hours": self.sleep_hours,
            "sleep_quality": self.sleep_quality,
            "work_life_balance": self.work_life_balance,
            "social_support": self.social_support,
            "physical_activity": self.physical_activity,
            "nutrition_quality": self.nutrition_quality,
            "productivity_level": self.productivity_level,
            "tags": self.tags,
            "factors": self.factors,
            "recommendations": self.recommendations,
            "risk_indicators": self.risk_indicators,
            "metadata": self.metadata,
            "is_anonymous": self.is_anonymous,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Conversation(Base):
    """Chat conversations between users and AI"""
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(36), nullable=False, index=True)
    message = Column(Text, nullable=False)
    sender = Column(String(20), nullable=False)  # user, ai
    sentiment = Column(String(20), nullable=True)  # positive, negative, neutral
    risk_level = Column(String(20), nullable=True)  # low, medium, high
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "message": self.message,
            "sender": self.sender,
            "sentiment": self.sentiment,
            "risk_level": self.risk_level,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


class Resource(Base):
    """Wellness resources and content"""
    __tablename__ = "resources"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    difficulty_level = Column(String(50), nullable=False)  # beginner, intermediate, advanced
    duration_minutes = Column(Integer, nullable=True)
    content_url = Column(String(500), nullable=True)
    tags = Column(JSON, default=list)
    author = Column(String(255), nullable=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    interactions = relationship("ResourceInteraction", back_populates="resource")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "difficulty_level": self.difficulty_level,
            "duration_minutes": self.duration_minutes,
            "content_url": self.content_url,
            "tags": self.tags,
            "author": self.author,
            "rating": self.rating,
            "review_count": self.review_count,
            "is_active": self.is_active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class ResourceInteraction(Base):
    """User interactions with resources"""
    __tablename__ = "resource_interactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    resource_id = Column(String(36), ForeignKey("resources.id"), nullable=False, index=True)
    interaction_type = Column(String(50), nullable=False)  # view, like, bookmark, complete, rate
    rating = Column(Integer, nullable=True)  # 1-5 stars
    comment = Column(Text, nullable=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="resource_interactions")
    resource = relationship("Resource", back_populates="interactions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "resource_id": self.resource_id,
            "interaction_type": self.interaction_type,
            "rating": self.rating,
            "comment": self.comment,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


class AnalyticsEvent(Base):
    """Analytics events for tracking user behavior"""
    __tablename__ = "analytics_events"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    event_data = Column(JSON, default=dict)
    session_id = Column(String(36), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "event_data": self.event_data,
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat()
        }


class RiskAssessment(Base):
    """Risk assessment records"""
    __tablename__ = "risk_assessments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    risk_level = Column(String(20), nullable=False)  # low, medium, high
    risk_score = Column(Float, nullable=False)
    risk_factors = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    interventions = Column(JSON, default=list)
    assessed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default="active")  # active, resolved, escalated
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "risk_factors": self.risk_factors,
            "recommendations": self.recommendations,
            "interventions": self.interventions,
            "assessed_by": self.assessed_by,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Notification(Base):
    """User notifications"""
    __tablename__ = "notifications"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # info, warning, success, error
    is_read = Column(Boolean, default=False)
    action_url = Column(String(500), nullable=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "is_read": self.is_read,
            "action_url": self.action_url,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


class TeamAnalytics(Base):
    """Team-level analytics and insights"""
    __tablename__ = "team_analytics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String(36), nullable=False, index=True)
    manager_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    metrics = Column(JSON, default=dict)  # Aggregated team metrics
    insights = Column(JSON, default=list)  # Team insights
    recommendations = Column(JSON, default=list)  # Team recommendations
    risk_alerts = Column(JSON, default=list)  # Team risk alerts
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "team_id": self.team_id,
            "manager_id": self.manager_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "metrics": self.metrics,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "risk_alerts": self.risk_alerts,
            "created_at": self.created_at.isoformat()
        }


class ComplianceRecord(Base):
    """Compliance and audit records"""
    __tablename__ = "compliance_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    record_type = Column(String(100), nullable=False)  # data_access, privacy_consent, audit_log
    action = Column(String(100), nullable=False)
    details = Column(JSON, default=dict)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "record_type": self.record_type,
            "action": self.action,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat()
        }


# New Models for Enhanced Functionality

class WellnessGoal(Base):
    """User wellness goals and objectives"""
    __tablename__ = "wellness_goals"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    goal_type = Column(String(100), nullable=False)  # physical, mental, social, career, financial
    target_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)  # hours, score, count, etc.
    start_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=True)
    status = Column(String(50), default="active")  # active, completed, paused, abandoned
    progress = Column(Float, default=0.0)  # 0-100 percentage
    milestones = Column(JSON, default=list)  # List of milestone objects
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="wellness_goals")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "goal_type": self.goal_type,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "unit": self.unit,
            "start_date": self.start_date.isoformat(),
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "status": self.status,
            "progress": self.progress,
            "milestones": self.milestones,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Intervention(Base):
    """Wellness interventions and programs"""
    __tablename__ = "interventions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    intervention_type = Column(String(100), nullable=False)  # workshop, therapy, program, resource
    status = Column(String(50), default="scheduled")  # scheduled, active, completed, cancelled
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    assigned_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    effectiveness_score = Column(Float, nullable=True)  # 0-100
    user_feedback = Column(Text, nullable=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="interventions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "intervention_type": self.intervention_type,
            "status": self.status,
            "priority": self.priority,
            "assigned_by": self.assigned_by,
            "assigned_to": self.assigned_to,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "effectiveness_score": self.effectiveness_score,
            "user_feedback": self.user_feedback,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Team(Base):
    """Team management and structure"""
    __tablename__ = "teams"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    manager_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    department = Column(String(100), nullable=True)
    team_size = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    wellness_score = Column(Float, nullable=True)  # Average team wellness score
    last_assessment = Column(DateTime, nullable=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "manager_id": self.manager_id,
            "department": self.department,
            "team_size": self.team_size,
            "is_active": self.is_active,
            "wellness_score": self.wellness_score,
            "last_assessment": self.last_assessment.isoformat() if self.last_assessment else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class TeamMember(Base):
    """Team membership associations"""
    __tablename__ = "team_members"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(50), default="member")  # member, lead, observer
    joined_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "team_id": self.team_id,
            "user_id": self.user_id,
            "role": self.role,
            "joined_at": self.joined_at.isoformat(),
            "is_active": self.is_active
        }


class WellnessProgram(Base):
    """Wellness programs and initiatives"""
    __tablename__ = "wellness_programs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    program_type = Column(String(100), nullable=False)  # mental_health, physical, social, financial
    target_audience = Column(String(100), nullable=True)  # all, managers, specific_department
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    max_participants = Column(Integer, nullable=True)
    current_participants = Column(Integer, default=0)
    success_metrics = Column(JSON, default=dict)
    budget = Column(Float, nullable=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "program_type": self.program_type,
            "target_audience": self.target_audience,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.is_active,
            "max_participants": self.max_participants,
            "current_participants": self.current_participants,
            "success_metrics": self.success_metrics,
            "budget": self.budget,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class ProgramParticipant(Base):
    """Program participation tracking"""
    __tablename__ = "program_participants"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id = Column(String(36), ForeignKey("wellness_programs.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(50), default="enrolled")  # enrolled, active, completed, dropped
    enrollment_date = Column(DateTime, default=func.now())
    completion_date = Column(DateTime, nullable=True)
    progress = Column(Float, default=0.0)  # 0-100 percentage
    feedback = Column(Text, nullable=True)
    satisfaction_score = Column(Float, nullable=True)  # 1-5 scale
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "program_id": self.program_id,
            "user_id": self.user_id,
            "status": self.status,
            "enrollment_date": self.enrollment_date.isoformat(),
            "completion_date": self.completion_date.isoformat() if self.completion_date else None,
            "progress": self.progress,
            "feedback": self.feedback,
            "satisfaction_score": self.satisfaction_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class AnalyticsReport(Base):
    """Analytics and reporting data"""
    __tablename__ = "analytics_reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_type = Column(String(100), nullable=False)  # wellness_trends, risk_assessment, team_analytics
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    data_period = Column(String(50), nullable=False)  # daily, weekly, monthly, quarterly
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    metrics = Column(JSON, default=dict)  # Calculated metrics
    insights = Column(JSON, default=list)  # AI-generated insights
    recommendations = Column(JSON, default=list)  # Recommendations
    generated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "report_type": self.report_type,
            "title": self.title,
            "description": self.description,
            "data_period": self.data_period,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "metrics": self.metrics,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "generated_by": self.generated_by,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat()
        }


class SystemSettings(Base):
    """System configuration and settings"""
    __tablename__ = "system_settings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    setting_key = Column(String(255), unique=True, nullable=False, index=True)
    setting_value = Column(Text, nullable=False)
    setting_type = Column(String(50), nullable=False)  # string, integer, float, boolean, json
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # wellness, notifications, privacy, etc.
    is_public = Column(Boolean, default=False)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "setting_key": self.setting_key,
            "setting_value": self.setting_value,
            "setting_type": self.setting_type,
            "description": self.description,
            "category": self.category,
            "is_public": self.is_public,
            "updated_by": self.updated_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
