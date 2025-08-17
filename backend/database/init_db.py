#!/usr/bin/env python3
"""
Database Initialization Script for Enterprise Employee Wellness AI
This script sets up the complete database with all tables, initial data, and configurations.
"""

import os
import sys
import logging
from datetime import datetime, date
from typing import Dict, Any

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import init_db, check_db_connection, get_db_context
from database.schema import (
    User, WellnessEntry, Resource, SystemSettings, Team, TeamMember,
    WellnessProgram, UserRole, ResourceCategory, DifficultyLevel
)
from database.migrations import run_database_setup, get_database_info
from database.repository import user_repo, system_settings_repo
from utils.auth import hash_password

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_data():
    """Create sample data for the application"""
    try:
        with get_db_context() as db:
            # Check if sample data already exists
            if db.query(User).count() > 0:
                logger.info("Sample data already exists, skipping creation")
                return True
            
            logger.info("Creating sample data...")
            
            # Create sample users
            sample_users = [
                {
                    "email": "admin@wellness.ai",
                    "password_hash": hash_password("admin123"),
                    "first_name": "Admin",
                    "last_name": "User",
                    "role": UserRole.ADMIN,
                    "department": "IT",
                    "position": "System Administrator",
                    "company": "Wellness AI Corp",
                    "is_active": True,
                    "is_verified": True,
                    "email_verified_at": datetime.utcnow()
                },
                {
                    "email": "hr@wellness.ai",
                    "password_hash": hash_password("hr123"),
                    "first_name": "Sarah",
                    "last_name": "Johnson",
                    "role": UserRole.HR,
                    "department": "Human Resources",
                    "position": "HR Manager",
                    "company": "Wellness AI Corp",
                    "is_active": True,
                    "is_verified": True,
                    "email_verified_at": datetime.utcnow()
                },
                {
                    "email": "manager@wellness.ai",
                    "password_hash": hash_password("manager123"),
                    "first_name": "Michael",
                    "last_name": "Chen",
                    "role": UserRole.MANAGER,
                    "department": "Engineering",
                    "position": "Engineering Manager",
                    "company": "Wellness AI Corp",
                    "is_active": True,
                    "is_verified": True,
                    "email_verified_at": datetime.utcnow()
                },
                {
                    "email": "employee@wellness.ai",
                    "password_hash": hash_password("employee123"),
                    "first_name": "Emily",
                    "last_name": "Davis",
                    "role": UserRole.EMPLOYEE,
                    "department": "Engineering",
                    "position": "Software Engineer",
                    "company": "Wellness AI Corp",
                    "manager_id": None,  # Will be set after user creation
                    "is_active": True,
                    "is_verified": True,
                    "email_verified_at": datetime.utcnow()
                },
                {
                    "email": "executive@wellness.ai",
                    "password_hash": hash_password("executive123"),
                    "first_name": "David",
                    "last_name": "Wilson",
                    "role": UserRole.EXECUTIVE,
                    "department": "Executive",
                    "position": "CEO",
                    "company": "Wellness AI Corp",
                    "is_active": True,
                    "is_verified": True,
                    "email_verified_at": datetime.utcnow()
                }
            ]
            
            created_users = {}
            for user_data in sample_users:
                user = User(**user_data)
                db.add(user)
                db.flush()  # Flush to get the ID
                created_users[user.email] = user.id
            
            # Set manager relationships
            employee_user = db.query(User).filter(User.email == "employee@wellness.ai").first()
            manager_user = db.query(User).filter(User.email == "manager@wellness.ai").first()
            if employee_user and manager_user:
                employee_user.manager_id = manager_user.id
            
            # Create sample teams
            engineering_team = Team(
                name="Engineering Team",
                description="Main engineering team for product development",
                manager_id=created_users["manager@wellness.ai"],
                department="Engineering",
                team_size=5,
                is_active=True
            )
            db.add(engineering_team)
            db.flush()
            
            # Add team members
            team_member = TeamMember(
                team_id=engineering_team.id,
                user_id=created_users["employee@wellness.ai"],
                role="member",
                is_active=True
            )
            db.add(team_member)
            
            # Create sample wellness programs
            wellness_programs = [
                {
                    "name": "Mental Health Awareness Program",
                    "description": "Comprehensive mental health awareness and support program",
                    "program_type": "mental_health",
                    "target_audience": "all",
                    "start_date": date.today(),
                    "end_date": date.today().replace(year=date.today().year + 1),
                    "is_active": True,
                    "max_participants": 100,
                    "current_participants": 0,
                    "budget": 5000.0,
                    "created_by": created_users["hr@wellness.ai"]
                },
                {
                    "name": "Stress Management Workshop",
                    "description": "Workshop on stress management techniques",
                    "program_type": "stress_management",
                    "target_audience": "all",
                    "start_date": date.today(),
                    "end_date": date.today().replace(month=date.today().month + 3),
                    "is_active": True,
                    "max_participants": 50,
                    "current_participants": 0,
                    "budget": 2000.0,
                    "created_by": created_users["hr@wellness.ai"]
                },
                {
                    "name": "Physical Wellness Challenge",
                    "description": "30-day physical wellness challenge",
                    "program_type": "physical_health",
                    "target_audience": "all",
                    "start_date": date.today(),
                    "end_date": date.today().replace(day=date.today().day + 30),
                    "is_active": True,
                    "max_participants": 200,
                    "current_participants": 0,
                    "budget": 3000.0,
                    "created_by": created_users["hr@wellness.ai"]
                }
            ]
            
            for program_data in wellness_programs:
                program = WellnessProgram(**program_data)
                db.add(program)
            
            # Create sample wellness resources
            sample_resources = [
                {
                    "title": "Mindfulness Meditation Guide",
                    "description": "A comprehensive guide to mindfulness meditation practices for beginners",
                    "category": ResourceCategory.MINDFULNESS.value,
                    "difficulty_level": DifficultyLevel.BEGINNER.value,
                    "duration_minutes": 15,
                    "tags": ["meditation", "mindfulness", "beginner", "stress-relief"],
                    "author": "Wellness Team",
                    "rating": 4.5,
                    "review_count": 25
                },
                {
                    "title": "Stress Management Techniques",
                    "description": "Effective stress management techniques for the workplace",
                    "category": ResourceCategory.STRESS_MANAGEMENT.value,
                    "difficulty_level": DifficultyLevel.BEGINNER.value,
                    "duration_minutes": 10,
                    "tags": ["stress", "workplace", "techniques", "management"],
                    "author": "Wellness Team",
                    "rating": 4.2,
                    "review_count": 18
                },
                {
                    "title": "Work-Life Balance Strategies",
                    "description": "Practical strategies for maintaining work-life balance",
                    "category": ResourceCategory.WORK_LIFE_BALANCE.value,
                    "difficulty_level": DifficultyLevel.INTERMEDIATE.value,
                    "duration_minutes": 20,
                    "tags": ["work-life-balance", "strategies", "wellness", "productivity"],
                    "author": "Wellness Team",
                    "rating": 4.0,
                    "review_count": 12
                },
                {
                    "title": "Physical Exercise Routine",
                    "description": "Simple physical exercise routine for office workers",
                    "category": ResourceCategory.EXERCISE.value,
                    "difficulty_level": DifficultyLevel.BEGINNER.value,
                    "duration_minutes": 30,
                    "tags": ["exercise", "physical-health", "office", "routine"],
                    "author": "Wellness Team",
                    "rating": 4.3,
                    "review_count": 15
                },
                {
                    "title": "Nutrition for Mental Health",
                    "description": "Nutrition guide for better mental health and cognitive function",
                    "category": ResourceCategory.NUTRITION.value,
                    "difficulty_level": DifficultyLevel.INTERMEDIATE.value,
                    "duration_minutes": 25,
                    "tags": ["nutrition", "mental-health", "cognitive", "diet"],
                    "author": "Wellness Team",
                    "rating": 4.1,
                    "review_count": 8
                }
            ]
            
            for resource_data in sample_resources:
                resource = Resource(**resource_data)
                db.add(resource)
            
            # Create sample wellness entries
            sample_entries = [
                {
                    "user_id": created_users["employee@wellness.ai"],
                    "entry_type": "comprehensive",
                    "value": 7.5,
                    "description": "Feeling good today, had a productive morning",
                    "mood_score": 8.0,
                    "stress_score": 4.0,
                    "energy_score": 7.5,
                    "sleep_hours": 7.5,
                    "sleep_quality": 8.0,
                    "work_life_balance": 7.0,
                    "social_support": 8.5,
                    "physical_activity": 6.0,
                    "nutrition_quality": 7.0,
                    "productivity_level": 8.0,
                    "tags": ["productive", "good-mood", "balanced"],
                    "created_at": datetime.utcnow()
                },
                {
                    "user_id": created_users["manager@wellness.ai"],
                    "entry_type": "comprehensive",
                    "value": 6.5,
                    "description": "Moderate stress due to project deadlines",
                    "mood_score": 6.0,
                    "stress_score": 7.0,
                    "energy_score": 6.5,
                    "sleep_hours": 6.5,
                    "sleep_quality": 6.0,
                    "work_life_balance": 5.5,
                    "social_support": 7.0,
                    "physical_activity": 5.0,
                    "nutrition_quality": 6.5,
                    "productivity_level": 7.5,
                    "tags": ["stressed", "deadlines", "moderate"],
                    "created_at": datetime.utcnow()
                }
            ]
            
            for entry_data in sample_entries:
                entry = WellnessEntry(**entry_data)
                db.add(entry)
            
            db.commit()
            logger.info("Sample data created successfully")
            return True
            
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        return False


def setup_system_settings():
    """Set up system settings"""
    try:
        logger.info("Setting up system settings...")
        
        settings_data = [
            {
                "setting_key": "wellness_checkin_frequency",
                "setting_value": "weekly",
                "setting_type": "string",
                "description": "Default frequency for wellness check-ins",
                "category": "wellness"
            },
            {
                "setting_key": "risk_threshold_high",
                "setting_value": "75",
                "setting_type": "integer",
                "description": "High risk threshold percentage",
                "category": "risk_assessment"
            },
            {
                "setting_key": "risk_threshold_medium",
                "setting_value": "50",
                "setting_type": "integer",
                "description": "Medium risk threshold percentage",
                "category": "risk_assessment"
            },
            {
                "setting_key": "notification_enabled",
                "setting_value": "true",
                "setting_type": "boolean",
                "description": "Enable system notifications",
                "category": "notifications"
            },
            {
                "setting_key": "privacy_anonymization",
                "setting_value": "true",
                "setting_type": "boolean",
                "description": "Enable data anonymization",
                "category": "privacy"
            },
            {
                "setting_key": "ai_conversation_enabled",
                "setting_value": "true",
                "setting_type": "boolean",
                "description": "Enable AI conversation features",
                "category": "ai_features"
            },
            {
                "setting_key": "analytics_retention_days",
                "setting_value": "365",
                "setting_type": "integer",
                "description": "Number of days to retain analytics data",
                "category": "data_retention"
            },
            {
                "setting_key": "max_team_size",
                "setting_value": "20",
                "setting_type": "integer",
                "description": "Maximum team size for wellness programs",
                "category": "teams"
            },
            {
                "setting_key": "wellness_score_weight_mood",
                "setting_value": "0.25",
                "setting_type": "float",
                "description": "Weight for mood in wellness score calculation",
                "category": "analytics"
            },
            {
                "setting_key": "wellness_score_weight_stress",
                "setting_value": "0.20",
                "setting_type": "float",
                "description": "Weight for stress in wellness score calculation",
                "category": "analytics"
            },
            {
                "setting_key": "wellness_score_weight_energy",
                "setting_value": "0.15",
                "setting_type": "float",
                "description": "Weight for energy in wellness score calculation",
                "category": "analytics"
            },
            {
                "setting_key": "wellness_score_weight_sleep",
                "setting_value": "0.20",
                "setting_type": "float",
                "description": "Weight for sleep in wellness score calculation",
                "category": "analytics"
            },
            {
                "setting_key": "wellness_score_weight_work_life_balance",
                "setting_value": "0.20",
                "setting_type": "float",
                "description": "Weight for work-life balance in wellness score calculation",
                "category": "analytics"
            }
        ]
        
        for setting_data in settings_data:
            existing_setting = system_settings_repo.get_setting(setting_data["setting_key"])
            if not existing_setting:
                system_settings_repo.create(setting_data)
        
        logger.info("System settings configured successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error setting up system settings: {e}")
        return False


def main():
    """Main initialization function"""
    try:
        logger.info("Starting database initialization...")
        
        # Check database connection
        if not check_db_connection():
            logger.error("Database connection failed")
            return False
        
        # Initialize database tables
        logger.info("Initializing database tables...")
        init_db()
        
        # Run database setup (migrations, validation, optimization)
        logger.info("Running database setup...")
        if not run_database_setup():
            logger.error("Database setup failed")
            return False
        
        # Set up system settings
        if not setup_system_settings():
            logger.error("System settings setup failed")
            return False
        
        # Create sample data
        if not create_sample_data():
            logger.error("Sample data creation failed")
            return False
        
        # Get database information
        db_info = get_database_info()
        logger.info("Database initialization completed successfully")
        
        # Print summary
        print("\n" + "="*60)
        print("DATABASE INITIALIZATION SUMMARY")
        print("="*60)
        print(f"Status: {'SUCCESS' if db_info.get('migration_status', {}).get('is_up_to_date') else 'PARTIAL'}")
        print(f"Tables Created: {db_info.get('schema_validation', {}).get('total_existing', 0)}")
        print(f"Migrations Applied: {db_info.get('migration_status', {}).get('applied_count', 0)}")
        print(f"Pending Migrations: {db_info.get('migration_status', {}).get('pending_count', 0)}")
        
        if 'database_stats' in db_info:
            stats = db_info['database_stats']
            print(f"Users: {stats.get('users_count', 0)}")
            print(f"Wellness Entries: {stats.get('wellness_entries_count', 0)}")
            print(f"Resources: {stats.get('resources_count', 0)}")
            print(f"Teams: {stats.get('teams_count', 0)}")
            print(f"Wellness Programs: {stats.get('wellness_programs_count', 0)}")
        
        print("\nSample Users Created:")
        print("- admin@wellness.ai (password: admin123)")
        print("- hr@wellness.ai (password: hr123)")
        print("- manager@wellness.ai (password: manager123)")
        print("- employee@wellness.ai (password: employee123)")
        print("- executive@wellness.ai (password: executive123)")
        
        print("\n" + "="*60)
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
