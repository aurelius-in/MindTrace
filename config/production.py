"""
Production Configuration - Secure defaults for production deployment
"""

import os
import secrets
from typing import List
from pydantic import BaseSettings, validator, Field


class ProductionSettings(BaseSettings):
    """Production-specific settings with security validation"""
    
    # Application
    APP_NAME: str = "Enterprise Employee Wellness AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = Field(default=4, ge=1, le=16)
    
    # Security - CRITICAL: These must be set in production
    SECRET_KEY: str = Field(..., min_length=32, description="Must be a strong secret key")
    ENCRYPTION_KEY: str = Field(..., min_length=32, description="Must be a strong encryption key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=15, le=120)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, le=30)
    
    # Database - Production database configuration
    DATABASE_URL: str = Field(..., description="Production database connection string")
    REDIS_URL: str = Field(..., description="Production Redis connection string")
    VECTOR_DB_URL: str = Field(..., description="Production vector database connection string")
    
    # AI Services - Required for production
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key required for production")
    ANTHROPIC_API_KEY: str = Field(..., description="Anthropic API key required for production")
    AI_MODEL: str = "gpt-4"
    AI_MAX_TOKENS: int = Field(default=1000, ge=100, le=4000)
    AI_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=1.0)
    
    # CORS - Restrictive for production
    CORS_ORIGINS: List[str] = Field(default=[], description="Allowed CORS origins for production")
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Monitoring & Observability
    ENABLE_MONITORING: bool = True
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3000
    LOG_LEVEL: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
    # Privacy & Compliance - Strict for production
    ENABLE_PRIVACY_CONTROLS: bool = True
    DATA_RETENTION_DAYS: int = Field(default=365, ge=30, le=2555)  # 30 days to 7 years
    ANONYMIZE_DATA: bool = True
    COMPLIANCE_FRAMEWORK: str = Field(default="GDPR", regex="^(GDPR|HIPAA|SOX|SOC2)$")
    DP_EPSILON: float = Field(default=1.0, ge=0.1, le=10.0)
    
    # Email Configuration
    SMTP_HOST: str = Field(..., description="Production SMTP host")
    SMTP_PORT: int = Field(default=587, ge=1, le=65535)
    SMTP_USERNAME: str = Field(..., description="Production SMTP username")
    SMTP_PASSWORD: str = Field(..., description="Production SMTP password")
    SMTP_USE_TLS: bool = True
    FROM_EMAIL: str = Field(..., description="Production sender email")
    
    # Enterprise Integrations
    SLACK_BOT_TOKEN: str = Field(default="", description="Slack bot token if using Slack integration")
    SLACK_SIGNING_SECRET: str = Field(default="", description="Slack signing secret if using Slack integration")
    TEAMS_APP_ID: str = Field(default="", description="Teams app ID if using Teams integration")
    TEAMS_CLIENT_SECRET: str = Field(default="", description="Teams client secret if using Teams integration")
    
    # HRIS Integrations
    WORKDAY_CLIENT_ID: str = Field(default="", description="Workday client ID if using Workday integration")
    WORKDAY_CLIENT_SECRET: str = Field(default="", description="Workday client secret if using Workday integration")
    BAMBOO_HR_API_KEY: str = Field(default="", description="BambooHR API key if using BambooHR integration")
    
    # Agent Configuration
    WELLNESS_COMPANION_MODEL: str = "gpt-4"
    WELLNESS_MEMORY_TYPE: str = Field(default="episodic", regex="^(episodic|summary|buffer)$")
    WELLNESS_RISK_THRESHOLD: float = Field(default=0.7, ge=0.1, le=1.0)
    RESOURCE_VECTOR_DB: str = "chromadb"
    RESOURCE_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    SENTIMENT_MODELS: List[str] = Field(default=["vader", "roberta"])
    RISK_INDICATORS: List[str] = Field(default=["burnout", "stress_spike", "toxic_patterns"])
    ANALYTICS_AGGREGATION_WINDOW: str = Field(default="7d", regex="^(1d|7d|30d|90d|365d)$")
    ANALYTICS_RETENTION_DAYS: int = Field(default=365, ge=30, le=2555)
    
    # Security Headers
    ENABLE_SECURITY_HEADERS: bool = True
    HSTS_MAX_AGE: int = Field(default=31536000, ge=0)  # 1 year
    CONTENT_SECURITY_POLICY: str = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    
    # Rate Limiting
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_REQUESTS: int = Field(default=100, ge=10, le=1000)
    RATE_LIMIT_WINDOW: int = Field(default=60, ge=10, le=3600)  # seconds
    
    # Backup & Recovery
    ENABLE_AUTO_BACKUP: bool = True
    BACKUP_FREQUENCY_HOURS: int = Field(default=24, ge=1, le=168)
    BACKUP_RETENTION_DAYS: int = Field(default=30, ge=1, le=365)
    
    # Performance
    ENABLE_CACHING: bool = True
    CACHE_TTL_SECONDS: int = Field(default=300, ge=60, le=3600)
    MAX_CONCURRENT_REQUESTS: int = Field(default=100, ge=10, le=1000)
    
    # Escalation & Support
    ESCALATION_EMAILS: List[str] = Field(default=[], description="Email addresses for escalation notifications")
    HR_TEAM_EMAILS: List[str] = Field(default=[], description="HR team email addresses")
    SUPPORT_EMAIL: str = Field(default="", description="Support email address")
    
    @validator('SECRET_KEY')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long')
        return v
    
    @validator('ENCRYPTION_KEY')
    def validate_encryption_key(cls, v):
        if len(v) < 32:
            raise ValueError('ENCRYPTION_KEY must be at least 32 characters long')
        return v
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        if not v.startswith(('postgresql://', 'postgres://')):
            raise ValueError('DATABASE_URL must be a PostgreSQL connection string')
        return v
    
    @validator('REDIS_URL')
    def validate_redis_url(cls, v):
        if not v.startswith('redis://'):
            raise ValueError('REDIS_URL must be a Redis connection string')
        return v
    
    @validator('CORS_ORIGINS')
    def validate_cors_origins(cls, v):
        if not v:
            raise ValueError('CORS_ORIGINS must be specified for production')
        return v
    
    @validator('FROM_EMAIL')
    def validate_from_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('FROM_EMAIL must be a valid email address')
        return v
    
    @validator('ESCALATION_EMAILS', 'HR_TEAM_EMAILS')
    def validate_email_lists(cls, v):
        for email in v:
            if '@' not in email or '.' not in email:
                raise ValueError(f'Invalid email address in list: {email}')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Production settings instance
production_settings = ProductionSettings()


def get_production_config() -> ProductionSettings:
    """Get production configuration with validation"""
    return production_settings


def validate_production_environment():
    """Validate that all required production environment variables are set"""
    missing_vars = []
    
    required_vars = [
        'SECRET_KEY',
        'ENCRYPTION_KEY',
        'DATABASE_URL',
        'REDIS_URL',
        'VECTOR_DB_URL',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'SMTP_HOST',
        'SMTP_USERNAME',
        'SMTP_PASSWORD',
        'FROM_EMAIL',
        'CORS_ORIGINS'
    ]
    
    for var in required_vars:
        if not getattr(production_settings, var, None):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required production environment variables: {', '.join(missing_vars)}")
    
    return True


def generate_secure_keys():
    """Generate secure keys for production deployment"""
    return {
        'SECRET_KEY': secrets.token_urlsafe(32),
        'ENCRYPTION_KEY': secrets.token_urlsafe(32)
    }


if __name__ == "__main__":
    # Validate production environment
    try:
        validate_production_environment()
        print("✅ Production environment validation passed")
    except ValueError as e:
        print(f"❌ Production environment validation failed: {e}")
        print("\nTo generate secure keys, run:")
        print("python -c \"from config.production import generate_secure_keys; print(generate_secure_keys())\"")
        exit(1)
