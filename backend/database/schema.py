from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, JSON, 
    ForeignKey, Table, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

# Association tables for many-to-many relationships
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

user_teams = Table(
    'user_teams',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    external_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    department = Column(String(100))
    position = Column(String(100))
    manager_id = Column(String(36), ForeignKey('users.id'))
    hire_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    manager = relationship("User", remote_side=[id], backref="direct_reports")
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    teams = relationship("Team", secondary=user_teams, back_populates="members")
    conversations = relationship("Conversation", back_populates="user")
    wellness_entries = relationship("WellnessEntry", back_populates="user")
    resource_interactions = relationship("ResourceInteraction", back_populates="user")
    risk_assessments = relationship("RiskAssessment", back_populates="user")
    
    __table_args__ = (
        Index('idx_user_external_id', 'external_id'),
        Index('idx_user_email', 'email'),
        Index('idx_user_department', 'department'),
    )

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    users = relationship("User", secondary=user_roles, back_populates="roles")

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    department = Column(String(100))
    manager_id = Column(String(36), ForeignKey('users.id'))
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    members = relationship("User", secondary=user_teams, back_populates="teams")
    manager = relationship("User")

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(36), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    sentiment_score = Column(Float)
    risk_level = Column(Float)
    risk_indicators = Column(JSON)
    agent_type = Column(String(50), nullable=False)
    workflow_type = Column(String(50))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="conversations")
    
    __table_args__ = (
        Index('idx_conversation_user_id', 'user_id'),
        Index('idx_conversation_session_id', 'session_id'),
        Index('idx_conversation_created_at', 'created_at'),
        Index('idx_conversation_risk_level', 'risk_level'),
    )

class WellnessEntry(Base):
    __tablename__ = 'wellness_entries'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    entry_type = Column(String(50), nullable=False)  # mood, stress, activity, etc.
    value = Column(Float, nullable=False)
    description = Column(Text)
    tags = Column(JSON)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="wellness_entries")
    
    __table_args__ = (
        Index('idx_wellness_user_id', 'user_id'),
        Index('idx_wellness_entry_type', 'entry_type'),
        Index('idx_wellness_created_at', 'created_at'),
        CheckConstraint('value >= 0 AND value <= 10', name='check_value_range'),
    )

class WellnessResource(Base):
    __tablename__ = 'wellness_resources'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(Text)
    resource_type = Column(String(50), nullable=False)  # article, video, exercise, etc.
    category = Column(String(100))
    tags = Column(JSON)
    difficulty_level = Column(String(20))
    duration_minutes = Column(Integer)
    url = Column(String(500))
    embedding_id = Column(String(255), index=True)
    metadata = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    interactions = relationship("ResourceInteraction", back_populates="resource")
    
    __table_args__ = (
        Index('idx_resource_type', 'resource_type'),
        Index('idx_resource_category', 'category'),
        Index('idx_resource_tags', 'tags'),
        Index('idx_resource_active', 'is_active'),
    )

class ResourceInteraction(Base):
    __tablename__ = 'resource_interactions'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    resource_id = Column(String(36), ForeignKey('wellness_resources.id'), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # view, like, share, complete
    rating = Column(Integer)
    feedback = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="resource_interactions")
    resource = relationship("WellnessResource", back_populates="interactions")
    
    __table_args__ = (
        Index('idx_interaction_user_id', 'user_id'),
        Index('idx_interaction_resource_id', 'resource_id'),
        Index('idx_interaction_type', 'interaction_type'),
        Index('idx_interaction_created_at', 'created_at'),
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

class RiskAssessment(Base):
    __tablename__ = 'risk_assessments'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    risk_type = Column(String(50), nullable=False)  # burnout, stress, mental_health, etc.
    risk_level = Column(Float, nullable=False)
    confidence_score = Column(Float)
    indicators = Column(JSON)
    context = Column(Text)
    recommendations = Column(JSON)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="risk_assessments")
    
    __table_args__ = (
        Index('idx_risk_user_id', 'user_id'),
        Index('idx_risk_type', 'risk_type'),
        Index('idx_risk_level', 'risk_level'),
        Index('idx_risk_created_at', 'created_at'),
        CheckConstraint('risk_level >= 0 AND risk_level <= 1', name='check_risk_level_range'),
        CheckConstraint('confidence_score >= 0 AND confidence_score <= 1', name='check_confidence_range'),
    )

class AnalyticsReport(Base):
    __tablename__ = 'analytics_reports'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_type = Column(String(50), nullable=False)  # organizational_health, team_wellness, etc.
    report_name = Column(String(255), nullable=False)
    timeframe = Column(String(50), nullable=False)
    filters = Column(JSON)
    data = Column(JSON, nullable=False)
    insights = Column(JSON)
    recommendations = Column(JSON)
    generated_by = Column(String(36), ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_report_type', 'report_type'),
        Index('idx_report_timeframe', 'timeframe'),
        Index('idx_report_created_at', 'created_at'),
    )

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(36))
    details = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_audit_user_id', 'user_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_resource_type', 'resource_type'),
        Index('idx_audit_created_at', 'created_at'),
    )

class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20))
    tags = Column(JSON)
    timestamp = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_metric_name', 'metric_name'),
        Index('idx_metric_timestamp', 'timestamp'),
        UniqueConstraint('metric_name', 'timestamp', name='uq_metric_name_timestamp'),
    )

class AgentPerformance(Base):
    __tablename__ = 'agent_performance'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_type = Column(String(50), nullable=False)
    workflow_type = Column(String(50))
    execution_time_ms = Column(Integer, nullable=False)
    success = Column(Boolean, nullable=False)
    error_message = Column(Text)
    input_size = Column(Integer)
    output_size = Column(Integer)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_performance_agent_type', 'agent_type'),
        Index('idx_performance_workflow_type', 'workflow_type'),
        Index('idx_performance_success', 'success'),
        Index('idx_performance_created_at', 'created_at'),
    )

class PrivacyViolation(Base):
    __tablename__ = 'privacy_violations'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    violation_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    description = Column(Text, nullable=False)
    affected_user_id = Column(String(36), ForeignKey('users.id'))
    data_type = Column(String(50))
    compliance_framework = Column(String(50))
    remediation_status = Column(String(20), default='open')
    metadata = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime)
    
    __table_args__ = (
        Index('idx_violation_type', 'violation_type'),
        Index('idx_violation_severity', 'severity'),
        Index('idx_violation_status', 'remediation_status'),
        Index('idx_violation_created_at', 'created_at'),
    )
