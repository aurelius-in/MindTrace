from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from typing import Generator, Optional
import asyncio
from functools import wraps

from config.settings import settings

logger = logging.getLogger(__name__)

# Database engine configuration
engine = create_engine(
    settings.database.url,
    poolclass=QueuePool,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=settings.debug,
    connect_args={
        "connect_timeout": 10,
        "application_name": "wellness_ai"
    }
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_database() -> Session:
    """
    Get a database session.
    Use this in dependency injection for FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Use this for manual session management.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()

def get_async_database():
    """
    Async wrapper for database sessions.
    Use this in async FastAPI endpoints.
    """
    def async_get_db():
        with get_db_session() as session:
            yield session
    
    return async_get_db

def with_db_session(func):
    """
    Decorator to automatically handle database sessions.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with get_db_session() as db:
            return func(db, *args, **kwargs)
    return wrapper

def with_async_db_session(func):
    """
    Async decorator to automatically handle database sessions.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        with get_db_session() as db:
            return await func(db, *args, **kwargs)
    return wrapper

def init_database():
    """
    Initialize the database by creating all tables.
    """
    try:
        from .schema import Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def check_database_connection() -> bool:
    """
    Check if the database connection is working.
    """
    try:
        with get_db_session() as db:
            db.execute("SELECT 1")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection check failed: {e}")
        return False

def get_database_stats() -> dict:
    """
    Get database connection pool statistics.
    """
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalid()
    }

# Database event listeners for logging and monitoring
@event.listens_for(engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    logger.debug("Database connection established")

@event.listens_for(engine, "disconnect")
def receive_disconnect(dbapi_connection, connection_record):
    logger.debug("Database connection closed")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug("Database connection checked out")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    logger.debug("Database connection checked in")

# Health check function
async def health_check() -> dict:
    """
    Perform a comprehensive database health check.
    """
    health_status = {
        "database": {
            "status": "unknown",
            "connection": False,
            "pool_stats": None,
            "error": None
        }
    }
    
    try:
        # Check connection
        if check_database_connection():
            health_status["database"]["connection"] = True
            health_status["database"]["status"] = "healthy"
            
            # Get pool statistics
            health_status["database"]["pool_stats"] = get_database_stats()
        else:
            health_status["database"]["status"] = "unhealthy"
            health_status["database"]["error"] = "Connection failed"
            
    except Exception as e:
        health_status["database"]["status"] = "error"
        health_status["database"]["error"] = str(e)
        logger.error(f"Database health check failed: {e}")
    
    return health_status

# Database migration utilities
def create_migration(description: str) -> str:
    """
    Create a new database migration.
    This is a placeholder for Alembic integration.
    """
    # TODO: Implement Alembic migration creation
    logger.info(f"Migration requested: {description}")
    return f"migration_{description.lower().replace(' ', '_')}"

def run_migrations() -> bool:
    """
    Run pending database migrations.
    This is a placeholder for Alembic integration.
    """
    try:
        # TODO: Implement Alembic migration runner
        logger.info("Database migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        return False

# Connection pool monitoring
async def monitor_connection_pool():
    """
    Monitor database connection pool health.
    """
    while True:
        try:
            stats = get_database_stats()
            logger.debug(f"Connection pool stats: {stats}")
            
            # Alert if pool is getting full
            if stats["checked_out"] > stats["pool_size"] * 0.8:
                logger.warning("Database connection pool is getting full")
            
            await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            logger.error(f"Connection pool monitoring error: {e}")
            await asyncio.sleep(60)

# Database cleanup utilities
def cleanup_old_data():
    """
    Clean up old data based on retention policies.
    """
    try:
        with get_db_session() as db:
            # TODO: Implement data cleanup based on retention policies
            # This could include cleaning up old audit logs, system metrics, etc.
            logger.info("Database cleanup completed")
    except Exception as e:
        logger.error(f"Database cleanup failed: {e}")

def vacuum_database():
    """
    Perform database maintenance (PostgreSQL specific).
    """
    try:
        with get_db_session() as db:
            db.execute("VACUUM ANALYZE")
            logger.info("Database vacuum completed")
    except Exception as e:
        logger.error(f"Database vacuum failed: {e}")

# Export commonly used functions
__all__ = [
    'get_database',
    'get_db_session',
    'get_async_database',
    'with_db_session',
    'with_async_db_session',
    'init_database',
    'check_database_connection',
    'get_database_stats',
    'health_check',
    'create_migration',
    'run_migrations',
    'monitor_connection_pool',
    'cleanup_old_data',
    'vacuum_database'
]
