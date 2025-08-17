"""
Database Connection - SQLAlchemy database configuration and session management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

# Database URL configuration
DATABASE_URL = settings.DATABASE_URL

# Engine configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG,  # Enable SQL logging in debug mode
    connect_args={
        "check_same_thread": False
    } if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Database context error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    """
    from database.schema import Base
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def check_db_connection():
    """
    Check database connection
    """
    try:
        with get_db_context() as db:
            db.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def get_db_stats():
    """
    Get database statistics
    """
    try:
        with get_db_context() as db:
            # Get table counts
            from database.schema import User, WellnessEntry, Conversation, Resource
            
            stats = {
                "users": db.query(User).count(),
                "wellness_entries": db.query(WellnessEntry).count(),
                "conversations": db.query(Conversation).count(),
                "resources": db.query(Resource).count(),
            }
            
            return stats
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}


# Database migration utilities
def run_migrations():
    """
    Run database migrations
    """
    try:
        # This would typically use Alembic for migrations
        # For now, we'll just recreate tables
        init_db()
        logger.info("Database migrations completed")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


def backup_database():
    """
    Create database backup
    """
    try:
        if "sqlite" in DATABASE_URL:
            import shutil
            from datetime import datetime
            
            backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(DATABASE_URL.replace("sqlite:///", ""), backup_path)
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
        else:
            logger.warning("Database backup not implemented for this database type")
            return None
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return None
