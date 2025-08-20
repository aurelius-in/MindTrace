from prometheus_client import (
    Counter, Histogram, Gauge, Summary, generate_latest, 
    CONTENT_TYPE_LATEST, CollectorRegistry, multiprocess
)
from typing import Dict, Any, Optional, List
import time
import logging
import asyncio
from datetime import datetime, timedelta
import json
import psutil
import threading
from contextlib import contextmanager

from config.settings import settings
from database.connection import get_db_session
from database.schema import SystemMetrics, AgentPerformance

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Centralized metrics collection and monitoring."""
    
    def __init__(self):
        self.registry = CollectorRegistry()
        
        # HTTP metrics
        self.http_requests_total = Counter(
            'http_requests_total',
            'Total number of HTTP requests',
            ['method', 'endpoint', 'status'],
            registry=self.registry
        )
        
        self.http_request_duration_seconds = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            registry=self.registry
        )
        
        # Agent metrics
        self.agent_requests_total = Counter(
            'agent_requests_total',
            'Total number of agent requests',
            ['agent_type', 'workflow_type', 'status'],
            registry=self.registry
        )
        
        self.agent_response_time_seconds = Histogram(
            'agent_response_time_seconds',
            'Agent response time in seconds',
            ['agent_type', 'workflow_type'],
            registry=self.registry
        )
        
        self.agent_memory_usage_bytes = Gauge(
            'agent_memory_usage_bytes',
            'Agent memory usage in bytes',
            ['agent_type'],
            registry=self.registry
        )
        
        # Business metrics
        self.active_users_gauge = Gauge(
            'active_users_total',
            'Total number of active users',
            registry=self.registry
        )
        
        self.conversations_total = Counter(
            'conversations_total',
            'Total number of conversations',
            ['user_role', 'risk_level'],
            registry=self.registry
        )
        
        self.wellness_entries_total = Counter(
            'wellness_entries_total',
            'Total number of wellness entries',
            ['entry_type'],
            registry=self.registry
        )
        
        self.resource_recommendations_total = Counter(
            'resource_recommendations_total',
            'Total number of resource recommendations',
            ['resource_type', 'category'],
            registry=self.registry
        )
        
        # System metrics
        self.system_memory_usage_percent = Gauge(
            'system_memory_usage_percent',
            'System memory usage percentage',
            registry=self.registry
        )
        
        self.system_cpu_usage_percent = Gauge(
            'system_cpu_usage_percent',
            'System CPU usage percentage',
            registry=self.registry
        )
        
        self.database_connections_active = Gauge(
            'database_connections_active',
            'Number of active database connections',
            registry=self.registry
        )
        
        # Error metrics
        self.errors_total = Counter(
            'errors_total',
            'Total number of errors',
            ['error_type', 'component'],
            registry=self.registry
        )
        
        # Privacy and compliance metrics
        self.privacy_violations_total = Counter(
            'privacy_violations_total',
            'Total number of privacy violations',
            ['violation_type', 'severity'],
            registry=self.registry
        )
        
        self.data_anonymization_total = Counter(
            'data_anonymization_total',
            'Total number of data anonymization operations',
            ['data_type'],
            registry=self.registry
        )
        
        # Custom metrics storage
        self.custom_metrics = {}
        self.metrics_lock = threading.Lock()
        
        # Start background monitoring
        self._start_background_monitoring()
    
    def record_http_request(self, method: str, endpoint: str, status: int, duration: float):
        """Record HTTP request metrics."""
        self.http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
        self.http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
    
    def record_agent_request(self, agent_type: str, workflow_type: str, status: str, duration: float):
        """Record agent request metrics."""
        self.agent_requests_total.labels(
            agent_type=agent_type, 
            workflow_type=workflow_type, 
            status=status
        ).inc()
        self.agent_response_time_seconds.labels(
            agent_type=agent_type, 
            workflow_type=workflow_type
        ).observe(duration)
    
    def record_conversation(self, user_role: str, risk_level: str):
        """Record conversation metrics."""
        self.conversations_total.labels(user_role=user_role, risk_level=risk_level).inc()
    
    def record_wellness_entry(self, entry_type: str):
        """Record wellness entry metrics."""
        self.wellness_entries_total.labels(entry_type=entry_type).inc()
    
    def record_resource_recommendation(self, resource_type: str, category: str):
        """Record resource recommendation metrics."""
        self.resource_recommendations_total.labels(
            resource_type=resource_type, 
            category=category
        ).inc()
    
    def record_error(self, error_type: str, component: str):
        """Record error metrics."""
        self.errors_total.labels(error_type=error_type, component=component).inc()
    
    def record_privacy_violation(self, violation_type: str, severity: str):
        """Record privacy violation metrics."""
        self.privacy_violations_total.labels(
            violation_type=violation_type, 
            severity=severity
        ).inc()
    
    def record_data_anonymization(self, data_type: str):
        """Record data anonymization metrics."""
        self.data_anonymization_total.labels(data_type=data_type).inc()
    
    def set_active_users(self, count: int):
        """Set active users count."""
        self.active_users_gauge.set(count)
    
    def set_system_metrics(self):
        """Update system metrics."""
        # Memory usage
        memory = psutil.virtual_memory()
        self.system_memory_usage_percent.set(memory.percent)
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.system_cpu_usage_percent.set(cpu_percent)
    
    def set_database_connections(self, count: int):
        """Set database connections count."""
        self.database_connections_active.set(count)
    
    def add_custom_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """Add a custom metric."""
        with self.metrics_lock:
            if name not in self.custom_metrics:
                self.custom_metrics[name] = Gauge(
                    f'custom_{name}',
                    f'Custom metric: {name}',
                    list(labels.keys()) if labels else [],
                    registry=self.registry
                )
            
            if labels:
                self.custom_metrics[name].labels(**labels).set(value)
            else:
                self.custom_metrics[name].set(value)
    
    def get_metrics(self) -> str:
        """Get Prometheus metrics as string."""
        return generate_latest(self.registry)
    
    def get_metrics_dict(self) -> Dict[str, Any]:
        """Get metrics as dictionary for API responses."""
        metrics_data = {
            "http_requests": {
                "total": self._get_counter_value(self.http_requests_total),
                "duration": self._get_histogram_value(self.http_request_duration_seconds)
            },
            "agent_requests": {
                "total": self._get_counter_value(self.agent_requests_total),
                "response_time": self._get_histogram_value(self.agent_response_time_seconds)
            },
            "business_metrics": {
                "active_users": self.active_users_gauge._value.get(),
                "conversations": self._get_counter_value(self.conversations_total),
                "wellness_entries": self._get_counter_value(self.wellness_entries_total),
                "resource_recommendations": self._get_counter_value(self.resource_recommendations_total)
            },
            "system_metrics": {
                "memory_usage_percent": self.system_memory_usage_percent._value.get(),
                "cpu_usage_percent": self.system_cpu_usage_percent._value.get(),
                "database_connections": self.database_connections_active._value.get()
            },
            "errors": self._get_counter_value(self.errors_total),
            "privacy": {
                "violations": self._get_counter_value(self.privacy_violations_total),
                "anonymization": self._get_counter_value(self.data_anonymization_total)
            },
            "custom_metrics": self.custom_metrics
        }
        
        return metrics_data
    
    def _get_counter_value(self, counter) -> Dict[str, Any]:
        """Get counter value with labels."""
        try:
            return {
                "total": counter._value.get(),
                "labels": {str(label): value for label, value in counter._metrics.items()}
            }
        except:
            return {"total": 0, "labels": {}}
    
    def _get_histogram_value(self, histogram) -> Dict[str, Any]:
        """Get histogram value with buckets."""
        try:
            return {
                "count": histogram._count.get(),
                "sum": histogram._sum.get(),
                "buckets": {str(bucket): value for bucket, value in histogram._buckets.items()}
            }
        except:
            return {"count": 0, "sum": 0, "buckets": {}}
    
    def _start_background_monitoring(self):
        """Start background monitoring tasks."""
        def monitor_system():
            while True:
                try:
                    self.set_system_metrics()
                    time.sleep(60)  # Update every minute
                except Exception as e:
                    logger.error(f"System monitoring error: {e}")
                    time.sleep(60)
        
        def monitor_database():
            while True:
                try:
                    from database.connection import get_database_stats
                    stats = get_database_stats()
                    self.set_database_connections(stats["checked_out"])
                    time.sleep(30)  # Update every 30 seconds
                except Exception as e:
                    logger.error(f"Database monitoring error: {e}")
                    time.sleep(30)
        
        # Start monitoring threads
        threading.Thread(target=monitor_system, daemon=True).start()
        threading.Thread(target=monitor_database, daemon=True).start()

class PerformanceMonitor:
    """Performance monitoring utilities."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
    
    @contextmanager
    def monitor_function(self, function_name: str, component: str = "api"):
        """Context manager to monitor function performance."""
        start_time = time.time()
        try:
            yield
            duration = time.time() - start_time
            self.metrics.add_custom_metric(
                f"{component}_{function_name}_duration_seconds",
                duration
            )
        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_error("function_error", component)
            self.metrics.add_custom_metric(
                f"{component}_{function_name}_error_duration_seconds",
                duration
            )
            raise
    
    async def monitor_async_function(self, function_name: str, component: str = "api"):
        """Async decorator to monitor function performance."""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    duration = time.time() - start_time
                    self.metrics.add_custom_metric(
                        f"{component}_{function_name}_duration_seconds",
                        duration
                    )
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self.metrics.record_error("async_function_error", component)
                    self.metrics.add_custom_metric(
                        f"{component}_{function_name}_error_duration_seconds",
                        duration
                    )
                    raise
            return wrapper
        return decorator

class HealthChecker:
    """Health check utilities."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
    
    async def check_system_health(self) -> Dict[str, Any]:
        """Perform comprehensive system health check."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {}
        }
        
        # Check system resources
        try:
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            health_status["components"]["system"] = {
                "status": "healthy",
                "memory_usage_percent": memory.percent,
                "cpu_usage_percent": cpu_percent,
                "disk_usage_percent": psutil.disk_usage('/').percent
            }
            
            # Alert if resources are high
            if memory.percent > 90 or cpu_percent > 90:
                health_status["components"]["system"]["status"] = "warning"
                health_status["status"] = "degraded"
                
        except Exception as e:
            health_status["components"]["system"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "unhealthy"
        
        # Check database connection
        try:
            from database.connection import check_database_connection, get_database_stats
            db_healthy = check_database_connection()
            db_stats = get_database_stats()
            
            health_status["components"]["database"] = {
                "status": "healthy" if db_healthy else "unhealthy",
                "connection": db_healthy,
                "pool_stats": db_stats
            }
            
            if not db_healthy:
                health_status["status"] = "unhealthy"
                
        except Exception as e:
            health_status["components"]["database"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "unhealthy"
        
        # Check external services
        try:
            external_services = self._check_external_services()
            health_status["components"]["external_services"] = {
                "status": "healthy" if all(external_services.values()) else "degraded",
                "services": external_services
            }
            
            if not all(external_services.values()):
                health_status["status"] = "degraded"
                
        except Exception as e:
            health_status["components"]["external_services"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "unhealthy"
        
        return health_status
    
    def _check_external_services(self) -> Dict[str, bool]:
        """Check external service health"""
        try:
            service_status = {}
            
            # Check OpenAI API
            service_status["openai"] = self._check_openai_service()
            
            # Check ChromaDB
            service_status["chromadb"] = self._check_chromadb_service()
            
            # Check Redis
            service_status["redis"] = self._check_redis_service()
            
            # Check PostgreSQL
            service_status["postgresql"] = self._check_postgresql_service()
            
            # Check Slack API (if configured)
            if hasattr(settings.integrations, 'slack_bot_token') and settings.integrations.slack_bot_token:
                service_status["slack"] = self._check_slack_service()
            
            # Check Teams API (if configured)
            if hasattr(settings.integrations, 'teams_app_id') and settings.integrations.teams_app_id:
                service_status["teams"] = self._check_teams_service()
            
            return service_status
            
        except Exception as e:
            self.logger.error(f"Error checking external services: {e}")
            return {
                "openai": False,
                "chromadb": False,
                "redis": False,
                "postgresql": False
            }
    
    def _check_openai_service(self) -> bool:
        """Check OpenAI API connectivity"""
        try:
            import openai
            from config.settings import settings
            
            # Test with a simple API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
                api_key=settings.ai.openai_api_key
            )
            
            return response is not None
            
        except Exception as e:
            self.logger.error(f"OpenAI service check failed: {e}")
            return False
    
    def _check_chromadb_service(self) -> bool:
        """Check ChromaDB connectivity"""
        try:
            import chromadb
            
            # Test connection to ChromaDB
            client = chromadb.PersistentClient(path="./data/chromadb")
            collections = client.list_collections()
            
            return True
            
        except Exception as e:
            self.logger.error(f"ChromaDB service check failed: {e}")
            return False
    
    def _check_redis_service(self) -> bool:
        """Check Redis connectivity"""
        try:
            import redis
            from config.settings import settings
            
            # Test Redis connection
            r = redis.from_url(settings.database.redis_url)
            r.ping()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Redis service check failed: {e}")
            return False
    
    def _check_postgresql_service(self) -> bool:
        """Check PostgreSQL connectivity"""
        try:
            from database.connection import check_db_connection
            
            return check_db_connection()
            
        except Exception as e:
            self.logger.error(f"PostgreSQL service check failed: {e}")
            return False
    
    def _check_slack_service(self) -> bool:
        """Check Slack API connectivity"""
        try:
            from slack_sdk import WebClient
            from config.settings import settings
            
            # Test Slack API connection
            client = WebClient(token=settings.integrations.slack_bot_token)
            response = client.auth_test()
            
            return response["ok"] if response else False
            
        except Exception as e:
            self.logger.error(f"Slack service check failed: {e}")
            return False
    
    def _check_teams_service(self) -> bool:
        """Check Teams API connectivity"""
        try:
            from microsoft_graph_python import GraphServiceClient
            from config.settings import settings
            
            # Test Teams API connection
            client = GraphServiceClient(credentials=settings.integrations.teams_client_credentials)
            
            # Try to get user info as a test
            user = client.me.get()
            
            return user is not None
            
        except Exception as e:
            self.logger.error(f"Teams service check failed: {e}")
            return False
    
    async def check_agent_health(self) -> Dict[str, Any]:
        """Check agent system health."""
        try:
            from agents.orchestrator import AgentOrchestrator
            orchestrator = AgentOrchestrator()
            agent_metrics = orchestrator.get_agent_metrics()
            workflow_stats = orchestrator.get_workflow_stats()
            
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "agent_metrics": agent_metrics,
                "workflow_stats": workflow_stats
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }

class MetricsExporter:
    """Export metrics to various destinations."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
    
    async def export_to_database(self):
        """Export metrics to database for historical analysis."""
        try:
            with get_db_session() as db:
                metrics_data = self.metrics.get_metrics_dict()
                
                # Export system metrics
                for metric_name, value in metrics_data["system_metrics"].items():
                    metric = SystemMetrics(
                        metric_name=metric_name,
                        metric_value=value,
                        metric_unit=self._get_unit_for_metric(metric_name),
                        tags={"source": "prometheus"}
                    )
                    db.add(metric)
                
                # Export agent performance metrics
                agent_metrics = metrics_data["agent_requests"]
                if agent_metrics["total"]["labels"]:
                    for labels, value in agent_metrics["total"]["labels"].items():
                        # Parse labels to extract agent_type and workflow_type
                        # This is a simplified version - you might need more complex parsing
                        performance = AgentPerformance(
                            agent_type="unknown",  # Parse from labels
                            workflow_type="unknown",  # Parse from labels
                            execution_time_ms=int(agent_metrics["response_time"]["sum"] * 1000),
                            success=True,  # You might want to track this separately
                            input_size=0,  # Track this if needed
                            output_size=0   # Track this if needed
                        )
                        db.add(performance)
                
                logger.info("Metrics exported to database successfully")
                
        except Exception as e:
            logger.error(f"Failed to export metrics to database: {e}")
    
    def _get_unit_for_metric(self, metric_name: str) -> str:
        """Get the unit for a metric name."""
        units = {
            "memory_usage_percent": "percent",
            "cpu_usage_percent": "percent",
            "database_connections": "connections",
            "active_users_total": "users",
            "conversations_total": "conversations",
            "wellness_entries_total": "entries"
        }
        return units.get(metric_name, "unknown")

# Global instances
metrics_collector = MetricsCollector()
performance_monitor = PerformanceMonitor(metrics_collector)
health_checker = HealthChecker(metrics_collector)
metrics_exporter = MetricsExporter(metrics_collector)

# Export commonly used functions and classes
__all__ = [
    'MetricsCollector',
    'PerformanceMonitor',
    'HealthChecker',
    'MetricsExporter',
    'metrics_collector',
    'performance_monitor',
    'health_checker',
    'metrics_exporter'
]
