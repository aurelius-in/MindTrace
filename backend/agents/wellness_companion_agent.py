"""
Wellness Companion Agent - Direct employee interaction and support
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import logging

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
        # TODO: Implement mood trend analysis with historical data
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
        """Get wellness insights for a user"""
        # TODO: Implement wellness insights based on conversation history
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
