"""
Enterprise Employee Wellness AI - Configuration Settings
"""

from typing import Dict, List, Optional
from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    postgres_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    vector_db_url: str = Field(..., env="VECTOR_DB_URL")
    
    class Config:
        env_file = ".env"


class AISettings(BaseSettings):
    """AI and LLM configuration settings"""
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    default_model: str = Field("gpt-4", env="DEFAULT_MODEL")
    embedding_model: str = Field("text-embedding-ada-002", env="EMBEDDING_MODEL")
    
    class Config:
        env_file = ".env"


class SecuritySettings(BaseSettings):
    """Security and privacy configuration"""
    secret_key: str = Field(..., env="SECRET_KEY")
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Privacy settings
    differential_privacy_epsilon: float = Field(1.0, env="DP_EPSILON")
    anonymization_enabled: bool = Field(True, env="ANONYMIZATION_ENABLED")
    
    class Config:
        env_file = ".env"


class IntegrationSettings(BaseSettings):
    """Enterprise integration settings"""
    slack_bot_token: str = Field(..., env="SLACK_BOT_TOKEN")
    slack_signing_secret: str = Field(..., env="SLACK_SIGNING_SECRET")
    teams_app_id: str = Field(..., env="TEAMS_APP_ID")
    teams_client_secret: str = Field(..., env="TEAMS_CLIENT_SECRET")
    
    # HRIS integrations
    workday_client_id: str = Field(..., env="WORKDAY_CLIENT_ID")
    workday_client_secret: str = Field(..., env="WORKDAY_CLIENT_SECRET")
    bamboo_hr_api_key: str = Field(..., env="BAMBOO_HR_API_KEY")
    
    class Config:
        env_file = ".env"


class MonitoringSettings(BaseSettings):
    """Observability and monitoring settings"""
    prometheus_endpoint: str = Field("http://localhost:9090", env="PROMETHEUS_ENDPOINT")
    grafana_url: str = Field("http://localhost:3000", env="GRAFANA_URL")
    opa_policy_url: str = Field("http://localhost:8181", env="OPA_POLICY_URL")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    
    class Config:
        env_file = ".env"


class AgentSettings(BaseSettings):
    """Agent-specific configuration"""
    
    # Wellness Companion Agent
    wellness_companion_model: str = Field("gpt-4", env="WELLNESS_COMPANION_MODEL")
    wellness_memory_type: str = Field("episodic", env="WELLNESS_MEMORY_TYPE")
    wellness_risk_threshold: float = Field(0.7, env="WELLNESS_RISK_THRESHOLD")
    
    # Resource Recommendation Agent
    resource_vector_db: str = Field("chromadb", env="RESOURCE_VECTOR_DB")
    resource_embedding_model: str = Field("text-embedding-ada-002", env="RESOURCE_EMBEDDING_MODEL")
    
    # Sentiment Analysis Agent
    sentiment_models: List[str] = Field(["vader", "roberta"], env="SENTIMENT_MODELS")
    risk_indicators: List[str] = Field(["burnout", "stress_spike", "toxic_patterns"], env="RISK_INDICATORS")
    
    # Analytics Agent
    analytics_aggregation_window: str = Field("7d", env="ANALYTICS_AGGREGATION_WINDOW")
    analytics_retention_days: int = Field(365, env="ANALYTICS_RETENTION_DAYS")
    
    # Privacy Agent
    privacy_scrubbing_rules: Dict[str, str] = Field({
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
    })
    
    class Config:
        env_file = ".env"


class Settings(BaseSettings):
    """Main application settings"""
    
    # App metadata
    app_name: str = "Enterprise Employee Wellness AI"
    app_version: str = "1.0.0"
    debug: bool = Field(False, env="DEBUG")
    
    # API settings
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    cors_origins: List[str] = Field(["http://localhost:3000"], env="CORS_ORIGINS")
    
    # Database
    database: DatabaseSettings = DatabaseSettings()
    
    # AI
    ai: AISettings = AISettings()
    
    # Security
    security: SecuritySettings = SecuritySettings()
    
    # Integrations
    integrations: IntegrationSettings = IntegrationSettings()
    
    # Monitoring
    monitoring: MonitoringSettings = MonitoringSettings()
    
    # Agents
    agents: AgentSettings = AgentSettings()
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
