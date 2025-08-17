"""
Integration tests for the Enterprise Employee Wellness AI application
"""
import pytest
from fastapi import status
from unittest.mock import patch, Mock
from datetime import datetime, timedelta


class TestCompleteUserWorkflow:
    """Test complete user workflow from registration to wellness tracking."""
    
    def test_complete_user_journey(self, client, db_session):
        """Test complete user journey from registration to wellness tracking."""
        # 1. User Registration
        register_data = {
            "email": "journey@example.com",
            "password": "journey123",
            "first_name": "Journey",
            "last_name": "User",
            "role": "employee",
            "department": "Engineering",
            "position": "Software Engineer"
        }
        
        response = client.post("/api/auth/register", json=register_data)
        assert response.status_code == status.HTTP_201_CREATED
        user_data = response.json()
        assert user_data["email"] == "journey@example.com"
        
        # 2. User Login
        login_response = client.post("/api/auth/login", data={
            "username": "journey@example.com",
            "password": "journey123"
        })
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get User Profile
        profile_response = client.get("/api/auth/me", headers=headers)
        assert profile_response.status_code == status.HTTP_200_OK
        profile_data = profile_response.json()
        assert profile_data["email"] == "journey@example.com"
        
        # 4. Create Wellness Check-in
        check_in_data = {
            "entry_type": "comprehensive",
            "value": 7.5,
            "description": "Feeling good on my first day",
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
            "tags": ["first-day", "positive"],
            "factors": {"workload": "moderate", "environment": "friendly"}
        }
        
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.analyze_wellness_entry.return_value = {
                "recommendations": ["Great start! Keep up the positive energy"],
                "risk_indicators": [],
                "insights": ["Good overall wellness score for first day"]
            }
            
            check_in_response = client.post("/api/wellness/check-in", json=check_in_data, headers=headers)
            assert check_in_response.status_code == status.HTTP_201_CREATED
            check_in_result = check_in_response.json()
            assert check_in_result["entry_type"] == "comprehensive"
            assert "recommendations" in check_in_result
        
        # 5. Get Wellness History
        history_response = client.get("/api/wellness/history", headers=headers)
        assert history_response.status_code == status.HTTP_200_OK
        history_data = history_response.json()
        assert len(history_data["entries"]) >= 1
        assert history_data["entries"][0]["entry_type"] == "comprehensive"
        
        # 6. Get Wellness Analytics
        with patch('api.routes.wellness.WellnessAnalytics') as mock_analytics:
            mock_instance = Mock()
            mock_analytics.return_value = mock_instance
            mock_instance.get_user_analytics.return_value = {
                "average_mood": 8.0,
                "average_stress": 4.0,
                "average_energy": 7.0,
                "trends": {"mood": "stable", "stress": "low"},
                "insights": ["Good wellness baseline established"]
            }
            
            analytics_response = client.get("/api/wellness/analytics", headers=headers)
            assert analytics_response.status_code == status.HTTP_200_OK
            analytics_data = analytics_response.json()
            assert "average_mood" in analytics_data
            assert "trends" in analytics_data
        
        # 7. Get Wellness Recommendations
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.get_recommendations.return_value = {
                "resources": [
                    {"id": "1", "title": "Getting Started Guide", "type": "resource"}
                ],
                "actions": [
                    {"action": "Set up regular check-ins", "priority": "high"}
                ],
                "insights": ["Establishing a routine will help maintain wellness"]
            }
            
            recommendations_response = client.get("/api/wellness/recommendations", headers=headers)
            assert recommendations_response.status_code == status.HTTP_200_OK
            recommendations_data = recommendations_response.json()
            assert "resources" in recommendations_data
            assert "actions" in recommendations_data
        
        # 8. Start Wellness Conversation
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.start_conversation.return_value = {
                "conversation_id": "conv_journey_1",
                "response": "Welcome to your wellness journey! How can I help you today?",
                "suggestions": ["Tell me about your goals", "Discuss any concerns"]
            }
            
            conversation_response = client.post("/api/wellness/conversation", json={
                "message": "Hello, I'm new here and want to improve my wellness"
            }, headers=headers)
            assert conversation_response.status_code == status.HTTP_200_OK
            conversation_data = conversation_response.json()
            assert "conversation_id" in conversation_data
            assert "response" in conversation_data
        
        # 9. Get Wellness Statistics
        stats_response = client.get("/api/wellness/stats", headers=headers)
        assert stats_response.status_code == status.HTTP_200_OK
        stats_data = stats_response.json()
        assert "total_entries" in stats_data
        assert "average_scores" in stats_data
        
        # 10. Logout
        logout_response = client.post("/api/auth/logout", headers=headers)
        assert logout_response.status_code == status.HTTP_200_OK
        
        # 11. Verify token is invalidated
        invalid_profile_response = client.get("/api/auth/me", headers=headers)
        assert invalid_profile_response.status_code == status.HTTP_401_UNAUTHORIZED


class TestWellnessTrackingWorkflow:
    """Test complete wellness tracking workflow."""
    
    def test_wellness_tracking_complete_cycle(self, authenticated_client, sample_user):
        """Test complete wellness tracking cycle."""
        # 1. Create multiple wellness entries over time
        entries_data = [
            {
                "entry_type": "mood",
                "value": 8.0,
                "description": "Great mood today",
                "tags": ["positive", "productive"]
            },
            {
                "entry_type": "stress",
                "value": 6.0,
                "description": "Some work stress",
                "tags": ["work", "stress"]
            },
            {
                "entry_type": "comprehensive",
                "value": 7.0,
                "description": "Overall feeling good",
                "mood_score": 7.5,
                "stress_score": 5.0,
                "energy_score": 7.0,
                "tags": ["balanced", "stable"]
            }
        ]
        
        created_entries = []
        for entry_data in entries_data:
            with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
                mock_instance = Mock()
                mock_orchestrator.return_value = mock_instance
                mock_instance.analyze_wellness_entry.return_value = {
                    "recommendations": ["Continue current routine"],
                    "risk_indicators": [],
                    "insights": ["Good wellness pattern"]
                }
                
                response = authenticated_client.post("/api/wellness/check-in", json=entry_data)
                assert response.status_code == status.HTTP_201_CREATED
                created_entries.append(response.json())
        
        # 2. Get wellness history with different filters
        history_response = authenticated_client.get("/api/wellness/history")
        assert history_response.status_code == status.HTTP_200_OK
        history_data = history_response.json()
        assert len(history_data["entries"]) >= 3
        
        # Filter by entry type
        mood_history = authenticated_client.get("/api/wellness/history?entry_type=mood")
        assert mood_history.status_code == status.HTTP_200_OK
        mood_data = mood_history.json()
        assert all(entry["entry_type"] == "mood" for entry in mood_data["entries"])
        
        # 3. Get comprehensive analytics
        with patch('api.routes.wellness.WellnessAnalytics') as mock_analytics:
            mock_instance = Mock()
            mock_analytics.return_value = mock_instance
            mock_instance.get_user_analytics.return_value = {
                "average_mood": 7.5,
                "average_stress": 5.5,
                "average_energy": 7.0,
                "trends": {
                    "mood": "stable",
                    "stress": "moderate",
                    "energy": "good"
                },
                "patterns": {
                    "weekly_pattern": "weekend_improvement",
                    "daily_pattern": "morning_peak"
                },
                "insights": [
                    "Mood is generally positive",
                    "Stress levels are manageable",
                    "Energy levels are consistent"
                ],
                "recommendations": [
                    "Continue current wellness routine",
                    "Consider stress management techniques",
                    "Maintain good sleep habits"
                ]
            }
            
            analytics_response = authenticated_client.get("/api/wellness/analytics")
            assert analytics_response.status_code == status.HTTP_200_OK
            analytics_data = analytics_response.json()
            assert "trends" in analytics_data
            assert "patterns" in analytics_data
            assert "insights" in analytics_data
        
        # 4. Get personalized recommendations
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.get_recommendations.return_value = {
                "personalized_resources": [
                    {
                        "id": "1",
                        "title": "Stress Management for Engineers",
                        "relevance": 0.9,
                        "type": "resource"
                    },
                    {
                        "id": "2",
                        "title": "Mood Enhancement Techniques",
                        "relevance": 0.8,
                        "type": "exercise"
                    }
                ],
                "personalized_actions": [
                    {
                        "action": "Practice 5-minute breathing exercises",
                        "priority": "high",
                        "confidence": 0.95
                    },
                    {
                        "action": "Take regular breaks every 2 hours",
                        "priority": "medium",
                        "confidence": 0.87
                    }
                ],
                "personalization_factors": ["role", "department", "wellness_history"]
            }
            
            recommendations_response = authenticated_client.get("/api/wellness/recommendations")
            assert recommendations_response.status_code == status.HTTP_200_OK
            recommendations_data = recommendations_response.json()
            assert "personalized_resources" in recommendations_data
            assert "personalized_actions" in recommendations_data
        
        # 5. Get wellness statistics
        stats_response = authenticated_client.get("/api/wellness/stats")
        assert stats_response.status_code == status.HTTP_200_OK
        stats_data = stats_response.json()
        assert "total_entries" in stats_data
        assert "average_scores" in stats_data
        assert "streak_days" in stats_data
        assert "completion_rate" in stats_data


class TestConversationWorkflow:
    """Test complete conversation workflow."""
    
    def test_conversation_complete_cycle(self, authenticated_client, sample_user):
        """Test complete conversation cycle."""
        # 1. Start a conversation
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.start_conversation.return_value = {
                "conversation_id": "conv_test_1",
                "response": "Hello! I'm here to support your wellness journey. What would you like to discuss today?",
                "suggestions": [
                    "I'm feeling stressed about work",
                    "I want to improve my sleep",
                    "I need help with work-life balance"
                ]
            }
            
            start_response = authenticated_client.post("/api/wellness/conversation", json={
                "message": "Hello, I need some wellness support"
            })
            assert start_response.status_code == status.HTTP_200_OK
            start_data = start_response.json()
            conversation_id = start_data["conversation_id"]
            assert "response" in start_data
            assert "suggestions" in start_data
        
        # 2. Continue the conversation
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.continue_conversation.return_value = {
                "response": "I understand you're feeling stressed about work. Let's explore what's causing this stress and find some strategies to help you manage it.",
                "suggestions": [
                    "Tell me more about your work situation",
                    "Let's discuss stress management techniques",
                    "Would you like to explore time management strategies?"
                ],
                "risk_assessment": {
                    "level": "medium",
                    "factors": ["workload", "stress"],
                    "recommendations": ["Consider stress management techniques"]
                }
            }
            
            continue_response = authenticated_client.post("/api/wellness/conversation/continue", json={
                "conversation_id": conversation_id,
                "message": "I'm feeling stressed about work deadlines"
            })
            assert continue_response.status_code == status.HTTP_200_OK
            continue_data = continue_response.json()
            assert "response" in continue_data
            assert "risk_assessment" in continue_data
        
        # 3. Get conversation history
        history_response = authenticated_client.get("/api/wellness/conversations")
        assert history_response.status_code == status.HTTP_200_OK
        history_data = history_response.json()
        assert "conversations" in history_data
        assert "pagination" in history_data
        
        # 4. Get conversation summary
        with patch('api.routes.wellness.AgentOrchestrator') as mock_orchestrator:
            mock_instance = Mock()
            mock_orchestrator.return_value = mock_instance
            mock_instance.get_conversation_summary.return_value = {
                "summary": "Discussed work-related stress and explored coping strategies",
                "key_topics": ["work stress", "deadlines", "coping strategies"],
                "recommendations": [
                    "Practice time management",
                    "Set realistic deadlines",
                    "Use stress reduction techniques"
                ],
                "follow_up": "Schedule a follow-up conversation in one week",
                "risk_level": "medium",
                "action_items": [
                    "Implement time management strategies",
                    "Practice daily stress reduction exercises",
                    "Monitor stress levels regularly"
                ]
            }
            
            summary_response = authenticated_client.get(f"/api/wellness/conversation/summary?conversation_id={conversation_id}")
            assert summary_response.status_code == status.HTTP_200_OK
            summary_data = summary_response.json()
            assert "summary" in summary_data
            assert "key_topics" in summary_data
            assert "recommendations" in summary_data
            assert "action_items" in summary_data


class TestResourceLibraryWorkflow:
    """Test complete resource library workflow."""
    
    def test_resource_library_complete_cycle(self, authenticated_client, sample_user):
        """Test complete resource library cycle."""
        # 1. Browse resources
        resources_response = authenticated_client.get("/api/resources/")
        assert resources_response.status_code == status.HTTP_200_OK
        resources_data = resources_response.json()
        assert "resources" in resources_data
        assert "pagination" in resources_data
        
        # 2. Filter resources by category
        stress_resources = authenticated_client.get("/api/resources/?category=stress_management")
        assert stress_resources.status_code == status.HTTP_200_OK
        stress_data = stress_resources.json()
        if stress_data["resources"]:
            assert all(resource["category"] == "stress_management" for resource in stress_data["resources"])
        
        # 3. Get resource details
        if resources_data["resources"]:
            resource_id = resources_data["resources"][0]["id"]
            detail_response = authenticated_client.get(f"/api/resources/{resource_id}")
            assert detail_response.status_code == status.HTTP_200_OK
            detail_data = detail_response.json()
            assert detail_data["id"] == resource_id
            assert "title" in detail_data
            assert "description" in detail_data
        
        # 4. Interact with resource
        if resources_data["resources"]:
            resource_id = resources_data["resources"][0]["id"]
            interaction_response = authenticated_client.post(f"/api/resources/{resource_id}/interact", json={
                "interaction_type": "view",
                "duration_seconds": 120,
                "rating": 4,
                "feedback": "Very helpful resource"
            })
            assert interaction_response.status_code == status.HTTP_200_OK
        
        # 5. Get user interactions
        interactions_response = authenticated_client.get("/api/resources/user/interactions")
        assert interactions_response.status_code == status.HTTP_200_OK
        interactions_data = interactions_response.json()
        assert "interactions" in interactions_data
        
        # 6. Get resource recommendations
        recommendations_response = authenticated_client.get("/api/resources/recommendations")
        assert recommendations_response.status_code == status.HTTP_200_OK
        recommendations_data = recommendations_response.json()
        assert "recommended_resources" in recommendations_data


class TestAnalyticsWorkflow:
    """Test complete analytics workflow."""
    
    def test_analytics_complete_cycle(self, authenticated_client, sample_user, generate_wellness_entries):
        """Test complete analytics cycle."""
        # Generate test data
        generate_wellness_entries(50)
        
        # 1. Get organizational health analytics
        org_health_response = authenticated_client.get("/api/analytics/organizational-health")
        assert org_health_response.status_code == status.HTTP_200_OK
        org_health_data = org_health_response.json()
        assert "overall_health_score" in org_health_data
        assert "department_analytics" in org_health_data
        assert "trends" in org_health_data
        
        # 2. Get team analytics
        team_response = authenticated_client.get("/api/analytics/team/team_123")
        assert team_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        # 3. Get risk assessment
        risk_response = authenticated_client.get("/api/analytics/risk-assessment")
        assert risk_response.status_code == status.HTTP_200_OK
        risk_data = risk_response.json()
        assert "risk_level" in risk_data
        assert "risk_factors" in risk_data
        assert "recommendations" in risk_data
        
        # 4. Get trends analysis
        trends_response = authenticated_client.get("/api/analytics/trends")
        assert trends_response.status_code == status.HTTP_200_OK
        trends_data = trends_response.json()
        assert "period" in trends_data
        assert "metrics" in trends_data
        assert "insights" in trends_data
        
        # 5. Get comparison analytics
        comparison_response = authenticated_client.get("/api/analytics/comparison?compare_with=previous_month")
        assert comparison_response.status_code == status.HTTP_200_OK
        comparison_data = comparison_response.json()
        assert "comparison_period" in comparison_data
        assert "changes" in comparison_data
        assert "insights" in comparison_data
        
        # 6. Export analytics data
        export_response = authenticated_client.get("/api/analytics/export?format=csv&period=last_30_days")
        assert export_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


class TestNotificationWorkflow:
    """Test complete notification workflow."""
    
    def test_notification_complete_cycle(self, authenticated_client, sample_user):
        """Test complete notification cycle."""
        # 1. Get user notifications
        notifications_response = authenticated_client.get("/api/notifications/")
        assert notifications_response.status_code == status.HTTP_200_OK
        notifications_data = notifications_response.json()
        assert "notifications" in notifications_data
        assert "pagination" in notifications_data
        
        # 2. Mark notification as read
        if notifications_data["notifications"]:
            notification_id = notifications_data["notifications"][0]["id"]
            mark_read_response = authenticated_client.put(f"/api/notifications/{notification_id}", json={
                "is_read": True
            })
            assert mark_read_response.status_code == status.HTTP_200_OK
        
        # 3. Mark all notifications as read
        mark_all_read_response = authenticated_client.post("/api/notifications/mark-all-read")
        assert mark_all_read_response.status_code == status.HTTP_200_OK
        
        # 4. Get notification statistics
        stats_response = authenticated_client.get("/api/notifications/stats")
        assert stats_response.status_code == status.HTTP_200_OK
        stats_data = stats_response.json()
        assert "total_notifications" in stats_data
        assert "unread_count" in stats_data
        assert "read_count" in stats_data


class TestComplianceWorkflow:
    """Test complete compliance workflow."""
    
    def test_compliance_complete_cycle(self, authenticated_client, sample_user):
        """Test complete compliance cycle."""
        # 1. Get audit trail
        audit_response = authenticated_client.get("/api/compliance/audit-trail")
        assert audit_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        # 2. Get privacy consent status
        consent_response = authenticated_client.get("/api/compliance/privacy-consent")
        assert consent_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        # 3. Update privacy consent
        update_consent_response = authenticated_client.post("/api/compliance/privacy-consent", json={
            "data_collection": True,
            "data_processing": True,
            "data_sharing": False,
            "marketing_communications": False
        })
        assert update_consent_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        # 4. Get data rights information
        rights_response = authenticated_client.get("/api/compliance/data-rights")
        assert rights_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        # 5. Request data export
        export_response = authenticated_client.post("/api/compliance/data-export", json={
            "data_types": ["wellness_entries", "conversations", "profile"],
            "format": "json"
        })
        assert export_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        # 6. Get compliance status
        status_response = authenticated_client.get("/api/compliance/compliance-status")
        assert status_response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


class TestErrorHandlingWorkflow:
    """Test error handling in complete workflows."""
    
    def test_error_handling_in_workflow(self, authenticated_client, sample_user):
        """Test error handling during workflow execution."""
        # 1. Test invalid wellness entry
        invalid_entry_response = authenticated_client.post("/api/wellness/check-in", json={
            "entry_type": "invalid_type",
            "value": 15.0  # Invalid value
        })
        assert invalid_entry_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # 2. Test conversation with invalid data
        invalid_conversation_response = authenticated_client.post("/api/wellness/conversation", json={
            "invalid_field": "invalid_value"
        })
        assert invalid_conversation_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # 3. Test resource access with invalid ID
        invalid_resource_response = authenticated_client.get("/api/resources/invalid_id")
        assert invalid_resource_response.status_code == status.HTTP_404_NOT_FOUND
        
        # 4. Test analytics with invalid parameters
        invalid_analytics_response = authenticated_client.get("/api/analytics/trends?period=invalid_period")
        assert invalid_analytics_response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_404_NOT_FOUND]
        
        # 5. Verify system remains functional after errors
        # Try a valid operation after errors
        valid_response = authenticated_client.get("/api/wellness/history")
        assert valid_response.status_code == status.HTTP_200_OK
