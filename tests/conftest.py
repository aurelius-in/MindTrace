"""
Pytest configuration and fixtures for Enterprise Employee Wellness AI tests
"""
import pytest
import asyncio
from typing import Generator, Dict, Any
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
import sys
import tempfile
import shutil
from datetime import datetime, timedelta
import uuid

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from database.connection import get_db_context
from database.schema import Base, User, WellnessEntry, Resource, Team, Notification
from utils.auth import hash_password, create_access_token
from agents.orchestrator import AgentOrchestrator


# Test database configuration
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db():
    """Create test database and tables."""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(test_db):
    """Create a new database session for a test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create a test client with database session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db_context] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": "employee",
        "department": "Engineering",
        "position": "Software Engineer",
        "company": "Test Corp",
        "phone": "+1234567890",
        "timezone": "UTC",
        "language": "en"
    }


@pytest.fixture
def sample_user(db_session, sample_user_data):
    """Create a sample user in the database."""
    user = User(
        id=str(uuid.uuid4()),
        email=sample_user_data["email"],
        password_hash=hash_password(sample_user_data["password"]),
        first_name=sample_user_data["first_name"],
        last_name=sample_user_data["last_name"],
        role=sample_user_data["role"],
        department=sample_user_data["department"],
        position=sample_user_data["position"],
        company=sample_user_data["company"],
        phone=sample_user_data["phone"],
        timezone=sample_user_data["timezone"],
        language=sample_user_data["language"],
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def authenticated_client(client, sample_user):
    """Create an authenticated test client."""
    access_token = create_access_token(data={"sub": sample_user.email})
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest.fixture
def sample_wellness_entry_data() -> Dict[str, Any]:
    """Sample wellness entry data for testing."""
    return {
        "entry_type": "comprehensive",
        "value": 7.5,
        "description": "Feeling good today",
        "mood_score": 8.0,
        "stress_score": 4.0,
        "energy_score": 7.0,
        "sleep_hours": 7.5,
        "sleep_quality": 8.0,
        "work_life_balance": 7.0,
        "social_support": 8.0,
        "physical_activity": 6.0,
        "nutrition_quality": 7.0,
        "productivity_level": 8.0,
        "tags": ["positive", "productive"],
        "factors": {"workload": "moderate", "sleep": "good"},
        "recommendations": ["Continue current routine", "Consider more exercise"],
        "risk_indicators": [],
        "is_anonymous": False
    }


@pytest.fixture
def sample_wellness_entry(db_session, sample_user, sample_wellness_entry_data):
    """Create a sample wellness entry in the database."""
    entry = WellnessEntry(
        id=str(uuid.uuid4()),
        user_id=sample_user.id,
        **sample_wellness_entry_data
    )
    db_session.add(entry)
    db_session.commit()
    db_session.refresh(entry)
    return entry


@pytest.fixture
def sample_resource_data() -> Dict[str, Any]:
    """Sample resource data for testing."""
    return {
        "title": "Stress Management Techniques",
        "description": "Learn effective stress management techniques for the workplace",
        "category": "stress_management",
        "difficulty_level": "beginner",
        "duration_minutes": 15,
        "tags": ["stress", "workplace", "techniques"],
        "author": "Wellness Team",
        "content_url": "https://example.com/stress-management",
        "thumbnail_url": "https://example.com/thumbnail.jpg",
        "is_active": True,
        "view_count": 0,
        "rating": 0.0,
        "rating_count": 0
    }


@pytest.fixture
def sample_resource(db_session, sample_resource_data):
    """Create a sample resource in the database."""
    resource = Resource(
        id=str(uuid.uuid4()),
        **sample_resource_data
    )
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)
    return resource


@pytest.fixture
def sample_team_data() -> Dict[str, Any]:
    """Sample team data for testing."""
    return {
        "name": "Engineering Team",
        "description": "Software engineering team",
        "department": "Engineering",
        "team_size": 5,
        "is_active": True,
        "wellness_score": 7.5,
        "metadata": {"location": "San Francisco", "timezone": "PST"}
    }


@pytest.fixture
def sample_team(db_session, sample_user, sample_team_data):
    """Create a sample team in the database."""
    team = Team(
        id=str(uuid.uuid4()),
        manager_id=sample_user.id,
        **sample_team_data
    )
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    return team


@pytest.fixture
def sample_notification_data() -> Dict[str, Any]:
    """Sample notification data for testing."""
    return {
        "title": "Wellness Check-in Reminder",
        "message": "Don't forget to complete your weekly wellness check-in",
        "notification_type": "info",
        "priority": "medium",
        "is_read": False,
        "metadata": {"reminder_type": "weekly_checkin"}
    }


@pytest.fixture
def sample_notification(db_session, sample_user, sample_notification_data):
    """Create a sample notification in the database."""
    notification = Notification(
        id=str(uuid.uuid4()),
        user_id=sample_user.id,
        **sample_notification_data
    )
    db_session.add(notification)
    db_session.commit()
    db_session.refresh(notification)
    return notification


@pytest.fixture
def mock_agent_orchestrator():
    """Mock agent orchestrator for testing."""
    with patch('agents.orchestrator.AgentOrchestrator') as mock:
        orchestrator_instance = Mock()
        mock.return_value = orchestrator_instance
        yield orchestrator_instance


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch('openai.OpenAI') as mock:
        client_instance = Mock()
        mock.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_redis_client():
    """Mock Redis client for testing."""
    with patch('redis.Redis') as mock:
        redis_instance = Mock()
        mock.return_value = redis_instance
        yield redis_instance


@pytest.fixture
def mock_prometheus_metrics():
    """Mock Prometheus metrics for testing."""
    with patch('prometheus_client.Counter') as mock_counter, \
         patch('prometheus_client.Histogram') as mock_histogram, \
         patch('prometheus_client.Gauge') as mock_gauge:
        
        counter_instance = Mock()
        histogram_instance = Mock()
        gauge_instance = Mock()
        
        mock_counter.return_value = counter_instance
        mock_histogram.return_value = histogram_instance
        mock_gauge.return_value = gauge_instance
        
        yield {
            'counter': counter_instance,
            'histogram': histogram_instance,
            'gauge': gauge_instance
        }


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        yield f.name
    if os.path.exists(f.name):
        os.unlink(f.name)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


# Test data generators
@pytest.fixture
def generate_users(db_session, sample_user_data):
    """Generate multiple users for testing."""
    def _generate_users(count: int = 5):
        users = []
        for i in range(count):
            user_data = sample_user_data.copy()
            user_data["email"] = f"user{i}@example.com"
            user_data["first_name"] = f"User{i}"
            user_data["last_name"] = f"Test{i}"
            
            user = User(
                id=str(uuid.uuid4()),
                password_hash=hash_password(user_data["password"]),
                **{k: v for k, v in user_data.items() if k != "password"}
            )
            db_session.add(user)
            users.append(user)
        
        db_session.commit()
        return users
    return _generate_users


@pytest.fixture
def generate_wellness_entries(db_session, sample_user, sample_wellness_entry_data):
    """Generate multiple wellness entries for testing."""
    def _generate_entries(count: int = 10):
        entries = []
        for i in range(count):
            entry_data = sample_wellness_entry_data.copy()
            entry_data["value"] = 5.0 + (i % 5)  # Vary values
            entry_data["mood_score"] = 6.0 + (i % 4)
            entry_data["created_at"] = datetime.now() - timedelta(days=i)
            
            entry = WellnessEntry(
                id=str(uuid.uuid4()),
                user_id=sample_user.id,
                **entry_data
            )
            db_session.add(entry)
            entries.append(entry)
        
        db_session.commit()
        return entries
    return _generate_entries


# Performance testing fixtures
@pytest.fixture
def performance_test_data(db_session, generate_users, generate_wellness_entries):
    """Generate large datasets for performance testing."""
    def _generate_performance_data(user_count: int = 100, entry_count: int = 1000):
        users = generate_users(user_count)
        entries = []
        
        for user in users:
            user_entries = generate_wellness_entries(entry_count // user_count)
            entries.extend(user_entries)
        
        return users, entries
    return _generate_performance_data


# Integration testing fixtures
@pytest.fixture
def integration_test_setup(db_session, sample_user, sample_team, sample_resource):
    """Setup complete integration test environment."""
    return {
        "user": sample_user,
        "team": sample_team,
        "resource": sample_resource,
        "session": db_session
    }


# Security testing fixtures
@pytest.fixture
def security_test_data():
    """Data for security testing."""
    return {
        "malicious_input": "<script>alert('xss')</script>",
        "sql_injection": "'; DROP TABLE users; --",
        "large_payload": "A" * 1000000,  # 1MB payload
        "invalid_token": "invalid.jwt.token",
        "expired_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    }


# Configuration for different test types
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as an API test"
    )
    config.addinivalue_line(
        "markers", "database: mark test as a database test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as a security test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        if "test_api_" in item.nodeid:
            item.add_marker(pytest.mark.api)
        elif "test_database_" in item.nodeid:
            item.add_marker(pytest.mark.database)
        elif "test_security_" in item.nodeid:
            item.add_marker(pytest.mark.security)
        elif "test_performance_" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        elif "test_integration_" in item.nodeid:
            item.add_marker(pytest.mark.integration)
