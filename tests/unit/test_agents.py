"""
Unit tests for AI agents
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from backend.agents.base_agent import BaseAgent
from backend.agents.wellness_companion_agent import WellnessCompanionAgent
from backend.agents.resource_recommendation_agent import ResourceRecommendationAgent
from backend.agents.sentiment_risk_detection_agent import SentimentRiskDetectionAgent
from backend.agents.analytics_reporting_agent import AnalyticsReportingAgent
from backend.agents.policy_privacy_agent import PolicyPrivacyAgent
from backend.agents.orchestrator import Orchestrator
from backend.agents.advanced_orchestrator import AdvancedOrchestrator


class TestBaseAgent:
    """Test BaseAgent functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.agent = BaseAgent()
        self.mock_user = Mock()
        self.mock_user.id = "test_user_123"
        self.mock_user.name = "Test User"
        self.mock_user.team = "Engineering"
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.logger is not None
        assert self.agent.memory is not None
    
    def test_process_message(self):
        """Test message processing"""
        message = "Hello, how are you feeling today?"
        response = self.agent.process_message(message, self.mock_user)
        assert response is not None
        assert isinstance(response, str)
    
    def test_escalate_to_human(self):
        """Test human escalation"""
        with patch('backend.agents.base_agent.email_utility') as mock_email:
            self.agent.escalate_to_human(
                user_id="test_user",
                reason="High stress detected",
                urgency="high"
            )
            mock_email.send_escalation_notification.assert_called_once()
    
    def test_get_user_context(self):
        """Test user context retrieval"""
        context = self.agent.get_user_context(self.mock_user)
        assert context is not None
        assert "user_id" in context
        assert "name" in context
        assert "team" in context


class TestWellnessCompanionAgent:
    """Test WellnessCompanionAgent functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.agent = WellnessCompanionAgent()
        self.mock_user = Mock()
        self.mock_user.id = "test_user_123"
        self.mock_user.name = "Test User"
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.model is not None
        assert self.agent.memory_type == "episodic"
    
    def test_analyze_mood_trend(self):
        """Test mood trend analysis"""
        # Mock historical data
        mock_entries = [
            Mock(mood="happy", timestamp=datetime.now() - timedelta(days=1)),
            Mock(mood="sad", timestamp=datetime.now() - timedelta(days=2)),
            Mock(mood="happy", timestamp=datetime.now() - timedelta(days=3))
        ]
        
        with patch.object(self.agent, '_get_user_mood_history', return_value=mock_entries):
            trend = self.agent._analyze_mood_trend(self.mock_user.id)
            assert trend is not None
            assert "trend" in trend
            assert "insights" in trend
    
    def test_get_wellness_insights(self):
        """Test wellness insights generation"""
        insights = self.agent.get_wellness_insights(self.mock_user)
        assert insights is not None
        assert "mood_trends" in insights
        assert "stress_patterns" in insights
        assert "recommendations" in insights
    
    def test_generate_personalized_response(self):
        """Test personalized response generation"""
        message = "I'm feeling stressed today"
        response = self.agent.generate_personalized_response(message, self.mock_user)
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0


class TestResourceRecommendationAgent:
    """Test ResourceRecommendationAgent functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.agent = ResourceRecommendationAgent()
        self.mock_user = Mock()
        self.mock_user.id = "test_user_123"
        self.mock_user.role = "developer"
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.vector_db is not None
        assert self.agent.embedding_model is not None
    
    def test_collaborative_recommendation(self):
        """Test collaborative filtering recommendations"""
        with patch.object(self.agent, '_find_similar_users') as mock_find:
            mock_find.return_value = [{"user_id": "similar_user", "similarity": 0.8}]
            
            with patch.object(self.agent, '_get_resources_from_similar_users') as mock_resources:
                mock_resources.return_value = [
                    {"resource_id": "res1", "rating": 4.5},
                    {"resource_id": "res2", "rating": 4.2}
                ]
                
                recommendations = self.agent._collaborative_recommendation(self.mock_user)
                assert recommendations is not None
                assert len(recommendations) > 0
    
    def test_content_based_recommendation(self):
        """Test content-based recommendations"""
        user_preferences = {"stress_management": 0.8, "work_life_balance": 0.7}
        recommendations = self.agent._content_based_recommendation(user_preferences)
        assert recommendations is not None
        assert isinstance(recommendations, list)
    
    def test_get_recommendations(self):
        """Test main recommendation method"""
        recommendations = self.agent.get_recommendations(self.mock_user, "stress_management")
        assert recommendations is not None
        assert "resources" in recommendations
        assert "reasoning" in recommendations


class TestSentimentRiskDetectionAgent:
    """Test SentimentRiskDetectionAgent functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.agent = SentimentRiskDetectionAgent()
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.sentiment_analyzer is not None
        assert self.agent.risk_models is not None
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis"""
        text = "I'm feeling really stressed and overwhelmed with work"
        sentiment = self.agent.analyze_sentiment(text)
        assert sentiment is not None
        assert "sentiment" in sentiment
        assert "confidence" in sentiment
        assert "emotions" in sentiment
    
    def test_detect_risk_indicators(self):
        """Test risk indicator detection"""
        text = "I can't take this anymore, everything is falling apart"
        risk_indicators = self.agent.detect_risk_indicators(text)
        assert risk_indicators is not None
        assert "risk_level" in risk_indicators
        assert "indicators" in risk_indicators
    
    def test_assess_burnout_risk(self):
        """Test burnout risk assessment"""
        user_data = {
            "stress_level": 8.5,
            "workload": 9.0,
            "satisfaction": 3.0,
            "energy_level": 2.0
        }
        burnout_risk = self.agent.assess_burnout_risk(user_data)
        assert burnout_risk is not None
        assert "risk_score" in burnout_risk
        assert "risk_level" in burnout_risk
        assert "factors" in burnout_risk


class TestAnalyticsReportingAgent:
    """Test AnalyticsReportingAgent functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.agent = AnalyticsReportingAgent()
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.historical_data is not None
    
    def test_calculate_overall_wellness_score(self):
        """Test overall wellness score calculation"""
        mock_entries = [
            Mock(wellness_score=7.5, stress_level=6.0, engagement_score=8.0),
            Mock(wellness_score=8.0, stress_level=5.0, engagement_score=8.5),
            Mock(wellness_score=6.5, stress_level=7.0, engagement_score=7.0)
        ]
        
        with patch.object(self.agent, '_get_wellness_entries', return_value=mock_entries):
            score = self.agent._calculate_overall_wellness_score("7d")
            assert score is not None
            assert isinstance(score, float)
            assert 0 <= score <= 10
    
    def test_calculate_stress_levels(self):
        """Test stress level calculation"""
        mock_entries = [
            Mock(stress_level=3.0),
            Mock(stress_level=6.0),
            Mock(stress_level=8.0),
            Mock(stress_level=9.0)
        ]
        
        with patch.object(self.agent, '_get_wellness_entries', return_value=mock_entries):
            stress_levels = self.agent._calculate_stress_levels("7d")
            assert stress_levels is not None
            assert "low_stress" in stress_levels
            assert "moderate_stress" in stress_levels
            assert "high_stress" in stress_levels
            assert "critical_stress" in stress_levels
    
    def test_generate_organizational_report(self):
        """Test organizational report generation"""
        report = self.agent.generate_organizational_report("7d")
        assert report is not None
        assert "summary" in report
        assert "metrics" in report
        assert "insights" in report
        assert "recommendations" in report
    
    def test_generate_team_report(self):
        """Test team report generation"""
        report = self.agent.generate_team_report("Engineering", "7d")
        assert report is not None
        assert "team_name" in report
        assert "metrics" in report
        assert "insights" in report
    
    def test_predict_metric_trend(self):
        """Test metric trend prediction"""
        # Create mock historical data
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        data = pd.DataFrame({
            'timestamp': dates,
            'wellness_score': np.random.normal(7.0, 1.0, 30)
        })
        
        prediction = self.agent._predict_metric_trend('wellness_score', data)
        assert prediction is not None
        assert "current_value" in prediction
        assert "predicted_value" in prediction
        assert "confidence" in prediction
        assert "trend" in prediction


class TestPolicyPrivacyAgent:
    """Test PolicyPrivacyAgent functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.agent = PolicyPrivacyAgent()
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        assert self.agent.privacy_controls is not None
        assert self.agent.compliance_framework is not None
    
    def test_anonymize_data(self):
        """Test data anonymization"""
        user_data = {
            "user_id": "user123",
            "name": "John Doe",
            "email": "john@example.com",
            "wellness_score": 7.5
        }
        
        anonymized = self.agent.anonymize_data(user_data)
        assert anonymized is not None
        assert "user_id" not in anonymized
        assert "name" not in anonymized
        assert "email" not in anonymized
        assert "wellness_score" in anonymized
    
    def test_check_compliance(self):
        """Test compliance checking"""
        data_usage = {
            "purpose": "wellness_analysis",
            "data_types": ["wellness_scores", "stress_levels"],
            "retention_period": 365
        }
        
        compliance = self.agent.check_compliance(data_usage)
        assert compliance is not None
        assert "compliant" in compliance
        assert "issues" in compliance
    
    def test_apply_differential_privacy(self):
        """Test differential privacy application"""
        data = [7.5, 8.0, 6.5, 7.8, 8.2]
        private_data = self.agent.apply_differential_privacy(data, epsilon=1.0)
        assert private_data is not None
        assert len(private_data) == len(data)
        assert all(isinstance(x, (int, float)) for x in private_data)


class TestOrchestrator:
    """Test Orchestrator functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.orchestrator = Orchestrator()
        self.mock_user = Mock()
        self.mock_user.id = "test_user_123"
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization"""
        assert self.orchestrator.wellness_agent is not None
        assert self.orchestrator.resource_agent is not None
        assert self.orchestrator.sentiment_agent is not None
        assert self.orchestrator.analytics_agent is not None
    
    def test_process_user_message(self):
        """Test user message processing"""
        message = "I'm feeling stressed and need some resources"
        response = self.orchestrator.process_user_message(message, self.mock_user)
        assert response is not None
        assert "response" in response
        assert "recommendations" in response
        assert "risk_assessment" in response
    
    def test_coordinate_agents(self):
        """Test agent coordination"""
        user_context = {"user_id": "test_user", "current_mood": "stressed"}
        coordination = self.orchestrator.coordinate_agents(user_context)
        assert coordination is not None
        assert "wellness_insights" in coordination
        assert "resource_recommendations" in coordination
        assert "risk_assessment" in coordination


class TestAdvancedOrchestrator:
    """Test AdvancedOrchestrator functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.orchestrator = AdvancedOrchestrator()
        self.mock_user = Mock()
        self.mock_user.id = "test_user_123"
    
    def test_advanced_orchestrator_initialization(self):
        """Test advanced orchestrator initialization"""
        assert self.orchestrator.policy_agent is not None
        assert self.orchestrator.learning_system is not None
        assert self.orchestrator.performance_optimizer is not None
    
    def test_adaptive_response_generation(self):
        """Test adaptive response generation"""
        message = "I'm having a really bad day"
        context = {"previous_interactions": [], "user_preferences": {}}
        
        response = self.orchestrator.generate_adaptive_response(message, self.mock_user, context)
        assert response is not None
        assert "response" in response
        assert "adaptation_reason" in response
    
    def test_continuous_learning(self):
        """Test continuous learning functionality"""
        interaction_data = {
            "user_id": "test_user",
            "message": "I'm feeling better",
            "response": "That's great to hear!",
            "feedback": "positive"
        }
        
        learning_result = self.orchestrator.update_learning_system(interaction_data)
        assert learning_result is not None
        assert "updated" in learning_result
    
    def test_performance_optimization(self):
        """Test performance optimization"""
        performance_metrics = {
            "response_time": 1.5,
            "user_satisfaction": 0.8,
            "accuracy": 0.85
        }
        
        optimization = self.orchestrator.optimize_performance(performance_metrics)
        assert optimization is not None
        assert "optimizations" in optimization
        assert "expected_improvement" in optimization


if __name__ == "__main__":
    pytest.main([__file__])
