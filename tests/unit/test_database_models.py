"""
Unit tests for database models
"""
import pytest
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from database.schema import (
    User, WellnessEntry, Conversation, Resource, ResourceInteraction,
    AnalyticsEvent, RiskAssessment, Notification, TeamAnalytics,
    ComplianceRecord, WellnessGoal, Intervention, Team, TeamMember,
    WellnessProgram, ProgramParticipant, AnalyticsReport, SystemSettings,
    UserRole, WellnessEntryType, RiskLevel, NotificationType,
    ResourceCategory, DifficultyLevel
)


class TestUserModel:
    """Test User model functionality."""
    
    def test_user_creation(self, db_session):
        """Test basic user creation."""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User",
            role=UserRole.EMPLOYEE,
            department="Engineering"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.role == UserRole.EMPLOYEE
        assert user.is_active is True
        assert user.is_verified is False
    
    def test_user_to_dict(self, db_session):
        """Test user serialization to dictionary."""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User",
            role=UserRole.MANAGER,
            department="Engineering"
        )
        db_session.add(user)
        db_session.commit()
        
        user_dict = user.to_dict()
        assert user_dict["email"] == "test@example.com"
        assert user_dict["full_name"] == "Test User"
        assert user_dict["role"] == "manager"
        assert "password_hash" not in user_dict
    
    def test_user_unique_email_constraint(self, db_session):
        """Test that email uniqueness is enforced."""
        user1 = User(
            email="test@example.com",
            password_hash="hash1",
            first_name="Test1",
            last_name="User1"
        )
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(
            email="test@example.com",
            password_hash="hash2",
            first_name="Test2",
            last_name="User2"
        )
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_relationships(self, db_session):
        """Test user relationships with other models."""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create wellness entry
        entry = WellnessEntry(
            user_id=user.id,
            entry_type=WellnessEntryType.MOOD,
            value=7.5
        )
        db_session.add(entry)
        db_session.commit()
        
        assert len(user.wellness_entries) == 1
        assert user.wellness_entries[0].id == entry.id


class TestWellnessEntryModel:
    """Test WellnessEntry model functionality."""
    
    def test_wellness_entry_creation(self, db_session, sample_user):
        """Test basic wellness entry creation."""
        entry = WellnessEntry(
            user_id=sample_user.id,
            entry_type=WellnessEntryType.COMPREHENSIVE,
            value=7.5,
            description="Feeling good today",
            mood_score=8.0,
            stress_score=4.0,
            energy_score=7.0
        )
        db_session.add(entry)
        db_session.commit()
        
        assert entry.id is not None
        assert entry.user_id == sample_user.id
        assert entry.entry_type == WellnessEntryType.COMPREHENSIVE
        assert entry.value == 7.5
        assert entry.mood_score == 8.0
    
    def test_wellness_entry_to_dict(self, db_session, sample_user):
        """Test wellness entry serialization."""
        entry = WellnessEntry(
            user_id=sample_user.id,
            entry_type=WellnessEntryType.STRESS,
            value=6.0,
            tags=["stressful", "work"],
            factors={"workload": "high"}
        )
        db_session.add(entry)
        db_session.commit()
        
        entry_dict = entry.to_dict()
        assert entry_dict["entry_type"] == "stress"
        assert entry_dict["value"] == 6.0
        assert entry_dict["tags"] == ["stressful", "work"]
        assert entry_dict["factors"] == {"workload": "high"}
    
    def test_wellness_entry_validation(self, db_session, sample_user):
        """Test wellness entry validation."""
        # Test required fields
        entry = WellnessEntry(
            user_id=sample_user.id,
            entry_type=WellnessEntryType.MOOD,
            value=5.0
        )
        db_session.add(entry)
        db_session.commit()
        
        assert entry.id is not None
    
    def test_wellness_entry_relationships(self, db_session, sample_user):
        """Test wellness entry relationships."""
        entry = WellnessEntry(
            user_id=sample_user.id,
            entry_type=WellnessEntryType.MOOD,
            value=7.0
        )
        db_session.add(entry)
        db_session.commit()
        
        assert entry.user.id == sample_user.id
        assert entry.user.email == sample_user.email


class TestResourceModel:
    """Test Resource model functionality."""
    
    def test_resource_creation(self, db_session):
        """Test basic resource creation."""
        resource = Resource(
            title="Stress Management Guide",
            description="A comprehensive guide to managing stress",
            category=ResourceCategory.STRESS_MANAGEMENT,
            difficulty_level=DifficultyLevel.BEGINNER,
            duration_minutes=15,
            tags=["stress", "management", "guide"],
            author="Wellness Team"
        )
        db_session.add(resource)
        db_session.commit()
        
        assert resource.id is not None
        assert resource.title == "Stress Management Guide"
        assert resource.category == ResourceCategory.STRESS_MANAGEMENT
        assert resource.difficulty_level == DifficultyLevel.BEGINNER
        assert resource.view_count == 0
        assert resource.rating == 0.0
    
    def test_resource_to_dict(self, db_session):
        """Test resource serialization."""
        resource = Resource(
            title="Test Resource",
            description="Test description",
            category=ResourceCategory.MENTAL_HEALTH,
            difficulty_level=DifficultyLevel.INTERMEDIATE,
            duration_minutes=30,
            tags=["test", "resource"],
            author="Test Author",
            content_url="https://example.com",
            rating=4.5,
            rating_count=10
        )
        db_session.add(resource)
        db_session.commit()
        
        resource_dict = resource.to_dict()
        assert resource_dict["title"] == "Test Resource"
        assert resource_dict["category"] == "mental_health"
        assert resource_dict["difficulty_level"] == "intermediate"
        assert resource_dict["rating"] == 4.5
        assert resource_dict["rating_count"] == 10
    
    def test_resource_view_count_increment(self, db_session):
        """Test resource view count increment."""
        resource = Resource(
            title="Test Resource",
            description="Test description",
            category=ResourceCategory.PHYSICAL_HEALTH,
            difficulty_level=DifficultyLevel.BEGINNER,
            duration_minutes=10,
            tags=["test"],
            author="Test Author"
        )
        db_session.add(resource)
        db_session.commit()
        
        initial_count = resource.view_count
        resource.view_count += 1
        db_session.commit()
        
        assert resource.view_count == initial_count + 1


class TestTeamModel:
    """Test Team model functionality."""
    
    def test_team_creation(self, db_session, sample_user):
        """Test basic team creation."""
        team = Team(
            name="Engineering Team",
            description="Software engineering team",
            manager_id=sample_user.id,
            department="Engineering",
            team_size=5,
            wellness_score=7.5
        )
        db_session.add(team)
        db_session.commit()
        
        assert team.id is not None
        assert team.name == "Engineering Team"
        assert team.manager_id == sample_user.id
        assert team.team_size == 5
        assert team.wellness_score == 7.5
        assert team.is_active is True
    
    def test_team_to_dict(self, db_session, sample_user):
        """Test team serialization."""
        team = Team(
            name="Test Team",
            description="Test team description",
            manager_id=sample_user.id,
            department="Test Department",
            team_size=3,
            wellness_score=8.0,
            metadata={"location": "Remote", "timezone": "UTC"}
        )
        db_session.add(team)
        db_session.commit()
        
        team_dict = team.to_dict()
        assert team_dict["name"] == "Test Team"
        assert team_dict["department"] == "Test Department"
        assert team_dict["team_size"] == 3
        assert team_dict["wellness_score"] == 8.0
        assert team_dict["metadata"] == {"location": "Remote", "timezone": "UTC"}


class TestNotificationModel:
    """Test Notification model functionality."""
    
    def test_notification_creation(self, db_session, sample_user):
        """Test basic notification creation."""
        notification = Notification(
            user_id=sample_user.id,
            title="Wellness Reminder",
            message="Don't forget your wellness check-in",
            notification_type=NotificationType.INFO,
            priority="medium"
        )
        db_session.add(notification)
        db_session.commit()
        
        assert notification.id is not None
        assert notification.user_id == sample_user.id
        assert notification.title == "Wellness Reminder"
        assert notification.notification_type == NotificationType.INFO
        assert notification.is_read is False
    
    def test_notification_to_dict(self, db_session, sample_user):
        """Test notification serialization."""
        notification = Notification(
            user_id=sample_user.id,
            title="Test Notification",
            message="Test message",
            notification_type=NotificationType.WARNING,
            priority="high",
            is_read=True,
            metadata={"action_required": True}
        )
        db_session.add(notification)
        db_session.commit()
        
        notification_dict = notification.to_dict()
        assert notification_dict["title"] == "Test Notification"
        assert notification_dict["notification_type"] == "warning"
        assert notification_dict["priority"] == "high"
        assert notification_dict["is_read"] is True
        assert notification_dict["metadata"] == {"action_required": True}


class TestWellnessGoalModel:
    """Test WellnessGoal model functionality."""
    
    def test_wellness_goal_creation(self, db_session, sample_user):
        """Test basic wellness goal creation."""
        goal = WellnessGoal(
            user_id=sample_user.id,
            title="Improve Sleep Quality",
            description="Get 8 hours of sleep per night",
            goal_type="physical",
            target_value=8.0,
            current_value=6.0,
            unit="hours",
            start_date=date.today(),
            target_date=date.today().replace(month=date.today().month + 1),
            progress=25.0
        )
        db_session.add(goal)
        db_session.commit()
        
        assert goal.id is not None
        assert goal.user_id == sample_user.id
        assert goal.title == "Improve Sleep Quality"
        assert goal.goal_type == "physical"
        assert goal.target_value == 8.0
        assert goal.current_value == 6.0
        assert goal.progress == 25.0
        assert goal.status == "active"
    
    def test_wellness_goal_to_dict(self, db_session, sample_user):
        """Test wellness goal serialization."""
        goal = WellnessGoal(
            user_id=sample_user.id,
            title="Test Goal",
            description="Test goal description",
            goal_type="mental",
            target_value=10.0,
            current_value=7.0,
            unit="score",
            start_date=date.today(),
            progress=70.0,
            milestones=[{"date": "2024-01-15", "description": "First milestone"}]
        )
        db_session.add(goal)
        db_session.commit()
        
        goal_dict = goal.to_dict()
        assert goal_dict["title"] == "Test Goal"
        assert goal_dict["goal_type"] == "mental"
        assert goal_dict["target_value"] == 10.0
        assert goal_dict["current_value"] == 7.0
        assert goal_dict["progress"] == 70.0
        assert goal_dict["milestones"] == [{"date": "2024-01-15", "description": "First milestone"}]


class TestInterventionModel:
    """Test Intervention model functionality."""
    
    def test_intervention_creation(self, db_session, sample_user):
        """Test basic intervention creation."""
        intervention = Intervention(
            user_id=sample_user.id,
            title="Stress Management Workshop",
            description="Workshop to help manage workplace stress",
            intervention_type="workshop",
            priority="high",
            assigned_by=sample_user.id,
            start_date=datetime.now(),
            end_date=datetime.now().replace(hour=datetime.now().hour + 2)
        )
        db_session.add(intervention)
        db_session.commit()
        
        assert intervention.id is not None
        assert intervention.user_id == sample_user.id
        assert intervention.title == "Stress Management Workshop"
        assert intervention.intervention_type == "workshop"
        assert intervention.priority == "high"
        assert intervention.status == "scheduled"
    
    def test_intervention_to_dict(self, db_session, sample_user):
        """Test intervention serialization."""
        intervention = Intervention(
            user_id=sample_user.id,
            title="Test Intervention",
            description="Test intervention description",
            intervention_type="therapy",
            priority="medium",
            status="active",
            effectiveness_score=85.0,
            user_feedback="Very helpful session"
        )
        db_session.add(intervention)
        db_session.commit()
        
        intervention_dict = intervention.to_dict()
        assert intervention_dict["title"] == "Test Intervention"
        assert intervention_dict["intervention_type"] == "therapy"
        assert intervention_dict["priority"] == "medium"
        assert intervention_dict["status"] == "active"
        assert intervention_dict["effectiveness_score"] == 85.0
        assert intervention_dict["user_feedback"] == "Very helpful session"


class TestWellnessProgramModel:
    """Test WellnessProgram model functionality."""
    
    def test_wellness_program_creation(self, db_session, sample_user):
        """Test basic wellness program creation."""
        program = WellnessProgram(
            name="Mental Health Awareness Program",
            description="Comprehensive mental health awareness program",
            program_type="mental_health",
            target_audience="all",
            start_date=date.today(),
            end_date=date.today().replace(month=date.today().month + 3),
            max_participants=100,
            current_participants=25,
            budget=5000.0,
            created_by=sample_user.id
        )
        db_session.add(program)
        db_session.commit()
        
        assert program.id is not None
        assert program.name == "Mental Health Awareness Program"
        assert program.program_type == "mental_health"
        assert program.target_audience == "all"
        assert program.max_participants == 100
        assert program.current_participants == 25
        assert program.budget == 5000.0
        assert program.is_active is True
    
    def test_wellness_program_to_dict(self, db_session, sample_user):
        """Test wellness program serialization."""
        program = WellnessProgram(
            name="Test Program",
            description="Test program description",
            program_type="physical",
            target_audience="managers",
            start_date=date.today(),
            max_participants=50,
            current_participants=10,
            success_metrics={"participation_rate": 0.8, "satisfaction_score": 4.2},
            budget=2500.0,
            created_by=sample_user.id
        )
        db_session.add(program)
        db_session.commit()
        
        program_dict = program.to_dict()
        assert program_dict["name"] == "Test Program"
        assert program_dict["program_type"] == "physical"
        assert program_dict["target_audience"] == "managers"
        assert program_dict["max_participants"] == 50
        assert program_dict["current_participants"] == 10
        assert program_dict["success_metrics"] == {"participation_rate": 0.8, "satisfaction_score": 4.2}
        assert program_dict["budget"] == 2500.0


class TestAnalyticsReportModel:
    """Test AnalyticsReport model functionality."""
    
    def test_analytics_report_creation(self, db_session, sample_user):
        """Test basic analytics report creation."""
        report = AnalyticsReport(
            report_type="wellness_trends",
            title="Monthly Wellness Trends Report",
            description="Analysis of wellness trends for the past month",
            data_period="monthly",
            start_date=datetime.now().replace(day=1),
            end_date=datetime.now(),
            metrics={"average_mood": 7.2, "stress_level": 5.8},
            insights=["Mood has improved by 15%", "Stress levels are decreasing"],
            recommendations=["Continue current wellness programs", "Consider additional stress management resources"],
            generated_by=sample_user.id,
            is_public=False
        )
        db_session.add(report)
        db_session.commit()
        
        assert report.id is not None
        assert report.report_type == "wellness_trends"
        assert report.title == "Monthly Wellness Trends Report"
        assert report.data_period == "monthly"
        assert report.metrics == {"average_mood": 7.2, "stress_level": 5.8}
        assert len(report.insights) == 2
        assert len(report.recommendations) == 2
        assert report.is_public is False
    
    def test_analytics_report_to_dict(self, db_session, sample_user):
        """Test analytics report serialization."""
        report = AnalyticsReport(
            report_type="risk_assessment",
            title="Test Report",
            description="Test report description",
            data_period="weekly",
            start_date=datetime.now().replace(day=1),
            end_date=datetime.now(),
            metrics={"risk_score": 0.3},
            insights=["Low risk overall"],
            recommendations=["Continue monitoring"],
            generated_by=sample_user.id,
            is_public=True
        )
        db_session.add(report)
        db_session.commit()
        
        report_dict = report.to_dict()
        assert report_dict["report_type"] == "risk_assessment"
        assert report_dict["title"] == "Test Report"
        assert report_dict["data_period"] == "weekly"
        assert report_dict["metrics"] == {"risk_score": 0.3}
        assert report_dict["is_public"] is True


class TestSystemSettingsModel:
    """Test SystemSettings model functionality."""
    
    def test_system_settings_creation(self, db_session, sample_user):
        """Test basic system settings creation."""
        setting = SystemSettings(
            setting_key="wellness_checkin_frequency",
            setting_value="weekly",
            setting_type="string",
            description="Default frequency for wellness check-ins",
            category="wellness",
            is_public=True,
            updated_by=sample_user.id
        )
        db_session.add(setting)
        db_session.commit()
        
        assert setting.id is not None
        assert setting.setting_key == "wellness_checkin_frequency"
        assert setting.setting_value == "weekly"
        assert setting.setting_type == "string"
        assert setting.category == "wellness"
        assert setting.is_public is True
    
    def test_system_settings_to_dict(self, db_session, sample_user):
        """Test system settings serialization."""
        setting = SystemSettings(
            setting_key="risk_threshold_high",
            setting_value="75",
            setting_type="integer",
            description="High risk threshold percentage",
            category="risk_assessment",
            is_public=False,
            updated_by=sample_user.id
        )
        db_session.add(setting)
        db_session.commit()
        
        setting_dict = setting.to_dict()
        assert setting_dict["setting_key"] == "risk_threshold_high"
        assert setting_dict["setting_value"] == "75"
        assert setting_dict["setting_type"] == "integer"
        assert setting_dict["category"] == "risk_assessment"
        assert setting_dict["is_public"] is False
        assert setting_dict["updated_by"] == sample_user.id


class TestEnumValues:
    """Test enum values and their string representations."""
    
    def test_user_role_enum(self):
        """Test UserRole enum values."""
        assert UserRole.EMPLOYEE.value == "employee"
        assert UserRole.MANAGER.value == "manager"
        assert UserRole.HR.value == "hr"
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.EXECUTIVE.value == "executive"
    
    def test_wellness_entry_type_enum(self):
        """Test WellnessEntryType enum values."""
        assert WellnessEntryType.MOOD.value == "mood"
        assert WellnessEntryType.STRESS.value == "stress"
        assert WellnessEntryType.ENERGY.value == "energy"
        assert WellnessEntryType.SLEEP_QUALITY.value == "sleep_quality"
        assert WellnessEntryType.WORK_LIFE_BALANCE.value == "work_life_balance"
        assert WellnessEntryType.COMPREHENSIVE.value == "comprehensive"
        assert WellnessEntryType.QUICK_CHECK.value == "quick_check"
    
    def test_risk_level_enum(self):
        """Test RiskLevel enum values."""
        assert RiskLevel.LOW.value == "low"
        assert RiskLevel.MEDIUM.value == "medium"
        assert RiskLevel.HIGH.value == "high"
        assert RiskLevel.CRITICAL.value == "critical"
    
    def test_notification_type_enum(self):
        """Test NotificationType enum values."""
        assert NotificationType.INFO.value == "info"
        assert NotificationType.WARNING.value == "warning"
        assert NotificationType.SUCCESS.value == "success"
        assert NotificationType.ERROR.value == "error"
        assert NotificationType.ALERT.value == "alert"
    
    def test_resource_category_enum(self):
        """Test ResourceCategory enum values."""
        assert ResourceCategory.MENTAL_HEALTH.value == "mental_health"
        assert ResourceCategory.PHYSICAL_HEALTH.value == "physical_health"
        assert ResourceCategory.STRESS_MANAGEMENT.value == "stress_management"
        assert ResourceCategory.WORK_LIFE_BALANCE.value == "work_life_balance"
        assert ResourceCategory.MINDFULNESS.value == "mindfulness"
        assert ResourceCategory.EXERCISE.value == "exercise"
        assert ResourceCategory.NUTRITION.value == "nutrition"
        assert ResourceCategory.SLEEP.value == "sleep"
        assert ResourceCategory.RELATIONSHIPS.value == "relationships"
        assert ResourceCategory.CAREER_DEVELOPMENT.value == "career_development"
        assert ResourceCategory.FINANCIAL_WELLNESS.value == "financial_wellness"
        assert ResourceCategory.SOCIAL_WELLNESS.value == "social_wellness"
    
    def test_difficulty_level_enum(self):
        """Test DifficultyLevel enum values."""
        assert DifficultyLevel.BEGINNER.value == "beginner"
        assert DifficultyLevel.INTERMEDIATE.value == "intermediate"
        assert DifficultyLevel.ADVANCED.value == "advanced"
