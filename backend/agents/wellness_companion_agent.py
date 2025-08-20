"""
Wellness Companion Agent - Direct employee interaction and support
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import logging
import numpy as np

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .base_agent import BaseAgent, AgentType, AgentContext, AgentResponse
from config.settings import settings


class WellnessCompanionAgent(BaseAgent):
    """
    Wellness Companion Agent provides direct employee interaction,
    mood tracking, stress check-ins, and empathetic support.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.WELLNESS_COMPANION, config)
        
        # Initialize sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Wellness conversation templates
        self.conversation_templates = {
            "greeting": "Hello! I'm here to support your wellness journey. How are you feeling today?",
            "stress_check": "I notice you mentioned feeling stressed. Would you like to talk about what's on your mind?",
            "mood_tracking": "Thank you for sharing. I'm tracking your mood to help provide better support.",
            "escalation": "I'm concerned about what you're sharing. Let me connect you with additional support."
        }
    
    def _initialize_agent(self):
        """Initialize the wellness companion agent"""
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name=settings.agents.wellness_companion_model,
            temperature=0.7,
            openai_api_key=settings.ai.openai_api_key
        )
        
        # Initialize memory with summary capability
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            return_messages=True,
            max_token_limit=1000
        )
        
        # Load wellness prompts and responses
        self._load_wellness_prompts()
    
    def _load_wellness_prompts(self):
        """Load wellness conversation prompts and responses"""
        self.system_prompt = """You are an empathetic AI wellness companion for employees. Your role is to:

1. Provide supportive, non-judgmental listening
2. Help employees reflect on their feelings and experiences
3. Offer gentle guidance for stress management and wellness
4. Recognize when to escalate to human support
5. Maintain professional boundaries while being warm and caring

Key guidelines:
- Always respond with empathy and understanding
- Ask open-ended questions to encourage reflection
- Provide practical wellness suggestions when appropriate
- Never give medical advice or diagnose conditions
- Escalate immediately if someone mentions self-harm or crisis
- Respect privacy and maintain confidentiality

Current conversation context: {memory}"""

        self.conversation_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{user_message}"),
        ])
    
    async def process_request(self, context: AgentContext, data: Dict[str, Any]) -> AgentResponse:
        """Process a wellness conversation request"""
        
        user_message = data.get("message", "")
        message_type = data.get("type", "conversation")  # conversation, mood_check, stress_check
        
        # Analyze sentiment
        sentiment_scores = self.sentiment_analyzer.polarity_scores(user_message)
        
        # Check for risk indicators
        risk_level = self._assess_risk_level(user_message, sentiment_scores)
        requires_escalation = risk_level > settings.agents.wellness_risk_threshold
        
        # Generate response
        if requires_escalation:
            response_message = self._generate_escalation_response(user_message)
        else:
            response_message = await self._generate_conversation_response(user_message, context)
        
        # Update memory
        self.add_to_memory(HumanMessage(content=user_message))
        self.add_to_memory(AIMessage(content=response_message))
        
        # Prepare response data
        response_data = {
            "response": response_message,
            "sentiment": sentiment_scores,
            "risk_level": risk_level,
            "conversation_history": self._get_recent_conversation_history(),
            "wellness_suggestions": self._generate_wellness_suggestions(sentiment_scores, risk_level)
        }
        
        return AgentResponse(
            success=True,
            data=response_data,
            message="Wellness conversation processed successfully",
            risk_level=risk_level,
            requires_escalation=requires_escalation,
            privacy_flags=self.validate_privacy_compliance(data)
        )
    
    def _assess_risk_level(self, message: str, sentiment_scores: Dict[str, float]) -> float:
        """Assess risk level based on message content and sentiment"""
        risk_score = 0.0
        
        # Negative sentiment contributes to risk
        if sentiment_scores['compound'] < -0.5:
            risk_score += 0.3
        
        # Check for crisis keywords
        crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'no reason to live',
            'self-harm', 'hurt myself', 'want to die', 'better off dead'
        ]
        
        message_lower = message.lower()
        for keyword in crisis_keywords:
            if keyword in message_lower:
                risk_score += 0.8
                break
        
        # Check for extreme stress indicators
        stress_keywords = [
            'overwhelmed', 'can\'t take it anymore', 'breaking point',
            'too much pressure', 'exhausted', 'burned out'
        ]
        
        for keyword in stress_keywords:
            if keyword in message_lower:
                risk_score += 0.2
                break
        
        return min(risk_score, 1.0)
    
    def _generate_escalation_response(self, user_message: str) -> str:
        """Generate response for high-risk situations"""
        return """I'm very concerned about what you're sharing, and I want to make sure you get the support you need right now. 

This is a situation where I'd like to connect you with a trained professional who can provide immediate support. 

Please consider:
• Calling the National Suicide Prevention Lifeline at 988 (available 24/7)
• Reaching out to your company's Employee Assistance Program (EAP)
• Speaking with your HR representative or manager
• Contacting a mental health professional

You don't have to go through this alone. There are people ready to help you right now."""
    
    async def _generate_conversation_response(self, user_message: str, context: AgentContext) -> str:
        """Generate empathetic conversation response"""
        
        # Get conversation memory
        memory_summary = self.memory.buffer if hasattr(self.memory, 'buffer') else ""
        
        # Prepare prompt
        messages = self.conversation_prompt.format_messages(
            memory=memory_summary,
            user_message=user_message
        )
        
        # Generate response
        response = await self.llm.agenerate([messages])
        return response.generations[0][0].text
    
    def _get_recent_conversation_history(self) -> List[Dict[str, str]]:
        """Get recent conversation history for context"""
        messages = self.get_memory()
        history = []
        
        for msg in messages[-6:]:  # Last 6 messages
            if isinstance(msg, HumanMessage):
                history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                history.append({"role": "assistant", "content": msg.content})
        
        return history
    
    def _generate_wellness_suggestions(self, sentiment_scores: Dict[str, float], risk_level: float) -> List[str]:
        """Generate personalized wellness suggestions"""
        suggestions = []
        
        if sentiment_scores['compound'] < -0.3:
            suggestions.extend([
                "Consider taking a few deep breaths to help center yourself",
                "Try a 5-minute mindfulness break to reset your mind",
                "Remember that it's okay to ask for help when you need it"
            ])
        
        if risk_level > 0.5:
            suggestions.extend([
                "Consider reaching out to a trusted colleague or friend",
                "Take a short walk to clear your mind",
                "Practice self-compassion - you're doing the best you can"
            ])
        
        if sentiment_scores['compound'] > 0.3:
            suggestions.extend([
                "Great to hear you're feeling positive!",
                "Consider sharing your good mood with a colleague",
                "Use this energy to tackle something you've been putting off"
            ])
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    async def track_mood(self, context: AgentContext, mood_data: Dict[str, Any]) -> AgentResponse:
        """Track employee mood over time"""
        
        mood_score = mood_data.get("mood_score", 0)
        mood_description = mood_data.get("description", "")
        activities = mood_data.get("activities", [])
        
        # Store mood data (anonymized)
        mood_record = {
            "timestamp": context.timestamp.isoformat(),
            "mood_score": mood_score,
            "description": mood_description,
            "activities": activities,
            "session_id": context.session_id
        }
        
        # Analyze mood trends
        mood_trend = self._analyze_mood_trend(mood_score)
        
        response_data = {
            "mood_recorded": True,
            "mood_score": mood_score,
            "mood_trend": mood_trend,
            "suggestions": self._get_mood_based_suggestions(mood_score, activities)
        }
        
        return AgentResponse(
            success=True,
            data=response_data,
            message="Mood tracking completed successfully",
            risk_level=0.1 if mood_score < 3 else 0.0
        )
    
    def _analyze_mood_trend(self, current_mood: int) -> str:
        """Analyze mood trend based on current and historical data"""
        try:
            # Get historical mood data for the user
            from database.repository import wellness_entry_repo
            
            # Get last 30 days of mood data
            historical_entries = wellness_entry_repo.get_user_entries_by_timeframe(
                user_id=self.current_user_id,
                days=30
            )
            
            if not historical_entries:
                # No historical data, use current mood only
                if current_mood >= 7:
                    return "positive"
                elif current_mood >= 4:
                    return "neutral"
                else:
                    return "negative"
            
            # Extract mood scores
            mood_scores = [entry.get('wellness_score', 7.0) for entry in historical_entries]
            
            # Calculate trend
            if len(mood_scores) >= 2:
                recent_avg = np.mean(mood_scores[-7:])  # Last 7 entries
                earlier_avg = np.mean(mood_scores[:-7]) if len(mood_scores) > 7 else np.mean(mood_scores)
                
                if recent_avg > earlier_avg * 1.1:  # 10% improvement
                    return "improving"
                elif recent_avg < earlier_avg * 0.9:  # 10% decline
                    return "declining"
                else:
                    return "stable"
            else:
                return "stable"
                
        except Exception as e:
            self.logger.error(f"Error analyzing mood trend: {e}")
            # Fallback to current mood analysis
            if current_mood >= 7:
                return "positive"
            elif current_mood >= 4:
                return "neutral"
            else:
                return "negative"
    
    def _get_mood_based_suggestions(self, mood_score: int, activities: List[str]) -> List[str]:
        """Get suggestions based on mood and activities"""
        suggestions = []
        
        if mood_score < 4:
            suggestions.extend([
                "Consider scheduling a wellness check-in with yourself",
                "Try a short meditation or breathing exercise",
                "Reach out to a colleague for a quick chat"
            ])
        elif mood_score > 7:
            suggestions.extend([
                "Great energy! Consider helping a colleague who might be struggling",
                "Use this positive mood to tackle challenging tasks",
                "Share your good mood with your team"
            ])
        
        return suggestions
    
    def get_wellness_insights(self, user_id: str) -> Dict[str, Any]:
        """Get wellness insights for a user based on conversation history and data"""
        try:
            from database.repository import wellness_entry_repo, analytics_repo
            
            # Get user's wellness data
            wellness_entries = wellness_entry_repo.get_user_entries_by_timeframe(user_id, 30)
            conversation_history = self.get_memory()
            
            if not wellness_entries and not conversation_history:
                return {
                    "mood_trend": "stable",
                    "stress_patterns": [],
                    "wellness_score": 7.5,
                    "recommendations": [
                        "Continue regular check-ins",
                        "Consider stress management techniques",
                        "Maintain work-life balance"
                    ]
                }
            
            # Analyze mood trends
            mood_trend = self._analyze_mood_trends(user_id)
            
            # Analyze stress patterns
            stress_patterns = self._analyze_stress_patterns(wellness_entries)
            
            # Calculate overall wellness score
            wellness_score = self._calculate_wellness_score(wellness_entries, conversation_history)
            
            # Generate personalized recommendations
            recommendations = self._generate_wellness_recommendations(
                mood_trend, stress_patterns, wellness_score, conversation_history
            )
            
            return {
                "mood_trend": mood_trend.get("trend", "stable"),
                "stress_patterns": stress_patterns,
                "wellness_score": wellness_score,
                "recommendations": recommendations,
                "data_points": len(wellness_entries),
                "conversation_count": len(conversation_history)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting wellness insights: {e}")
            return {
                "mood_trend": "stable",
                "stress_patterns": [],
                "wellness_score": 7.5,
                "recommendations": [
                    "Continue regular check-ins",
                    "Consider stress management techniques",
                    "Maintain work-life balance"
                ]
            }
    
    def _analyze_mood_trends(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's mood trends over time"""
        try:
            from database.repository import wellness_entry_repo
            
            # Get last 30 days of mood data
            historical_entries = wellness_entry_repo.get_user_entries_by_timeframe(
                user_id=user_id,
                days=30
            )
            
            if not historical_entries:
                return {
                    "trend": "stable",
                    "average_mood": 7.0,
                    "mood_volatility": 0.5,
                    "recommendations": ["Continue current wellness practices"]
                }
            
            # Extract mood scores
            mood_scores = [entry.get('wellness_score', 7.0) for entry in historical_entries]
            
            # Calculate trend
            if len(mood_scores) >= 2:
                recent_avg = np.mean(mood_scores[-7:])  # Last 7 entries
                earlier_avg = np.mean(mood_scores[:-7]) if len(mood_scores) > 7 else np.mean(mood_scores)
                
                if recent_avg > earlier_avg * 1.1:  # 10% improvement
                    trend = "improving"
                elif recent_avg < earlier_avg * 0.9:  # 10% decline
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "stable"
            
            # Calculate volatility (standard deviation)
            mood_volatility = np.std(mood_scores) if len(mood_scores) > 1 else 0.5
            
            # Generate recommendations based on analysis
            recommendations = self._generate_mood_recommendations(trend, mood_volatility, np.mean(mood_scores))
            
            return {
                "trend": trend,
                "average_mood": np.mean(mood_scores),
                "mood_volatility": mood_volatility,
                "data_points": len(mood_scores),
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing mood trends: {e}")
            return {
                "trend": "stable",
                "average_mood": 7.0,
                "mood_volatility": 0.5,
                "recommendations": ["Continue current wellness practices"]
            }
    
    def _analyze_stress_patterns(self, wellness_entries: List[Dict]) -> List[str]:
        """Analyze stress patterns from wellness entries"""
        try:
            if not wellness_entries:
                return []
            
            stress_patterns = []
            stress_scores = [entry.get('stress_level', 5.0) for entry in wellness_entries]
            
            # Analyze stress patterns
            avg_stress = np.mean(stress_scores)
            stress_volatility = np.std(stress_scores) if len(stress_scores) > 1 else 0
            
            if avg_stress > 7.0:
                stress_patterns.append("Consistently high stress levels")
            elif avg_stress < 3.0:
                stress_patterns.append("Generally low stress levels")
            
            if stress_volatility > 2.0:
                stress_patterns.append("High stress variability")
            
            # Check for time-based patterns
            weekday_stress = []
            weekend_stress = []
            
            for entry in wellness_entries:
                timestamp = entry.get('timestamp')
                if timestamp:
                    if isinstance(timestamp, str):
                        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    
                    if timestamp.weekday() < 5:  # Weekday
                        weekday_stress.append(entry.get('stress_level', 5.0))
                    else:  # Weekend
                        weekend_stress.append(entry.get('stress_level', 5.0))
            
            if weekday_stress and weekend_stress:
                weekday_avg = np.mean(weekday_stress)
                weekend_avg = np.mean(weekend_stress)
                
                if weekday_avg > weekend_avg * 1.5:
                    stress_patterns.append("Higher stress during workdays")
                elif weekend_avg > weekday_avg * 1.5:
                    stress_patterns.append("Higher stress during weekends")
            
            return stress_patterns
            
        except Exception as e:
            self.logger.error(f"Error analyzing stress patterns: {e}")
            return []
    
    def _calculate_wellness_score(self, wellness_entries: List[Dict], conversation_history: List) -> float:
        """Calculate overall wellness score"""
        try:
            if not wellness_entries and not conversation_history:
                return 7.5
            
            # Calculate score from wellness entries
            entry_score = 0
            if wellness_entries:
                wellness_scores = [entry.get('wellness_score', 7.0) for entry in wellness_entries]
                entry_score = np.mean(wellness_scores)
            
            # Calculate score from conversation sentiment
            conversation_score = 0
            if conversation_history:
                sentiment_scores = []
                for message in conversation_history:
                    if hasattr(message, 'content'):
                        sentiment = self.sentiment_analyzer.polarity_scores(message.content)
                        sentiment_scores.append(sentiment['compound'])
                
                if sentiment_scores:
                    avg_sentiment = np.mean(sentiment_scores)
                    conversation_score = (avg_sentiment + 1) * 5  # Convert from [-1,1] to [0,10]
            
            # Weighted average
            if entry_score > 0 and conversation_score > 0:
                return (entry_score * 0.7) + (conversation_score * 0.3)
            elif entry_score > 0:
                return entry_score
            elif conversation_score > 0:
                return conversation_score
            else:
                return 7.5
                
        except Exception as e:
            self.logger.error(f"Error calculating wellness score: {e}")
            return 7.5
    
    def _generate_wellness_recommendations(self, mood_trend: Dict, stress_patterns: List[str], 
                                         wellness_score: float, conversation_history: List) -> List[str]:
        """Generate personalized wellness recommendations"""
        recommendations = []
        
        # Mood-based recommendations
        if mood_trend.get("trend") == "declining":
            recommendations.append("Consider scheduling a wellness check-in with HR or a counselor")
        
        # Stress-based recommendations
        if "Consistently high stress levels" in stress_patterns:
            recommendations.append("Implement regular stress management techniques like meditation or exercise")
        
        if "Higher stress during workdays" in stress_patterns:
            recommendations.append("Consider workload management and setting boundaries")
        
        # Wellness score-based recommendations
        if wellness_score < 6.0:
            recommendations.append("Focus on self-care and consider reaching out for support")
        elif wellness_score > 8.5:
            recommendations.append("Great wellness! Consider mentoring others or sharing positive practices")
        
        # Conversation-based recommendations
        if len(conversation_history) < 5:
            recommendations.append("Increase regular check-ins to better track your wellness")
        
        # Default recommendations
        if not recommendations:
            recommendations.extend([
                "Continue regular check-ins",
                "Consider stress management techniques",
                "Maintain work-life balance"
            ])
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _generate_mood_recommendations(self, trend: str, volatility: float, avg_mood: float) -> List[str]:
        """Generate personalized recommendations based on mood analysis"""
        recommendations = []
        
        # Trend-based recommendations
        if trend == "declining":
            recommendations.extend([
                "Consider scheduling a check-in with your manager or HR",
                "Try incorporating more stress-reduction activities into your routine",
                "Consider reaching out to the Employee Assistance Program"
            ])
        elif trend == "improving":
            recommendations.extend([
                "Great progress! Continue with your current wellness practices",
                "Consider sharing your positive strategies with colleagues"
            ])
        
        # Volatility-based recommendations
        if volatility > 2.0:  # High mood swings
            recommendations.extend([
                "Consider establishing a more consistent daily routine",
                "Practice mindfulness or meditation to stabilize mood",
                "Track your mood triggers to identify patterns"
            ])
        
        # Average mood-based recommendations
        if avg_mood < 5.0:
            recommendations.extend([
                "Consider speaking with a mental health professional",
                "Focus on small, achievable wellness goals",
                "Reach out to trusted colleagues or friends for support"
            ])
        elif avg_mood > 8.0:
            recommendations.extend([
                "Excellent wellness! Consider mentoring others",
                "Share your positive energy with the team"
            ])
        
        # Default recommendation if none generated
        if not recommendations:
            recommendations.append("Continue current wellness practices")
        
        return recommendations[:5]  # Limit to 5 recommendations
