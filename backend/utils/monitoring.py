"""
Monitoring Utility - Prometheus metrics and monitoring setup
"""

import logging
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import time

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'active_users_total',
    'Total number of active users'
)

WELLNESS_CHECKINS = Counter(
    'wellness_checkins_total',
    'Total wellness check-ins',
    ['type', 'user_role']
)

AI_CONVERSATIONS = Counter(
    'ai_conversations_total',
    'Total AI conversations',
    ['sentiment', 'risk_level']
)

RESOURCE_INTERACTIONS = Counter(
    'resource_interactions_total',
    'Total resource interactions',
    ['interaction_type', 'category']
)

ERROR_COUNT = Counter(
    'errors_total',
    'Total errors',
    ['error_type', 'endpoint']
)

DATABASE_OPERATIONS = Histogram(
    'database_operation_duration_seconds',
    'Database operation duration in seconds',
    ['operation', 'table']
)


class MonitoringManager:
    """
    Manages application monitoring and metrics
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_enabled = True
    
    def setup_monitoring(self, app):
        """
        Setup monitoring middleware and endpoints
        """
        if not self.metrics_enabled:
            return
        
        # Add monitoring middleware
        @app.middleware("http")
        async def monitoring_middleware(request: Request, call_next):
            start_time = time.time()
            
            # Process request
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            endpoint = request.url.path
            
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status=response.status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=endpoint
            ).observe(duration)
            
            # Log errors
            if response.status_code >= 400:
                ERROR_COUNT.labels(
                    error_type=f"http_{response.status_code}",
                    endpoint=endpoint
                ).inc()
            
            return response
        
        # Add metrics endpoint
        @app.get("/metrics")
        async def metrics():
            return Response(
                content=generate_latest(),
                media_type=CONTENT_TYPE_LATEST
            )
        
        self.logger.info("Monitoring setup completed")
    
    def record_wellness_checkin(self, checkin_type: str, user_role: str):
        """
        Record wellness check-in metric
        """
        if self.metrics_enabled:
            WELLNESS_CHECKINS.labels(
                type=checkin_type,
                user_role=user_role
            ).inc()
    
    def record_ai_conversation(self, sentiment: str, risk_level: str):
        """
        Record AI conversation metric
        """
        if self.metrics_enabled:
            AI_CONVERSATIONS.labels(
                sentiment=sentiment,
                risk_level=risk_level
            ).inc()
    
    def record_resource_interaction(self, interaction_type: str, category: str):
        """
        Record resource interaction metric
        """
        if self.metrics_enabled:
            RESOURCE_INTERACTIONS.labels(
                interaction_type=interaction_type,
                category=category
            ).inc()
    
    def record_database_operation(self, operation: str, table: str, duration: float):
        """
        Record database operation metric
        """
        if self.metrics_enabled:
            DATABASE_OPERATIONS.labels(
                operation=operation,
                table=table
            ).observe(duration)
    
    def update_active_users(self, count: int):
        """
        Update active users metric
        """
        if self.metrics_enabled:
            ACTIVE_USERS.set(count)
    
    def record_error(self, error_type: str, endpoint: str):
        """
        Record error metric
        """
        if self.metrics_enabled:
            ERROR_COUNT.labels(
                error_type=error_type,
                endpoint=endpoint
            ).inc()
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get metrics summary
        """
        try:
            # This would typically query Prometheus for actual values
            # For now, return a placeholder structure
            return {
                "total_requests": "N/A",  # Would be actual value from Prometheus
                "active_users": "N/A",
                "wellness_checkins": "N/A",
                "ai_conversations": "N/A",
                "resource_interactions": "N/A",
                "errors": "N/A",
                "average_response_time": "N/A"
            }
        except Exception as e:
            self.logger.error(f"Failed to get metrics summary: {e}")
            return {}


# Global monitoring manager instance
monitoring_manager = MonitoringManager()


def setup_monitoring(app):
    """
    Setup monitoring for the application
    """
    monitoring_manager.setup_monitoring(app)


def record_wellness_checkin(checkin_type: str, user_role: str):
    """
    Record wellness check-in metric
    """
    monitoring_manager.record_wellness_checkin(checkin_type, user_role)


def record_ai_conversation(sentiment: str, risk_level: str):
    """
    Record AI conversation metric
    """
    monitoring_manager.record_ai_conversation(sentiment, risk_level)


def record_resource_interaction(interaction_type: str, category: str):
    """
    Record resource interaction metric
    """
    monitoring_manager.record_resource_interaction(interaction_type, category)


def record_database_operation(operation: str, table: str, duration: float):
    """
    Record database operation metric
    """
    monitoring_manager.record_database_operation(operation, table, duration)


def update_active_users(count: int):
    """
    Update active users metric
    """
    monitoring_manager.update_active_users(count)


def record_error(error_type: str, endpoint: str):
    """
    Record error metric
    """
    monitoring_manager.record_error(error_type, endpoint)


def get_metrics_summary() -> Dict[str, Any]:
    """
    Get metrics summary
    """
    return monitoring_manager.get_metrics_summary()
