#!/usr/bin/env python3
"""
Database initialization script for Enterprise Employee Wellness AI.
This script creates initial data including roles, teams, wellness resources, and sample users.
"""

import sys
import os
import logging
from datetime import datetime, timedelta
import uuid
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database.connection import get_db_session, init_database
from database.schema import (
    User, Role, Team, WellnessResource, WellnessEntry, 
    Conversation, RiskAssessment, SystemMetrics
)
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_roles():
    """Create default roles for the system."""
    roles_data = [
        {
            "name": "employee",
            "description": "Regular employee with basic wellness access",
            "permissions": {
                "wellness": ["read", "create"],
                "resources": ["read"],
                "analytics": ["read_own"],
                "admin": []
            }
        },
        {
            "name": "manager",
            "description": "Team manager with team wellness insights",
            "permissions": {
                "wellness": ["read", "create"],
                "resources": ["read"],
                "analytics": ["read_own", "read_team"],
                "admin": []
            }
        },
        {
            "name": "hr",
            "description": "HR professional with organizational insights",
            "permissions": {
                "wellness": ["read", "create"],
                "resources": ["read", "create", "update"],
                "analytics": ["read_own", "read_team", "read_org"],
                "admin": ["users", "teams"]
            }
        },
        {
            "name": "admin",
            "description": "System administrator with full access",
            "permissions": {
                "wellness": ["read", "create", "update", "delete"],
                "resources": ["read", "create", "update", "delete"],
                "analytics": ["read_own", "read_team", "read_org", "read_all"],
                "admin": ["users", "teams", "system", "security"]
            }
        }
    ]
    
    with get_db_session() as db:
        for role_data in roles_data:
            existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                role = Role(
                    name=role_data["name"],
                    description=role_data["description"],
                    permissions=role_data["permissions"]
                )
                db.add(role)
                logger.info(f"Created role: {role_data['name']}")
            else:
                logger.info(f"Role already exists: {role_data['name']}")

def create_teams():
    """Create sample teams for the organization."""
    teams_data = [
        {
            "name": "Engineering",
            "department": "Technology",
            "description": "Software engineering team"
        },
        {
            "name": "Product",
            "department": "Technology",
            "description": "Product management team"
        },
        {
            "name": "Sales",
            "department": "Revenue",
            "description": "Sales and business development team"
        },
        {
            "name": "Marketing",
            "department": "Revenue",
            "description": "Marketing and communications team"
        },
        {
            "name": "HR",
            "department": "People",
            "description": "Human resources team"
        },
        {
            "name": "Finance",
            "department": "Operations",
            "description": "Finance and accounting team"
        }
    ]
    
    with get_db_session() as db:
        for team_data in teams_data:
            existing_team = db.query(Team).filter(Team.name == team_data["name"]).first()
            if not existing_team:
                team = Team(
                    name=team_data["name"],
                    department=team_data["department"],
                    description=team_data["description"]
                )
                db.add(team)
                logger.info(f"Created team: {team_data['name']}")
            else:
                logger.info(f"Team already exists: {team_data['name']}")

def create_sample_users():
    """Create sample users for testing and development."""
    users_data = [
        {
            "external_id": "emp_001",
            "email": "john.doe@company.com",
            "first_name": "John",
            "last_name": "Doe",
            "department": "Technology",
            "position": "Senior Software Engineer",
            "role": "employee",
            "team": "Engineering",
            "hire_date": datetime.now() - timedelta(days=365*2),
            "consent_given": True,
            "consent_date": datetime.now() - timedelta(days=30)
        },
        {
            "external_id": "emp_002",
            "email": "jane.smith@company.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "department": "Technology",
            "position": "Engineering Manager",
            "role": "manager",
            "team": "Engineering",
            "hire_date": datetime.now() - timedelta(days=365*3),
            "consent_given": True,
            "consent_date": datetime.now() - timedelta(days=30)
        },
        {
            "external_id": "emp_003",
            "email": "mike.johnson@company.com",
            "first_name": "Mike",
            "last_name": "Johnson",
            "department": "Revenue",
            "position": "Sales Director",
            "role": "manager",
            "team": "Sales",
            "hire_date": datetime.now() - timedelta(days=365*4),
            "consent_given": True,
            "consent_date": datetime.now() - timedelta(days=30)
        },
        {
            "external_id": "emp_004",
            "email": "sarah.wilson@company.com",
            "first_name": "Sarah",
            "last_name": "Wilson",
            "department": "People",
            "position": "HR Manager",
            "role": "hr",
            "team": "HR",
            "hire_date": datetime.now() - timedelta(days=365*5),
            "consent_given": True,
            "consent_date": datetime.now() - timedelta(days=30)
        },
        {
            "external_id": "admin_001",
            "email": "admin@company.com",
            "first_name": "System",
            "last_name": "Administrator",
            "department": "Technology",
            "position": "System Administrator",
            "role": "admin",
            "team": "Engineering",
            "hire_date": datetime.now() - timedelta(days=365*6),
            "consent_given": True,
            "consent_date": datetime.now() - timedelta(days=30)
        }
    ]
    
    with get_db_session() as db:
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                # Get role
                role = db.query(Role).filter(Role.name == user_data["role"]).first()
                if not role:
                    logger.error(f"Role not found: {user_data['role']}")
                    continue
                
                # Get team
                team = db.query(Team).filter(Team.name == user_data["team"]).first()
                if not team:
                    logger.error(f"Team not found: {user_data['team']}")
                    continue
                
                # Create user
                user = User(
                    external_id=user_data["external_id"],
                    email=user_data["email"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    department=user_data["department"],
                    position=user_data["position"],
                    hire_date=user_data["hire_date"],
                    consent_given=user_data["consent_given"],
                    consent_date=user_data["consent_date"]
                )
                
                # Add role and team
                user.roles.append(role)
                user.teams.append(team)
                
                db.add(user)
                logger.info(f"Created user: {user_data['email']}")
            else:
                logger.info(f"User already exists: {user_data['email']}")

def create_wellness_resources():
    """Create sample wellness resources."""
    resources_data = [
        {
            "title": "5-Minute Breathing Exercise",
            "description": "A quick breathing exercise to reduce stress and anxiety",
            "content": "Find a comfortable position. Close your eyes and take a deep breath in for 4 counts, hold for 4 counts, exhale for 4 counts. Repeat for 5 minutes.",
            "resource_type": "exercise",
            "category": "stress_management",
            "tags": ["breathing", "stress", "quick", "meditation"],
            "difficulty_level": "beginner",
            "duration_minutes": 5
        },
        {
            "title": "Mindful Walking Guide",
            "description": "Learn to practice mindfulness while walking",
            "content": "Take a 10-minute walk outside. Focus on your footsteps, the feeling of the ground beneath you, and the sounds around you. Let thoughts come and go without judgment.",
            "resource_type": "exercise",
            "category": "mindfulness",
            "tags": ["walking", "mindfulness", "outdoor", "meditation"],
            "difficulty_level": "beginner",
            "duration_minutes": 10
        },
        {
            "title": "Work-Life Balance Tips",
            "description": "Practical tips for maintaining work-life balance",
            "content": "Set clear boundaries between work and personal time. Schedule breaks throughout the day. Learn to say no to non-essential tasks. Prioritize self-care activities.",
            "resource_type": "article",
            "category": "work_life_balance",
            "tags": ["balance", "boundaries", "self-care", "productivity"],
            "difficulty_level": "intermediate",
            "duration_minutes": 15
        },
        {
            "title": "Progressive Muscle Relaxation",
            "description": "A technique to reduce physical tension and stress",
            "content": "Starting from your toes, tense each muscle group for 5 seconds, then relax for 10 seconds. Work your way up through your body to your head.",
            "resource_type": "exercise",
            "category": "stress_management",
            "tags": ["relaxation", "muscle", "stress", "tension"],
            "difficulty_level": "beginner",
            "duration_minutes": 15
        },
        {
            "title": "Gratitude Journaling",
            "description": "Learn to practice gratitude through daily journaling",
            "content": "Write down 3 things you're grateful for each day. Reflect on why they matter to you. This practice can improve mood and overall well-being.",
            "resource_type": "exercise",
            "category": "positive_psychology",
            "tags": ["gratitude", "journaling", "positivity", "reflection"],
            "difficulty_level": "beginner",
            "duration_minutes": 10
        },
        {
            "title": "Digital Detox Challenge",
            "description": "A 7-day challenge to reduce screen time and improve well-being",
            "content": "Set specific times to check email and social media. Turn off notifications. Spend more time on offline activities. Notice how you feel after reducing screen time.",
            "resource_type": "challenge",
            "category": "digital_wellness",
            "tags": ["digital", "screen_time", "challenge", "wellness"],
            "difficulty_level": "intermediate",
            "duration_minutes": 0
        },
        {
            "title": "Mindful Eating Guide",
            "description": "Learn to eat mindfully and improve your relationship with food",
            "content": "Eat without distractions. Pay attention to the taste, texture, and smell of your food. Eat slowly and stop when you're satisfied, not full.",
            "resource_type": "article",
            "category": "nutrition",
            "tags": ["eating", "mindfulness", "nutrition", "health"],
            "difficulty_level": "beginner",
            "duration_minutes": 20
        },
        {
            "title": "Quick Desk Stretches",
            "description": "Simple stretches you can do at your desk to reduce tension",
            "content": "Neck rolls, shoulder shrugs, wrist stretches, and seated twists. Do each stretch for 30 seconds. Repeat throughout the day.",
            "resource_type": "exercise",
            "category": "physical_wellness",
            "tags": ["stretching", "desk", "physical", "tension"],
            "difficulty_level": "beginner",
            "duration_minutes": 5
        }
    ]
    
    with get_db_session() as db:
        for resource_data in resources_data:
            existing_resource = db.query(WellnessResource).filter(
                WellnessResource.title == resource_data["title"]
            ).first()
            
            if not existing_resource:
                resource = WellnessResource(
                    title=resource_data["title"],
                    description=resource_data["description"],
                    content=resource_data["content"],
                    resource_type=resource_data["resource_type"],
                    category=resource_data["category"],
                    tags=resource_data["tags"],
                    difficulty_level=resource_data["difficulty_level"],
                    duration_minutes=resource_data["duration_minutes"]
                )
                db.add(resource)
                logger.info(f"Created resource: {resource_data['title']}")
            else:
                logger.info(f"Resource already exists: {resource_data['title']}")

def create_sample_wellness_entries():
    """Create sample wellness entries for testing."""
    with get_db_session() as db:
        users = db.query(User).limit(3).all()
        
        entry_types = ["mood", "stress", "energy", "sleep_quality"]
        
        for user in users:
            # Create entries for the last 30 days
            for i in range(30):
                date = datetime.now() - timedelta(days=i)
                
                for entry_type in entry_types:
                    # Generate realistic values
                    if entry_type == "mood":
                        value = 6 + (i % 3)  # 6-8 range
                    elif entry_type == "stress":
                        value = 4 + (i % 4)  # 4-7 range
                    elif entry_type == "energy":
                        value = 5 + (i % 4)  # 5-8 range
                    else:  # sleep_quality
                        value = 6 + (i % 3)  # 6-8 range
                    
                    entry = WellnessEntry(
                        user_id=user.id,
                        entry_type=entry_type,
                        value=value,
                        description=f"Sample {entry_type} entry",
                        tags=["sample", "test"],
                        created_at=date
                    )
                    db.add(entry)
            
            logger.info(f"Created wellness entries for user: {user.email}")

def create_sample_conversations():
    """Create sample conversations for testing."""
    conversation_data = [
        {
            "message": "I'm feeling a bit stressed today with all the deadlines",
            "response": "I understand that deadlines can be overwhelming. Let's take a moment to breathe. Would you like to try a quick 5-minute breathing exercise?",
            "sentiment_score": -0.3,
            "risk_level": 0.2
        },
        {
            "message": "I had a great workout this morning and feel energized",
            "response": "That's wonderful! Exercise is such a great way to boost your mood and energy. Keep up the great work!",
            "sentiment_score": 0.8,
            "risk_level": 0.0
        },
        {
            "message": "I'm having trouble sleeping lately",
            "response": "Sleep issues can really impact your well-being. Let's explore some strategies. Have you tried establishing a consistent bedtime routine?",
            "sentiment_score": -0.2,
            "risk_level": 0.3
        }
    ]
    
    with get_db_session() as db:
        users = db.query(User).limit(2).all()
        
        for user in users:
            for i, conv_data in enumerate(conversation_data):
                conversation = Conversation(
                    user_id=user.id,
                    session_id=str(uuid.uuid4()),
                    message=conv_data["message"],
                    response=conv_data["response"],
                    sentiment_score=conv_data["sentiment_score"],
                    risk_level=conv_data["risk_level"],
                    agent_type="wellness_companion",
                    workflow_type="employee_conversation",
                    created_at=datetime.now() - timedelta(days=i)
                )
                db.add(conversation)
            
            logger.info(f"Created conversations for user: {user.email}")

def create_sample_system_metrics():
    """Create sample system metrics for monitoring."""
    metrics_data = [
        {"name": "active_users", "value": 150, "unit": "users"},
        {"name": "conversations_per_day", "value": 45, "unit": "conversations"},
        {"name": "avg_response_time", "value": 2.3, "unit": "seconds"},
        {"name": "system_uptime", "value": 99.8, "unit": "percent"},
        {"name": "memory_usage", "value": 65.2, "unit": "percent"},
        {"name": "cpu_usage", "value": 42.1, "unit": "percent"}
    ]
    
    with get_db_session() as db:
        for metric_data in metrics_data:
            metric = SystemMetrics(
                metric_name=metric_data["name"],
                metric_value=metric_data["value"],
                metric_unit=metric_data["unit"],
                tags={"environment": "development"}
            )
            db.add(metric)
        
        logger.info("Created sample system metrics")

def main():
    """Main function to initialize all data."""
    logger.info("Starting database initialization...")
    
    try:
        # Initialize database tables
        init_database()
        logger.info("Database tables created successfully")
        
        # Create initial data
        create_roles()
        create_teams()
        create_sample_users()
        create_wellness_resources()
        create_sample_wellness_entries()
        create_sample_conversations()
        create_sample_system_metrics()
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
