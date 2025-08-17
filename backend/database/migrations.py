"""
Database Migration Utility - Handle schema changes and versioning
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
import logging

from database.connection import get_db_context, engine
from database.schema import Base

logger = logging.getLogger(__name__)


class MigrationManager:
    """Database migration manager"""
    
    def __init__(self):
        self.migrations_table = "schema_migrations"
        self.migrations_dir = "backend/database/migrations"
        self.ensure_migrations_table()
    
    def ensure_migrations_table(self):
        """Ensure the migrations table exists"""
        try:
            with get_db_context() as db:
                # Check if migrations table exists
                inspector = inspect(engine)
                if self.migrations_table not in inspector.get_table_names():
                    # Create migrations table
                    create_migrations_table = text(f"""
                        CREATE TABLE {self.migrations_table} (
                            id SERIAL PRIMARY KEY,
                            version VARCHAR(255) UNIQUE NOT NULL,
                            name VARCHAR(255) NOT NULL,
                            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            checksum VARCHAR(64),
                            execution_time_ms INTEGER
                        )
                    """)
                    db.execute(create_migrations_table)
                    db.commit()
                    logger.info(f"Created migrations table: {self.migrations_table}")
        except Exception as e:
            logger.error(f"Error ensuring migrations table: {e}")
            raise
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions"""
        try:
            with get_db_context() as db:
                result = db.execute(text(f"SELECT version FROM {self.migrations_table} ORDER BY version"))
                return [row[0] for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Error getting applied migrations: {e}")
            return []
    
    def get_pending_migrations(self) -> List[Dict[str, Any]]:
        """Get list of pending migrations"""
        applied_versions = set(self.get_applied_migrations())
        pending_migrations = []
        
        if not os.path.exists(self.migrations_dir):
            return pending_migrations
        
        for filename in sorted(os.listdir(self.migrations_dir)):
            if filename.endswith('.sql'):
                version = filename.split('_')[0]
                if version not in applied_versions:
                    migration_info = self.parse_migration_file(filename)
                    if migration_info:
                        pending_migrations.append(migration_info)
        
        return pending_migrations
    
    def parse_migration_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """Parse migration file and extract metadata"""
        try:
            filepath = os.path.join(self.migrations_dir, filename)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Extract version and name from filename
            parts = filename.replace('.sql', '').split('_', 1)
            if len(parts) >= 2:
                version = parts[0]
                name = parts[1].replace('_', ' ')
                
                return {
                    'version': version,
                    'name': name,
                    'filename': filename,
                    'filepath': filepath,
                    'content': content
                }
        except Exception as e:
            logger.error(f"Error parsing migration file {filename}: {e}")
        
        return None
    
    def apply_migration(self, migration: Dict[str, Any]) -> bool:
        """Apply a single migration"""
        try:
            start_time = datetime.now()
            
            with get_db_context() as db:
                # Execute migration SQL
                db.execute(text(migration['content']))
                db.commit()
                
                # Record migration
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                checksum = self.calculate_checksum(migration['content'])
                
                insert_migration = text(f"""
                    INSERT INTO {self.migrations_table} 
                    (version, name, checksum, execution_time_ms) 
                    VALUES (:version, :name, :checksum, :execution_time)
                """)
                
                db.execute(insert_migration, {
                    'version': migration['version'],
                    'name': migration['name'],
                    'checksum': checksum,
                    'execution_time': int(execution_time)
                })
                db.commit()
                
                logger.info(f"Applied migration: {migration['version']} - {migration['name']}")
                return True
                
        except Exception as e:
            logger.error(f"Error applying migration {migration['version']}: {e}")
            return False
    
    def calculate_checksum(self, content: str) -> str:
        """Calculate checksum for migration content"""
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()
    
    def run_migrations(self) -> bool:
        """Run all pending migrations"""
        try:
            pending_migrations = self.get_pending_migrations()
            
            if not pending_migrations:
                logger.info("No pending migrations to apply")
                return True
            
            logger.info(f"Found {len(pending_migrations)} pending migrations")
            
            for migration in pending_migrations:
                if not self.apply_migration(migration):
                    logger.error(f"Failed to apply migration: {migration['version']}")
                    return False
            
            logger.info("All migrations applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error running migrations: {e}")
            return False
    
    def rollback_migration(self, version: str) -> bool:
        """Rollback a specific migration"""
        try:
            # This is a simplified rollback - in production you'd want more sophisticated rollback logic
            with get_db_context() as db:
                # Remove migration record
                db.execute(text(f"DELETE FROM {self.migrations_table} WHERE version = :version"), {
                    'version': version
                })
                db.commit()
                
                logger.info(f"Rolled back migration: {version}")
                return True
                
        except Exception as e:
            logger.error(f"Error rolling back migration {version}: {e}")
            return False
    
    def get_migration_status(self) -> Dict[str, Any]:
        """Get migration status information"""
        try:
            applied_migrations = self.get_applied_migrations()
            pending_migrations = self.get_pending_migrations()
            
            return {
                'applied_count': len(applied_migrations),
                'pending_count': len(pending_migrations),
                'applied_migrations': applied_migrations,
                'pending_migrations': [m['version'] for m in pending_migrations],
                'is_up_to_date': len(pending_migrations) == 0
            }
        except Exception as e:
            logger.error(f"Error getting migration status: {e}")
            return {}


class SchemaValidator:
    """Database schema validator"""
    
    def __init__(self):
        self.expected_tables = [
            'users', 'wellness_entries', 'conversations', 'resources',
            'resource_interactions', 'analytics_events', 'risk_assessments',
            'notifications', 'team_analytics', 'compliance_records',
            'wellness_goals', 'interventions', 'teams', 'team_members',
            'wellness_programs', 'program_participants', 'analytics_reports',
            'system_settings', 'schema_migrations'
        ]
    
    def validate_schema(self) -> Dict[str, Any]:
        """Validate current database schema"""
        try:
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            missing_tables = set(self.expected_tables) - set(existing_tables)
            extra_tables = set(existing_tables) - set(self.expected_tables)
            
            validation_result = {
                'is_valid': len(missing_tables) == 0,
                'missing_tables': list(missing_tables),
                'extra_tables': list(extra_tables),
                'total_expected': len(self.expected_tables),
                'total_existing': len(existing_tables),
                'validation_timestamp': datetime.now().isoformat()
            }
            
            if validation_result['is_valid']:
                logger.info("Database schema validation passed")
            else:
                logger.warning(f"Database schema validation failed: {validation_result}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating schema: {e}")
            return {
                'is_valid': False,
                'error': str(e),
                'validation_timestamp': datetime.now().isoformat()
            }
    
    def get_table_info(self) -> Dict[str, Any]:
        """Get detailed information about database tables"""
        try:
            inspector = inspect(engine)
            table_info = {}
            
            for table_name in inspector.get_table_names():
                columns = []
                for column in inspector.get_columns(table_name):
                    columns.append({
                        'name': column['name'],
                        'type': str(column['type']),
                        'nullable': column['nullable'],
                        'default': column['default'],
                        'primary_key': column['primary_key']
                    })
                
                indexes = []
                for index in inspector.get_indexes(table_name):
                    indexes.append({
                        'name': index['name'],
                        'columns': index['column_names'],
                        'unique': index['unique']
                    })
                
                table_info[table_name] = {
                    'columns': columns,
                    'indexes': indexes,
                    'row_count': self.get_table_row_count(table_name)
                }
            
            return table_info
            
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            return {}
    
    def get_table_row_count(self, table_name: str) -> int:
        """Get row count for a specific table"""
        try:
            with get_db_context() as db:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                return result.scalar()
        except Exception as e:
            logger.error(f"Error getting row count for {table_name}: {e}")
            return 0


class DatabaseMaintenance:
    """Database maintenance utilities"""
    
    @staticmethod
    def vacuum_database():
        """Vacuum database to reclaim storage and update statistics"""
        try:
            with get_db_context() as db:
                db.execute(text("VACUUM"))
                db.commit()
                logger.info("Database vacuum completed")
                return True
        except Exception as e:
            logger.error(f"Error vacuuming database: {e}")
            return False
    
    @staticmethod
    def analyze_tables():
        """Analyze tables to update statistics"""
        try:
            with get_db_context() as db:
                db.execute(text("ANALYZE"))
                db.commit()
                logger.info("Database analyze completed")
                return True
        except Exception as e:
            logger.error(f"Error analyzing database: {e}")
            return False
    
    @staticmethod
    def optimize_database():
        """Run database optimization tasks"""
        try:
            # Vacuum database
            if not DatabaseMaintenance.vacuum_database():
                return False
            
            # Analyze tables
            if not DatabaseMaintenance.analyze_tables():
                return False
            
            logger.info("Database optimization completed")
            return True
            
        except Exception as e:
            logger.error(f"Error optimizing database: {e}")
            return False


# Migration manager instance
migration_manager = MigrationManager()
schema_validator = SchemaValidator()
database_maintenance = DatabaseMaintenance()


def run_database_setup():
    """Run complete database setup including migrations and validation"""
    try:
        logger.info("Starting database setup...")
        
        # Run migrations
        if not migration_manager.run_migrations():
            logger.error("Database migrations failed")
            return False
        
        # Validate schema
        validation_result = schema_validator.validate_schema()
        if not validation_result['is_valid']:
            logger.error("Database schema validation failed")
            return False
        
        # Optimize database
        if not database_maintenance.optimize_database():
            logger.warning("Database optimization failed")
        
        logger.info("Database setup completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False


def get_database_info() -> Dict[str, Any]:
    """Get comprehensive database information"""
    try:
        return {
            'migration_status': migration_manager.get_migration_status(),
            'schema_validation': schema_validator.validate_schema(),
            'table_info': schema_validator.get_table_info(),
            'database_stats': get_database_stats()
        }
    except Exception as e:
        logger.error(f"Error getting database info: {e}")
        return {'error': str(e)}


def get_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    try:
        with get_db_context() as db:
            # Get basic stats
            stats = {}
            
            # Table counts
            for table_name in schema_validator.expected_tables:
                try:
                    result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    stats[f"{table_name}_count"] = result.scalar()
                except:
                    stats[f"{table_name}_count"] = 0
            
            # Database size (for PostgreSQL)
            try:
                result = db.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))"))
                stats['database_size'] = result.scalar()
            except:
                stats['database_size'] = 'Unknown'
            
            return stats
            
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {}
