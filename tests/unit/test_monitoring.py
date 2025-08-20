"""
Unit tests for monitoring and observability
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time
import json

from backend.monitoring.metrics import MetricsCollector
from backend.monitoring.health_checks import HealthChecker
from backend.monitoring.logging import Logger
from backend.monitoring.alerting import AlertManager
from backend.monitoring.performance import PerformanceMonitor


class TestMetricsCollector:
    """Test MetricsCollector functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.metrics = MetricsCollector()
    
    def test_initialization(self):
        """Test metrics collector initialization"""
        assert self.metrics.prometheus_client is not None
        assert self.metrics.metrics_registry is not None
    
    def test_collect_system_metrics(self):
        """Test system metrics collection"""
        metrics = self.metrics.collect_system_metrics()
        assert metrics is not None
        assert "cpu_usage" in metrics
        assert "memory_usage" in metrics
        assert "disk_usage" in metrics
        assert all(isinstance(v, (int, float)) for v in metrics.values())
    
    def test_collect_application_metrics(self):
        """Test application metrics collection"""
        metrics = self.metrics.collect_application_metrics()
        assert metrics is not None
        assert "request_count" in metrics
        assert "response_time" in metrics
        assert "error_rate" in metrics
        assert "active_users" in metrics
    
    def test_collect_business_metrics(self):
        """Test business metrics collection"""
        metrics = self.metrics.collect_business_metrics()
        assert metrics is not None
        assert "wellness_score_avg" in metrics
        assert "stress_level_avg" in metrics
        assert "user_engagement" in metrics
        assert "intervention_effectiveness" in metrics
    
    def test_record_metric(self):
        """Test metric recording"""
        with patch.object(self.metrics, 'prometheus_client') as mock_client:
            self.metrics.record_metric("test_metric", 42.0, {"label": "value"})
            mock_client.Counter.assert_called_once()
    
    def test_get_metrics_summary(self):
        """Test metrics summary generation"""
        summary = self.metrics.get_metrics_summary()
        assert summary is not None
        assert "system" in summary
        assert "application" in summary
        assert "business" in summary
        assert "timestamp" in summary
    
    def test_check_external_services(self):
        """Test external service health checks"""
        with patch.object(self.metrics, '_check_openai_service') as mock_openai:
            with patch.object(self.metrics, '_check_chromadb_service') as mock_chroma:
                with patch.object(self.metrics, '_check_redis_service') as mock_redis:
                    mock_openai.return_value = {"status": "healthy"}
                    mock_chroma.return_value = {"status": "healthy"}
                    mock_redis.return_value = {"status": "healthy"}
                    
                    services = self.metrics._check_external_services()
                    assert services is not None
                    assert "openai" in services
                    assert "chromadb" in services
                    assert "redis" in services


class TestHealthChecker:
    """Test HealthChecker functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.health_checker = HealthChecker()
    
    def test_initialization(self):
        """Test health checker initialization"""
        assert self.health_checker.checks is not None
        assert len(self.health_checker.checks) > 0
    
    def test_check_database_health(self):
        """Test database health check"""
        with patch('backend.monitoring.health_checks.database_connection') as mock_db:
            mock_db.check_connection.return_value = True
            
            health = self.health_checker.check_database_health()
            assert health is not None
            assert "status" in health
            assert "response_time" in health
            assert health["status"] == "healthy"
    
    def test_check_redis_health(self):
        """Test Redis health check"""
        with patch('backend.monitoring.health_checks.redis_client') as mock_redis:
            mock_redis.ping.return_value = True
            
            health = self.health_checker.check_redis_health()
            assert health is not None
            assert "status" in health
            assert "response_time" in health
            assert health["status"] == "healthy"
    
    def test_check_vector_db_health(self):
        """Test vector database health check"""
        with patch('backend.monitoring.health_checks.vector_db_client') as mock_vector:
            mock_vector.health_check.return_value = {"status": "healthy"}
            
            health = self.health_checker.check_vector_db_health()
            assert health is not None
            assert "status" in health
            assert health["status"] == "healthy"
    
    def test_check_ai_services_health(self):
        """Test AI services health check"""
        with patch('backend.monitoring.health_checks.openai_client') as mock_openai:
            mock_openai.health_check.return_value = {"status": "healthy"}
            
            health = self.health_checker.check_ai_services_health()
            assert health is not None
            assert "openai" in health
            assert health["openai"]["status"] == "healthy"
    
    def test_run_all_health_checks(self):
        """Test running all health checks"""
        with patch.object(self.health_checker, 'check_database_health') as mock_db:
            with patch.object(self.health_checker, 'check_redis_health') as mock_redis:
                with patch.object(self.health_checker, 'check_vector_db_health') as mock_vector:
                    with patch.object(self.health_checker, 'check_ai_services_health') as mock_ai:
                        mock_db.return_value = {"status": "healthy"}
                        mock_redis.return_value = {"status": "healthy"}
                        mock_vector.return_value = {"status": "healthy"}
                        mock_ai.return_value = {"openai": {"status": "healthy"}}
                        
                        all_checks = self.health_checker.run_all_health_checks()
                        assert all_checks is not None
                        assert "database" in all_checks
                        assert "redis" in all_checks
                        assert "vector_db" in all_checks
                        assert "ai_services" in all_checks
                        assert all_checks["overall_status"] == "healthy"


class TestLogger:
    """Test Logger functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.logger = Logger()
    
    def test_initialization(self):
        """Test logger initialization"""
        assert self.logger.logger is not None
        assert self.logger.log_level is not None
    
    def test_log_info(self):
        """Test info logging"""
        with patch.object(self.logger.logger, 'info') as mock_info:
            self.logger.log_info("Test info message")
            mock_info.assert_called_once_with("Test info message")
    
    def test_log_warning(self):
        """Test warning logging"""
        with patch.object(self.logger.logger, 'warning') as mock_warning:
            self.logger.log_warning("Test warning message")
            mock_warning.assert_called_once_with("Test warning message")
    
    def test_log_error(self):
        """Test error logging"""
        with patch.object(self.logger.logger, 'error') as mock_error:
            self.logger.log_error("Test error message")
            mock_error.assert_called_once_with("Test error message")
    
    def test_log_critical(self):
        """Test critical logging"""
        with patch.object(self.logger.logger, 'critical') as mock_critical:
            self.logger.log_critical("Test critical message")
            mock_critical.assert_called_once_with("Test critical message")
    
    def test_log_with_context(self):
        """Test logging with context"""
        with patch.object(self.logger.logger, 'info') as mock_info:
            context = {"user_id": "test_user", "action": "login"}
            self.logger.log_with_context("User action", context, "info")
            mock_info.assert_called_once()
    
    def test_log_performance(self):
        """Test performance logging"""
        with patch.object(self.logger.logger, 'info') as mock_info:
            self.logger.log_performance("test_operation", 1.5, {"details": "test"})
            mock_info.assert_called_once()
    
    def test_log_security_event(self):
        """Test security event logging"""
        with patch.object(self.logger.logger, 'warning') as mock_warning:
            self.logger.log_security_event("failed_login", {"ip": "192.168.1.1"})
            mock_warning.assert_called_once()


class TestAlertManager:
    """Test AlertManager functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.alert_manager = AlertManager()
    
    def test_initialization(self):
        """Test alert manager initialization"""
        assert self.alert_manager.alert_rules is not None
        assert self.alert_manager.notification_channels is not None
    
    def test_check_alert_conditions(self):
        """Test alert condition checking"""
        metrics = {
            "cpu_usage": 85.0,
            "memory_usage": 90.0,
            "error_rate": 0.05
        }
        
        alerts = self.alert_manager.check_alert_conditions(metrics)
        assert alerts is not None
        assert isinstance(alerts, list)
    
    def test_create_alert(self):
        """Test alert creation"""
        alert = self.alert_manager.create_alert(
            alert_type="high_cpu_usage",
            severity="warning",
            message="CPU usage is high",
            metadata={"cpu_usage": 85.0}
        )
        assert alert is not None
        assert "alert_id" in alert
        assert "timestamp" in alert
        assert "severity" in alert
        assert alert["severity"] == "warning"
    
    def test_send_alert_notification(self):
        """Test alert notification sending"""
        with patch.object(self.alert_manager, 'send_email_alert') as mock_email:
            with patch.object(self.alert_manager, 'send_slack_alert') as mock_slack:
                mock_email.return_value = True
                mock_slack.return_value = True
                
                alert = {
                    "alert_id": "alert_123",
                    "severity": "critical",
                    "message": "System down"
                }
                
                result = self.alert_manager.send_alert_notification(alert)
                assert result is True
                mock_email.assert_called_once()
                mock_slack.assert_called_once()
    
    def test_send_email_alert(self):
        """Test email alert sending"""
        with patch('backend.monitoring.alerting.email_utility') as mock_email:
            mock_email.send_alert_email.return_value = True
            
            alert = {"message": "Test alert"}
            result = self.alert_manager.send_email_alert(alert)
            assert result is True
            mock_email.send_alert_email.assert_called_once()
    
    def test_send_slack_alert(self):
        """Test Slack alert sending"""
        with patch('backend.monitoring.alerting.slack_integration') as mock_slack:
            mock_slack.send_alert_message.return_value = True
            
            alert = {"message": "Test alert"}
            result = self.alert_manager.send_slack_alert(alert)
            assert result is True
            mock_slack.send_alert_message.assert_called_once()
    
    def test_resolve_alert(self):
        """Test alert resolution"""
        alert_id = "alert_123"
        resolution_notes = "Issue resolved"
        
        with patch.object(self.alert_manager, 'update_alert_status') as mock_update:
            mock_update.return_value = True
            
            result = self.alert_manager.resolve_alert(alert_id, resolution_notes)
            assert result is True
            mock_update.assert_called_once_with(alert_id, "resolved", resolution_notes)


class TestPerformanceMonitor:
    """Test PerformanceMonitor functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.performance_monitor = PerformanceMonitor()
    
    def test_initialization(self):
        """Test performance monitor initialization"""
        assert self.performance_monitor.metrics is not None
        assert self.performance_monitor.thresholds is not None
    
    def test_start_timer(self):
        """Test timer start"""
        timer_id = self.performance_monitor.start_timer("test_operation")
        assert timer_id is not None
        assert timer_id in self.performance_monitor.active_timers
    
    def test_stop_timer(self):
        """Test timer stop"""
        timer_id = self.performance_monitor.start_timer("test_operation")
        time.sleep(0.1)  # Small delay to ensure measurable time
        
        duration = self.performance_monitor.stop_timer(timer_id)
        assert duration is not None
        assert duration > 0
        assert timer_id not in self.performance_monitor.active_timers
    
    def test_measure_function_performance(self):
        """Test function performance measurement"""
        def test_function():
            time.sleep(0.1)
            return "test_result"
        
        with patch.object(self.performance_monitor, 'record_performance_metric') as mock_record:
            result = self.performance_monitor.measure_function_performance(
                test_function, "test_function"
            )
            assert result == "test_result"
            mock_record.assert_called_once()
    
    def test_record_performance_metric(self):
        """Test performance metric recording"""
        with patch.object(self.performance_monitor, 'metrics') as mock_metrics:
            self.performance_monitor.record_performance_metric(
                "test_operation", 1.5, {"details": "test"}
            )
            mock_metrics.append.assert_called_once()
    
    def test_get_performance_summary(self):
        """Test performance summary generation"""
        # Add some test metrics
        self.performance_monitor.metrics = [
            {"operation": "test1", "duration": 1.0, "timestamp": time.time()},
            {"operation": "test2", "duration": 2.0, "timestamp": time.time()},
            {"operation": "test1", "duration": 1.5, "timestamp": time.time()}
        ]
        
        summary = self.performance_monitor.get_performance_summary()
        assert summary is not None
        assert "operations" in summary
        assert "average_duration" in summary
        assert "slowest_operations" in summary
    
    def test_check_performance_thresholds(self):
        """Test performance threshold checking"""
        self.performance_monitor.thresholds = {
            "max_response_time": 2.0,
            "max_cpu_usage": 80.0,
            "max_memory_usage": 85.0
        }
        
        current_metrics = {
            "response_time": 1.5,
            "cpu_usage": 75.0,
            "memory_usage": 90.0
        }
        
        violations = self.performance_monitor.check_performance_thresholds(current_metrics)
        assert violations is not None
        assert "memory_usage" in violations  # Should violate threshold
    
    def test_generate_performance_report(self):
        """Test performance report generation"""
        report = self.performance_monitor.generate_performance_report()
        assert report is not None
        assert "summary" in report
        assert "metrics" in report
        assert "recommendations" in report
        assert "timestamp" in report


if __name__ == "__main__":
    pytest.main([__file__])
