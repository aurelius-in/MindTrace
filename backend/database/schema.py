"""
Database Schema - SQLAlchemy models for the wellness application
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(50), default="employee")  # employee, manager, hr, admin
    department = Column(String(100))
    position = Column(String(100))
    manager_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    wellness_entries = relationship("WellnessEntry", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")
    resource_interactions = relationship("ResourceInteraction", back_populates="user")
    team_members = relationship("User", backref=backref("manager", remote_side=[id]))
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "department": self.department,
            "position": self.position,
            "manager_id": self.manager_id,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class WellnessEntry(Base):
    """Wellness check-in entries"""
    __tablename__ = "wellness_entries"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    entry_type = Column(String(50), nullable=False)  # mood, stress, energy, sleep_quality, work_life_balance, comprehensive
    value = Column(Float, nullable=False)  # 1-10 scale
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # List of tags
    metadata = Column(JSON, default=dict)  # Additional data
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="wellness_entries")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "entry_type": self.entry_type,
            "value": self.value,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata,
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
