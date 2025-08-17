"""
API tests for wellness endpoints
"""
import pytest
from fastapi import status
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from database.schema import WellnessEntry, WellnessEntryType


class TestWellnessAPI:
    """Test wellness API endpoints."""
    
    def test_check_in_success(self, authenticated_client, sample_user):
        """Test successful wellness check-in."""
        check_in_data = {
            "entry_type": "comprehensive",
            "value": 7.5,
            "description": "Feeling good today",
            "mood_score": 8.0,
            "stress_score": 4.0,
            "energy_score": 7.0,
            "sleep_hours": 7.5,
            "sleep_quality": 8.0,
            "work_life_balance": 7.0,
            "social_support": 8.0,
            "physical_activity": 6.0,
            "nutrition_quality": 7.0,
            "productivity_level": 8.0,
            "tags": ["positive", "productive"],
            "factors": {"workload": "moderate", "sleep": "good"},
            "is_anonymous": False
        }
        
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.analyze_wellness_entry.return_value = {
                "recommendations": ["Continue current routine", "Consider more exercise"],
                "risk_indicators": [],
                "insights": ["Good overall wellness score"]
            }
            
            response = authenticated_client.post("/api/wellness/check-in", json=check_in_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["entry_type"] == "comprehensive"
            assert data["value"] == 7.5
            assert data["mood_score"] == 8.0
            assert data["user_id"] == sample_user.id
            assert "recommendations" in data
            assert "risk_indicators" in data
            assert "insights" in data
    
    def test_quick_mood_check_in(self, authenticated_client, sample_user):
        """Test quick mood check-in."""
        mood_data = {
            "entry_type": "mood",
            "value": 8.0,
            "description": "Feeling great!"
        }
        
        response = authenticated_client.post("/api/wellness/mood", json=mood_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["entry_type"] == "mood"
        assert data["value"] == 8.0
        assert data["user_id"] == sample_user.id
    
    def test_check_in_invalid_data(self, authenticated_client):
        """Test check-in with invalid data."""
        # Missing required fields
        response = authenticated_client.post("/api/wellness/check-in", json={
            "description": "Feeling good"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_check_in_invalid_value_range(self, authenticated_client):
        """Test check-in with invalid value range."""
        response = authenticated_client.post("/api/wellness/check-in", json={
            "entry_type": "mood",
            "value": 15.0,  # Should be 1-10
            "description": "Test"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_check_in_unauthenticated(self, client):
        """Test check-in without authentication."""
        response = client.post("/api/wellness/check-in", json={
            "entry_type": "mood",
            "value": 7.0,
            "description": "Test"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_wellness_history(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test getting wellness history."""
        # Generate some wellness entries
        generate_wellness_entries(5)
        
        response = authenticated_client.get("/api/wellness/history")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "entries" in data
        assert "pagination" in data
        assert len(data["entries"]) > 0
        assert data["entries"][0]["user_id"] == sample_user.id
    
    def test_get_wellness_history_with_filters(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test getting wellness history with filters."""
        generate_wellness_entries(10)
        
        response = authenticated_client.get("/api/wellness/history?entry_type=mood&limit=5&offset=0")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "entries" in data
        assert len(data["entries"]) <= 5
    
    def test_get_wellness_analytics(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test getting wellness analytics."""
        generate_wellness_entries(20)
        
        with patch('api.routes.wellness.WellnessAnalytics') as mock_analytics:
            mock_instance = Mock()
            mock_analytics.return_value = mock_instance
            mock_instance.get_user_analytics.return_value = {
                "average_mood": 7.2,
                "average_stress": 5.8,
                "average_energy": 6.5,
                "trends": {"mood": "increasing", "stress": "decreasing"},
                "insights": ["Mood has improved over time", "Stress levels are manageable"]
            }
            
            response = authenticated_client.get("/api/wellness/analytics")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "average_mood" in data
            assert "trends" in data
            assert "insights" in data
    
    def test_get_wellness_recommendations(self, authenticated_client, sample_user):
        """Test getting wellness recommendations."""
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.get_recommendations.return_value = {
                "resources": [
                    {"id": "1", "title": "Stress Management Guide", "type": "resource"},
                    {"id": "2", "title": "Mindfulness Exercise", "type": "exercise"}
                ],
                "actions": [
                    {"action": "Take a 5-minute break", "priority": "high"},
                    {"action": "Practice deep breathing", "priority": "medium"}
                ],
                "insights": ["You might benefit from stress management techniques"]
            }
            
            response = authenticated_client.get("/api/wellness/recommendations")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "resources" in data
            assert "actions" in data
            assert "insights" in data
    
    def test_start_conversation(self, authenticated_client, sample_user):
        """Test starting a wellness conversation."""
        conversation_data = {
            "message": "I've been feeling stressed lately",
            "context": "work-related stress"
        }
        
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.start_conversation.return_value = {
                "conversation_id": "conv_123",
                "response": "I understand you're feeling stressed. Let's talk about what's been happening at work.",
                "suggestions": ["Would you like to discuss specific stressors?", "Should we explore coping strategies?"]
            }
            
            response = authenticated_client.post("/api/wellness/conversation", json=conversation_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "conversation_id" in data
            assert "response" in data
            assert "suggestions" in data
    
    def test_continue_conversation(self, authenticated_client, sample_user):
        """Test continuing a wellness conversation."""
        message_data = {
            "conversation_id": "conv_123",
            "message": "Yes, I've been working long hours"
        }
        
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.continue_conversation.return_value = {
                "response": "Long hours can definitely contribute to stress. Let's explore some strategies to help manage your workload.",
                "suggestions": ["Time management techniques", "Setting boundaries"],
                "risk_assessment": {"level": "medium", "factors": ["workload", "hours"]}
            }
            
            response = authenticated_client.post("/api/wellness/conversation/continue", json=message_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "response" in data
            assert "suggestions" in data
            assert "risk_assessment" in data
    
    def test_get_conversation_history(self, authenticated_client, sample_user):
        """Test getting conversation history."""
        response = authenticated_client.get("/api/wellness/conversations")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "conversations" in data
        assert "pagination" in data
    
    def test_get_conversation_summary(self, authenticated_client, sample_user):
        """Test getting conversation summary."""
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.get_conversation_summary.return_value = {
                "summary": "Discussed work-related stress and explored coping strategies",
                "key_topics": ["workload", "stress management", "boundaries"],
                "recommendations": ["Practice time management", "Set work boundaries"],
                "follow_up": "Schedule a follow-up in one week"
            }
            
            response = authenticated_client.get("/api/wellness/conversation/summary?conversation_id=conv_123")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "summary" in data
            assert "key_topics" in data
            assert "recommendations" in data
            assert "follow_up" in data
    
    def test_get_wellness_stats(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test getting wellness statistics."""
        generate_wellness_entries(15)
        
        response = authenticated_client.get("/api/wellness/stats")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_entries" in data
        assert "average_scores" in data
        assert "streak_days" in data
        assert "completion_rate" in data
    
    def test_anonymous_check_in(self, authenticated_client, sample_user):
        """Test anonymous wellness check-in."""
        check_in_data = {
            "entry_type": "stress",
            "value": 6.0,
            "description": "Feeling overwhelmed",
            "is_anonymous": True
        }
        
        response = authenticated_client.post("/api/wellness/check-in", json=check_in_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["is_anonymous"] is True
        # Should not return user_id for anonymous entries
        assert "user_id" not in data
    
    def test_check_in_with_tags_and_factors(self, authenticated_client, sample_user):
        """Test check-in with tags and contributing factors."""
        check_in_data = {
            "entry_type": "comprehensive",
            "value": 6.5,
            "description": "Mixed feelings today",
            "tags": ["work", "stress", "productive"],
            "factors": {
                "workload": "high",
                "sleep": "poor",
                "social": "good"
            }
        }
        
        response = authenticated_client.post("/api/wellness/check-in", json=check_in_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["tags"] == ["work", "stress", "productive"]
        assert data["factors"] == {"workload": "high", "sleep": "poor", "social": "good"}
    
    def test_get_wellness_history_by_date_range(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test getting wellness history with date range filter."""
        generate_wellness_entries(10)
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        response = authenticated_client.get(
            f"/api/wellness/history?start_date={start_date}&end_date={end_date}"
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "entries" in data
    
    def test_get_wellness_analytics_by_period(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test getting wellness analytics for specific period."""
        generate_wellness_entries(30)
        
        with patch('api.routes.wellness.WellnessAnalytics') as mock_analytics:
            mock_instance = Mock()
            mock_analytics.return_value = mock_instance
            mock_instance.get_user_analytics.return_value = {
                "period": "last_30_days",
                "average_mood": 7.1,
                "mood_trend": "stable",
                "stress_pattern": "weekday_peaks",
                "recommendations": ["Consider weekend stress relief activities"]
            }
            
            response = authenticated_client.get("/api/wellness/analytics?period=30_days")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "period" in data
            assert "mood_trend" in data
            assert "stress_pattern" in data
    
    def test_conversation_with_context(self, authenticated_client, sample_user):
        """Test conversation with additional context."""
        conversation_data = {
            "message": "I'm having trouble sleeping",
            "context": "sleep_issues",
            "mood_score": 4.0,
            "stress_level": 8.0,
            "recent_events": ["work deadline", "family stress"]
        }
        
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.start_conversation.return_value = {
                "conversation_id": "conv_456",
                "response": "I see you're experiencing sleep issues, which can be related to stress and recent events. Let's explore some sleep hygiene strategies.",
                "suggestions": ["Sleep hygiene practices", "Stress reduction techniques", "Professional consultation"],
                "priority": "high"
            }
            
            response = authenticated_client.post("/api/wellness/conversation", json=conversation_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "priority" in data
            assert "high" in data["suggestions"][0]
    
    def test_wellness_entry_validation_rules(self, authenticated_client):
        """Test wellness entry validation rules."""
        # Test value range validation
        invalid_entries = [
            {"entry_type": "mood", "value": 0.0, "description": "Test"},  # Too low
            {"entry_type": "mood", "value": 11.0, "description": "Test"},  # Too high
            {"entry_type": "mood", "value": -1.0, "description": "Test"},  # Negative
        ]
        
        for entry in invalid_entries:
            response = authenticated_client.post("/api/wellness/check-in", json=entry)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test valid entries
        valid_entries = [
            {"entry_type": "mood", "value": 1.0, "description": "Test"},
            {"entry_type": "mood", "value": 10.0, "description": "Test"},
            {"entry_type": "mood", "value": 5.5, "description": "Test"},
        ]
        
        for entry in valid_entries:
            response = authenticated_client.post("/api/wellness/check-in", json=entry)
            assert response.status_code == status.HTTP_201_CREATED
    
    def test_wellness_entry_types(self, authenticated_client):
        """Test different wellness entry types."""
        entry_types = ["mood", "stress", "energy", "sleep_quality", "work_life_balance", "comprehensive", "quick_check"]
        
        for entry_type in entry_types:
            entry_data = {
                "entry_type": entry_type,
                "value": 7.0,
                "description": f"Test {entry_type} entry"
            }
            
            response = authenticated_client.post("/api/wellness/check-in", json=entry_data)
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["entry_type"] == entry_type
    
    def test_wellness_analytics_performance(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test wellness analytics performance with large dataset."""
        # Generate a larger dataset
        generate_wellness_entries(100)
        
        with patch('api.routes.wellness.WellnessAnalytics') as mock_analytics:
            mock_instance = Mock()
            mock_analytics.return_value = mock_instance
            mock_instance.get_user_analytics.return_value = {
                "average_mood": 7.0,
                "total_entries": 100,
                "processing_time": "0.5s"
            }
            
            response = authenticated_client.get("/api/wellness/analytics")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "average_mood" in data
            assert "total_entries" in data
    
    def test_conversation_error_handling(self, authenticated_client, sample_user):
        """Test conversation error handling."""
        conversation_data = {
            "message": "Test message"
        }
        
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.start_conversation.side_effect = Exception("Service unavailable")
            
            response = authenticated_client.post("/api/wellness/conversation", json=conversation_data)
            
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            data = response.json()
            assert "error" in data["detail"].lower()
    
    def test_wellness_recommendations_personalization(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test personalized wellness recommendations."""
        # Generate some wellness history
        generate_wellness_entries(10)
        
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.get_recommendations.return_value = {
                "personalized_resources": [
                    {"id": "1", "title": "Stress Management for Engineers", "relevance": 0.9},
                    {"id": "2", "title": "Work-Life Balance Guide", "relevance": 0.8}
                ],
                "personalized_actions": [
                    {"action": "Take regular breaks", "confidence": 0.95},
                    {"action": "Practice mindfulness", "confidence": 0.87}
                ],
                "personalization_factors": ["role", "department", "wellness_history"]
            }
            
            response = authenticated_client.get("/api/wellness/recommendations")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "personalized_resources" in data
            assert "personalized_actions" in data
            assert "personalization_factors" in data
