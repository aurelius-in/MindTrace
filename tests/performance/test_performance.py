"""
Performance tests for the Enterprise Employee Wellness AI application
"""
import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import status
from unittest.mock import patch
import statistics


class TestDatabasePerformance:
    """Test database performance under various loads."""
    
    def test_bulk_wellness_entry_creation(self, authenticated_client, sample_user, performance_test_data):
        """Test bulk creation of wellness entries."""
        users, _ = performance_test_data(10, 0)  # 10 users, no entries
        
        start_time = time.time()
        
        # Create 100 wellness entries
        entries_created = 0
        for i in range(100):
            response = authenticated_client.post("/api/wellness/check-in", json={
                "entry_type": "mood",
                "value": 7.0,
                "description": f"Bulk test entry {i}"
            })
            
            if response.status_code == status.HTTP_201_CREATED:
                entries_created += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Performance assertions
        assert entries_created >= 95  # At least 95% success rate
        assert duration < 30.0  # Should complete within 30 seconds
        assert duration / entries_created < 0.3  # Average time per entry < 300ms
    
    def test_wellness_history_query_performance(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test wellness history query performance."""
        # Generate test data
        generate_wellness_entries(1000)
        
        start_time = time.time()
        
        response = authenticated_client.get("/api/wellness/history?limit=100")
        
        end_time = time.time()
        duration = end_time - start_time
        
        assert response.status_code == status.HTTP_200_OK
        assert duration < 2.0  # Should complete within 2 seconds
        
        data = response.json()
        assert len(data["entries"]) <= 100
    
    def test_concurrent_user_operations(self, client, performance_test_data):
        """Test concurrent operations from multiple users."""
        users, _ = performance_test_data(50, 0)  # 50 users
        
        def user_operation(user_index):
            # Login
            login_response = client.post("/api/auth/login", data={
                "username": f"user{user_index}@example.com",
                "password": "testpassword123"
            })
            
            if login_response.status_code != status.HTTP_200_OK:
                return False
            
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Create wellness entry
            entry_response = client.post("/api/wellness/check-in", json={
                "entry_type": "mood",
                "value": 7.0,
                "description": f"Concurrent test entry {user_index}"
            }, headers=headers)
            
            # Get history
            history_response = client.get("/api/wellness/history", headers=headers)
            
            return (entry_response.status_code == status.HTTP_201_CREATED and 
                   history_response.status_code == status.HTTP_200_OK)
        
        start_time = time.time()
        
        # Execute concurrent operations
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(user_operation, range(50)))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Performance assertions
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.8  # At least 80% success rate
        assert duration < 60.0  # Should complete within 60 seconds
        assert duration / 50 < 1.2  # Average time per user < 1.2 seconds
    
    def test_database_connection_pool_performance(self, authenticated_client, sample_user):
        """Test database connection pool performance under load."""
        start_time = time.time()
        
        # Make many concurrent requests to test connection pool
        def make_request():
            return authenticated_client.get("/api/wellness/history")
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            responses = list(executor.map(lambda _: make_request(), range(100)))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Check all responses
        successful_responses = sum(1 for r in responses if r.status_code == status.HTTP_200_OK)
        success_rate = successful_responses / len(responses)
        
        assert success_rate >= 0.95  # At least 95% success rate
        assert duration < 30.0  # Should complete within 30 seconds
        assert duration / 100 < 0.3  # Average time per request < 300ms


class TestAPIPerformance:
    """Test API endpoint performance."""
    
    def test_wellness_check_in_performance(self, authenticated_client, sample_user):
        """Test wellness check-in endpoint performance."""
        response_times = []
        
        for i in range(50):
            start_time = time.time()
            
            response = authenticated_client.post("/api/wellness/check-in", json={
                "entry_type": "mood",
                "value": 7.0,
                "description": f"Performance test entry {i}"
            })
            
            end_time = time.time()
            response_times.append(end_time - start_time)
            
            assert response.status_code == status.HTTP_201_CREATED
        
        # Performance analysis
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        max_response_time = max(response_times)
        
        assert avg_response_time < 0.5  # Average response time < 500ms
        assert p95_response_time < 1.0  # 95th percentile < 1 second
        assert max_response_time < 2.0  # Maximum response time < 2 seconds
    
    def test_wellness_analytics_performance(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test wellness analytics endpoint performance."""
        # Generate test data
        generate_wellness_entries(500)
        
        response_times = []
        
        for i in range(20):
            start_time = time.time()
            
            with patch('api.routes.wellness.WellnessAnalytics') as mock_analytics:
                mock_instance = Mock()
                mock_analytics.return_value = mock_instance
                mock_instance.get_user_analytics.return_value = {
                    "average_mood": 7.0,
                    "trends": {"mood": "stable"},
                    "insights": ["Good overall wellness"]
                }
                
                response = authenticated_client.get("/api/wellness/analytics")
            
            end_time = time.time()
            response_times.append(end_time - start_time)
            
            assert response.status_code == status.HTTP_200_OK
        
        # Performance analysis
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]
        
        assert avg_response_time < 1.0  # Average response time < 1 second
        assert p95_response_time < 2.0  # 95th percentile < 2 seconds
    
    def test_conversation_performance(self, authenticated_client, sample_user):
        """Test conversation endpoint performance."""
        response_times = []
        
        for i in range(30):
            start_time = time.time()
            
            with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
                mock_instance = Mock()
                mock_orchestrator.return_value = mock_instance
                mock_instance.start_conversation.return_value = {
                    "conversation_id": f"conv_{i}",
                    "response": f"Test response {i}",
                    "suggestions": ["Test suggestion"]
                }
                
                response = authenticated_client.post("/api/wellness/conversation", json={
                    "message": f"Test message {i}"
                })
            
            end_time = time.time()
            response_times.append(end_time - start_time)
            
            assert response.status_code == status.HTTP_200_OK
        
        # Performance analysis
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]
        
        assert avg_response_time < 1.5  # Average response time < 1.5 seconds
        assert p95_response_time < 3.0  # 95th percentile < 3 seconds
    
    def test_resource_library_performance(self, authenticated_client, sample_user):
        """Test resource library endpoint performance."""
        response_times = []
        
        for i in range(40):
            start_time = time.time()
            
            response = authenticated_client.get("/api/resources/")
            
            end_time = time.time()
            response_times.append(end_time - start_time)
            
            assert response.status_code == status.HTTP_200_OK
        
        # Performance analysis
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]
        
        assert avg_response_time < 0.3  # Average response time < 300ms
        assert p95_response_time < 0.8  # 95th percentile < 800ms


class TestSystemScalability:
    """Test system scalability under various loads."""
    
    def test_memory_usage_under_load(self, authenticated_client, sample_user, performance_test_data):
        """Test memory usage under load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Generate load
        users, entries = performance_test_data(100, 1000)
        
        # Perform operations
        for i in range(200):
            authenticated_client.post("/api/wellness/check-in", json={
                "entry_type": "mood",
                "value": 7.0,
                "description": f"Memory test entry {i}"
            })
            
            authenticated_client.get("/api/wellness/history")
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory should not increase excessively
        assert memory_increase < 100  # Less than 100MB increase
    
    def test_cpu_usage_under_load(self, authenticated_client, sample_user):
        """Test CPU usage under load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Monitor CPU usage during load
        cpu_percentages = []
        
        for i in range(50):
            start_time = time.time()
            
            # Perform CPU-intensive operations
            for j in range(10):
                authenticated_client.post("/api/wellness/check-in", json={
                    "entry_type": "comprehensive",
                    "value": 7.0,
                    "description": f"CPU test entry {i}_{j}",
                    "mood_score": 7.0,
                    "stress_score": 5.0,
                    "energy_score": 6.0
                })
            
            # Measure CPU usage
            cpu_percent = process.cpu_percent(interval=0.1)
            cpu_percentages.append(cpu_percent)
            
            # Ensure we don't exceed reasonable time
            if time.time() - start_time > 10:
                break
        
        # CPU usage should be reasonable
        avg_cpu = statistics.mean(cpu_percentages)
        max_cpu = max(cpu_percentages)
        
        assert avg_cpu < 80  # Average CPU usage < 80%
        assert max_cpu < 95  # Maximum CPU usage < 95%
    
    def test_concurrent_user_simulation(self, client, performance_test_data):
        """Simulate concurrent users accessing the system."""
        users, _ = performance_test_data(200, 0)  # 200 users
        
        def simulate_user(user_id):
            # Login
            login_response = client.post("/api/auth/login", data={
                "username": f"user{user_id}@example.com",
                "password": "testpassword123"
            })
            
            if login_response.status_code != status.HTTP_200_OK:
                return False
            
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Perform typical user actions
            actions = [
                lambda: client.get("/api/wellness/history", headers=headers),
                lambda: client.post("/api/wellness/check-in", json={
                    "entry_type": "mood",
                    "value": 7.0,
                    "description": "Concurrent user test"
                }, headers=headers),
                lambda: client.get("/api/resources/", headers=headers),
                lambda: client.get("/api/wellness/stats", headers=headers)
            ]
            
            success_count = 0
            for action in actions:
                try:
                    response = action()
                    if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                        success_count += 1
                except Exception:
                    pass
            
            return success_count >= 2  # At least 2 successful actions
        
        start_time = time.time()
        
        # Simulate concurrent users
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(simulate_user, range(200)))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Performance assertions
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.7  # At least 70% success rate
        assert duration < 120.0  # Should complete within 2 minutes
        assert duration / 200 < 0.6  # Average time per user < 600ms


class TestCachingPerformance:
    """Test caching performance improvements."""
    
    def test_wellness_history_caching(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test caching performance for wellness history."""
        generate_wellness_entries(100)
        
        # First request (cache miss)
        start_time = time.time()
        response1 = authenticated_client.get("/api/wellness/history")
        first_request_time = time.time() - start_time
        
        assert response1.status_code == status.HTTP_200_OK
        
        # Second request (cache hit)
        start_time = time.time()
        response2 = authenticated_client.get("/api/wellness/history")
        second_request_time = time.time() - start_time
        
        assert response2.status_code == status.HTTP_200_OK
        
        # Cached request should be faster
        if second_request_time < first_request_time:
            improvement = (first_request_time - second_request_time) / first_request_time
            assert improvement > 0.1  # At least 10% improvement
    
    def test_analytics_caching(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test caching performance for analytics."""
        generate_wellness_entries(200)
        
        with patch('api.routes.wellness.WellnessAnalytics') as mock_analytics:
            mock_instance = Mock()
            mock_analytics.return_value = mock_instance
            mock_instance.get_user_analytics.return_value = {
                "average_mood": 7.0,
                "trends": {"mood": "stable"},
                "insights": ["Good overall wellness"]
            }
            
            # First request
            start_time = time.time()
            response1 = authenticated_client.get("/api/wellness/analytics")
            first_request_time = time.time() - start_time
            
            assert response1.status_code == status.HTTP_200_OK
            
            # Second request
            start_time = time.time()
            response2 = authenticated_client.get("/api/wellness/analytics")
            second_request_time = time.time() - start_time
            
            assert response2.status_code == status.HTTP_200_OK
            
            # Cached request should be faster
            if second_request_time < first_request_time:
                improvement = (first_request_time - second_request_time) / first_request_time
                assert improvement > 0.2  # At least 20% improvement


class TestLoadTesting:
    """Load testing scenarios."""
    
    def test_peak_load_simulation(self, client, performance_test_data):
        """Simulate peak load conditions."""
        users, _ = performance_test_data(500, 0)  # 500 users
        
        def peak_load_operation(user_id):
            # Login
            login_response = client.post("/api/auth/login", data={
                "username": f"user{user_id}@example.com",
                "password": "testpassword123"
            })
            
            if login_response.status_code != status.HTTP_200_OK:
                return False
            
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Perform peak load operations
            operations = [
                client.get("/api/wellness/history", headers=headers),
                client.post("/api/wellness/check-in", json={
                    "entry_type": "mood",
                    "value": 7.0,
                    "description": "Peak load test"
                }, headers=headers),
                client.get("/api/resources/", headers=headers),
                client.get("/api/wellness/stats", headers=headers)
            ]
            
            successful_ops = sum(1 for op in operations if op.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED])
            return successful_ops >= 3  # At least 3 successful operations
        
        start_time = time.time()
        
        # Simulate peak load
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = list(executor.map(peak_load_operation, range(500)))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Peak load performance assertions
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.6  # At least 60% success rate under peak load
        assert duration < 300.0  # Should complete within 5 minutes
        assert duration / 500 < 0.6  # Average time per user < 600ms
    
    def test_stress_testing(self, authenticated_client, sample_user):
        """Stress testing with extreme load."""
        response_times = []
        errors = 0
        
        # Extreme load test
        for i in range(1000):
            start_time = time.time()
            
            try:
                response = authenticated_client.post("/api/wellness/check-in", json={
                    "entry_type": "mood",
                    "value": 7.0,
                    "description": f"Stress test entry {i}"
                })
                
                if response.status_code == status.HTTP_201_CREATED:
                    response_times.append(time.time() - start_time)
                else:
                    errors += 1
                    
            except Exception:
                errors += 1
        
        # Stress test assertions
        if response_times:
            avg_response_time = statistics.mean(response_times)
            p95_response_time = statistics.quantiles(response_times, n=20)[18]
            
            assert avg_response_time < 2.0  # Average response time < 2 seconds
            assert p95_response_time < 5.0  # 95th percentile < 5 seconds
        
        error_rate = errors / 1000
        assert error_rate < 0.1  # Error rate < 10%
