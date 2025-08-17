"""
Configuration Settings - Application configuration management
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "Enterprise Employee Wellness AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Database
    DATABASE_URL: str = "sqlite:///./wellness_app.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # AI/ML Services
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-3.5-turbo"
    AI_MAX_TOKENS: int = 1000
    AI_TEMPERATURE: float = 0.7
    
    # Vector Database
    VECTOR_DB_URL: Optional[str] = None
    VECTOR_DB_API_KEY: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_DB: int = 0
    
    # Monitoring
    ENABLE_MONITORING: bool = True
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3000
    
    # Privacy & Compliance
    ENABLE_PRIVACY_CONTROLS: bool = True
    DATA_RETENTION_DAYS: int = 365
    ANONYMIZE_DATA: bool = False
    COMPLIANCE_FRAMEWORK: str = "GDPR"  # GDPR, HIPAA, SOX
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    FROM_EMAIL: str = "noreply@wellness-ai.com"
    
    # External Integrations
    SLACK_WEBHOOK_URL: Optional[str] = None
    MICROSOFT_GRAPH_CLIENT_ID: Optional[str] = None
    MICROSOFT_GRAPH_CLIENT_SECRET: Optional[str] = None
    MICROSOFT_GRAPH_TENANT_ID: Optional[str] = None
    
    # File Storage
    STORAGE_TYPE: str = "local"  # local, s3, azure
    STORAGE_PATH: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Feature Flags
    ENABLE_AI_CHAT: bool = True
    ENABLE_ANALYTICS: bool = True
    ENABLE_RISK_ASSESSMENT: bool = True
    ENABLE_TEAM_INSIGHTS: bool = True
    ENABLE_RESOURCE_RECOMMENDATIONS: bool = True
    
    # Wellness Settings
    DEFAULT_CHECKIN_FREQUENCY: str = "daily"  # daily, weekly, monthly
    WELLNESS_SCORE_THRESHOLD: float = 5.0
    RISK_ALERT_THRESHOLD: float = 7.0
    MAX_RECOMMENDATIONS: int = 5
    
    # Agent Settings
    AGENT_TIMEOUT: int = 30  # seconds
    AGENT_MAX_RETRIES: int = 3
    AGENT_COLLABORATION_ENABLED: bool = True
    
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v):
        if not v:
            return "sqlite:///./wellness_app.db"
        return v
    
    @validator("SECRET_KEY", pre=True)
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production":
            import secrets
            return secrets.token_urlsafe(32)
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def validate_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    ENABLE_MONITORING: bool = False


class ProductionSettings(Settings):
    """Production environment settings"""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    ENABLE_PRIVACY_CONTROLS: bool = True
    ANONYMIZE_DATA: bool = True


class TestingSettings(Settings):
    """Testing environment settings"""
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test_wellness_app.db"
    ENABLE_MONITORING: bool = False
    ENABLE_AI_CHAT: bool = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Export settings
__all__ = ["settings", "get_settings", "Settings"]
