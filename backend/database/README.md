# Database Layer - Enterprise Employee Wellness AI

This directory contains the complete database layer for the Enterprise Employee Wellness AI application, including models, migrations, repositories, and utilities.

## 📁 Directory Structure

```
backend/database/
├── README.md                 # This documentation file
├── schema.py                 # SQLAlchemy models and enums
├── connection.py             # Database connection and session management
├── repository.py             # Repository pattern for data access
├── migrations.py             # Migration management utilities
├── init_db.py                # Database initialization script
└── migrations/               # SQL migration files
    └── 001_initial_schema.sql # Initial database schema
```

## 🏗️ Architecture Overview

The database layer follows a clean architecture pattern with the following components:

### 1. **Models (schema.py)**
- SQLAlchemy ORM models with comprehensive relationships
- Enum classes for type safety
- JSON fields for flexible data storage
- Automatic timestamps and UUID primary keys

### 2. **Connection Management (connection.py)**
- Database engine configuration
- Session management with context managers
- Connection pooling and optimization
- Database initialization and seeding

### 3. **Repository Pattern (repository.py)**
- Clean data access layer
- Type-safe operations
- Error handling and logging
- Specialized repositories for each model

### 4. **Migration System (migrations.py)**
- Version-controlled schema changes
- Migration tracking and rollback
- Schema validation
- Database maintenance utilities

## 🗄️ Database Models

### Core Models

#### User
```python
class User(Base):
    # Authentication & Profile
    email, password_hash, first_name, last_name
    role, department, position, manager_id
    company, phone, avatar_url, timezone, language
    hire_date, is_active, is_verified
    
    # Activity Tracking
    last_login, last_activity
    
    # Preferences & Profile
    preferences, wellness_profile
```

#### WellnessEntry
```python
class WellnessEntry(Base):
    # Basic Entry
    user_id, entry_type, value, description
    
    # Detailed Metrics
    mood_score, stress_score, energy_score
    sleep_hours, sleep_quality, work_life_balance
    social_support, physical_activity, nutrition_quality
    productivity_level
    
    # Analysis & Recommendations
    tags, factors, recommendations, risk_indicators
    is_anonymous
```

#### Resource
```python
class Resource(Base):
    # Content Information
    title, description, category, difficulty_level
    duration_minutes, content_url, author
    
    # Engagement Metrics
    rating, review_count, tags
    
    # Management
    is_active, metadata
```

### Supporting Models

- **Conversation**: AI chat interactions with sentiment analysis
- **ResourceInteraction**: User interactions with wellness resources
- **RiskAssessment**: Risk evaluation and intervention tracking
- **Notification**: User notifications and alerts
- **TeamAnalytics**: Team-level wellness insights
- **ComplianceRecord**: Audit trails and compliance tracking

### Advanced Models

- **WellnessGoal**: User wellness objectives and progress tracking
- **Intervention**: Wellness interventions and programs
- **Team/TeamMember**: Team management and structure
- **WellnessProgram**: Organizational wellness initiatives
- **ProgramParticipant**: Program participation tracking
- **AnalyticsReport**: Generated analytics and insights
- **SystemSettings**: Application configuration

## 🔧 Database Setup

### 1. **Initial Setup**
```bash
# Run the database initialization script
cd backend
python database/init_db.py
```

### 2. **Manual Setup**
```python
from database.connection import init_db, check_db_connection
from database.migrations import run_database_setup

# Check connection
if check_db_connection():
    # Initialize tables
    init_db()
    
    # Run migrations and validation
    run_database_setup()
```

### 3. **Environment Configuration**
```bash
# Required environment variables
DATABASE_URL=postgresql://user:password@localhost/wellness_db
# or for SQLite
DATABASE_URL=sqlite:///./wellness.db
```

## 📊 Repository Pattern Usage

### Basic Operations
```python
from database.repository import user_repo, wellness_entry_repo

# Create
user_data = {
    "email": "user@example.com",
    "password_hash": "hashed_password",
    "first_name": "John",
    "last_name": "Doe"
}
user = user_repo.create(user_data)

# Read
user = user_repo.get_by_id(user_id)
user_by_email = user_repo.get_by_email("user@example.com")

# Update
user_repo.update(user_id, {"last_name": "Smith"})

# Delete
user_repo.delete(user_id)
```

### Specialized Operations
```python
# Get wellness entries for a user
entries = wellness_entry_repo.get_user_entries(user_id, limit=10)

# Get department averages
averages = wellness_entry_repo.get_department_averages("Engineering", days=30)

# Get trend data
trends = wellness_entry_repo.get_trend_data(user_id, "mood", days=90)
```

## 🔄 Migration System

### Running Migrations
```python
from database.migrations import migration_manager

# Run all pending migrations
migration_manager.run_migrations()

# Check migration status
status = migration_manager.get_migration_status()
print(f"Applied: {status['applied_count']}, Pending: {status['pending_count']}")
```

### Creating New Migrations
1. Create a new SQL file in `migrations/` directory
2. Follow naming convention: `{version}_{description}.sql`
3. Include both up and down migrations if needed

Example:
```sql
-- 002_add_user_preferences.sql
ALTER TABLE users ADD COLUMN preferences JSON DEFAULT '{}';
```

## 📈 Analytics and Reporting

### Wellness Score Calculation
```python
# Get user wellness score components
entries = wellness_entry_repo.get_entries_by_type(user_id, "comprehensive", days=30)

# Calculate weighted score
weights = {
    "mood": 0.25,
    "stress": 0.20,
    "energy": 0.15,
    "sleep": 0.20,
    "work_life_balance": 0.20
}
```

### Risk Assessment
```python
from database.repository import risk_assessment_repo

# Get high-risk users
high_risk = risk_assessment_repo.get_high_risk_users()

# Get department risk summary
summary = risk_assessment_repo.get_department_risk_summary("Engineering")
```

## 🔒 Security and Privacy

### Data Anonymization
- Anonymous wellness check-ins
- Privacy controls in user preferences
- Audit trails for data access

### Compliance Features
- GDPR compliance tracking
- Data retention policies
- Consent management
- Audit logging

## 🚀 Performance Optimization

### Indexes
- Primary keys on all tables
- Foreign key indexes
- Composite indexes for common queries
- Full-text search indexes for resources

### Query Optimization
- Repository pattern for efficient queries
- Connection pooling
- Prepared statements
- Query result caching

### Database Maintenance
```python
from database.migrations import database_maintenance

# Optimize database
database_maintenance.optimize_database()

# Vacuum database
database_maintenance.vacuum_database()
```

## 📋 Sample Data

The initialization script creates sample data including:

### Users
- **Admin**: admin@wellness.ai (admin123)
- **HR Manager**: hr@wellness.ai (hr123)
- **Engineering Manager**: manager@wellness.ai (manager123)
- **Employee**: employee@wellness.ai (employee123)
- **Executive**: executive@wellness.ai (executive123)

### Sample Content
- 5 wellness resources across different categories
- 3 wellness programs
- Sample wellness entries
- Team structures
- System settings

## 🛠️ Development Tools

### Database Information
```python
from database.migrations import get_database_info

# Get comprehensive database information
info = get_database_info()
print(f"Tables: {info['schema_validation']['total_existing']}")
print(f"Users: {info['database_stats']['users_count']}")
```

### Schema Validation
```python
from database.migrations import schema_validator

# Validate schema
validation = schema_validator.validate_schema()
if validation['is_valid']:
    print("Schema is valid")
else:
    print(f"Missing tables: {validation['missing_tables']}")
```

## 🔧 Configuration

### Database Settings
```python
# In config/settings.py
DATABASE_URL = "postgresql://user:password@localhost/wellness_db"
DATABASE_POOL_SIZE = 10
DATABASE_MAX_OVERFLOW = 20
DATABASE_POOL_TIMEOUT = 30
```

### System Settings
```python
from database.repository import system_settings_repo

# Get wellness check-in frequency
frequency = system_settings_repo.get_setting("wellness_checkin_frequency")

# Update risk threshold
system_settings_repo.update_setting("risk_threshold_high", "80")
```

## 📚 Best Practices

### 1. **Use Repository Pattern**
- Always use repositories for data access
- Don't access models directly from services
- Use type hints for better code quality

### 2. **Handle Transactions**
```python
from database.connection import get_db_context

with get_db_context() as db:
    # Multiple operations in single transaction
    user_repo.create(user_data)
    wellness_entry_repo.create(entry_data)
    # Transaction automatically committed
```

### 3. **Error Handling**
```python
try:
    user = user_repo.get_by_email(email)
    if not user:
        raise ValueError("User not found")
except Exception as e:
    logger.error(f"Database error: {e}")
    # Handle appropriately
```

### 4. **Performance Considerations**
- Use appropriate indexes
- Limit query results with pagination
- Use eager loading for relationships
- Cache frequently accessed data

## 🐛 Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check DATABASE_URL configuration
   - Verify database server is running
   - Check network connectivity

2. **Migration Issues**
   - Ensure migrations table exists
   - Check migration file syntax
   - Verify database permissions

3. **Performance Issues**
   - Check query execution plans
   - Verify indexes are being used
   - Monitor connection pool usage

### Debug Commands
```python
# Check database connection
from database.connection import check_db_connection
check_db_connection()

# Get database stats
from database.migrations import get_database_stats
stats = get_database_stats()

# Validate schema
from database.migrations import schema_validator
validation = schema_validator.validate_schema()
```

## 📖 Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Database Design Best Practices](https://www.postgresql.org/docs/current/ddl.html)
- [Performance Tuning Guide](https://www.postgresql.org/docs/current/performance.html)

---

This database layer provides a robust, scalable foundation for the Enterprise Employee Wellness AI application with comprehensive features for data management, analytics, and compliance.
