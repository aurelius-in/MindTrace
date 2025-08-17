"""
Wellness Service - Core business logic for wellness management
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from database.connection import get_db
from database.schema import WellnessEntry, User, Conversation, Resource
from agents.orchestrator import AdvancedAgentOrchestrator
from utils.analytics import WellnessAnalytics
from utils.privacy import PrivacyManager

logger = logging.getLogger(__name__)


@dataclass
class WellnessMetrics:
    """Wellness metrics data structure"""
    mood: float
    stress: float
    energy: float
    sleep_quality: float
    work_life_balance: float
    description: Optional[str] = None
    tags: Optional[List[str]] = None


@dataclass
class WellnessInsights:
    """Wellness insights and recommendations"""
    overall_score: float
    trend: str
    risk_level: str
    recommendations: List[str]
    alerts: List[str]


class WellnessService:
    """
    Core wellness service handling check-ins, analytics, and recommendations
    """
    
    def __init__(self):
        self.agent_orchestrator = AdvancedAgentOrchestrator()
        self.analytics = WellnessAnalytics()
        self.privacy_manager = PrivacyManager()
        self.logger = logging.getLogger(__name__)
    
    async def create_wellness_checkin(
        self,
        user_id: str,
        metrics: WellnessMetrics,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new wellness check-in entry
        """
        try:
            db = next(get_db())
            
            # Create wellness entry
            entry = WellnessEntry(
                id=str(uuid.uuid4()),
                user_id=user_id,
                entry_type="comprehensive",
                value=metrics.mood,  # Primary metric
                description=metrics.description,
                tags=metrics.tags or [],
                metadata={
                    "metrics": {
                        "mood": metrics.mood,
                        "stress": metrics.stress,
                        "energy": metrics.energy,
                        "sleep_quality": metrics.sleep_quality,
                        "work_life_balance": metrics.work_life_balance,
                    },
                    "checkin_type": "comprehensive",
                    **(metadata or {})
                },
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(entry)
            db.commit()
            db.refresh(entry)
            
            # Generate insights using AI agents
            insights = await self._generate_wellness_insights(user_id, metrics)
            
            # Apply privacy controls
            insights = self.privacy_manager.apply_privacy_controls(insights, user_id)
            
            return {
                "success": True,
                "entry_id": entry.id,
                "insights": insights,
                "message": "Wellness check-in recorded successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create wellness check-in: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to record wellness check-in"
            }
    
    async def track_mood(
        self,
        user_id: str,
        mood_value: float,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Track a quick mood check-in
        """
        try:
            db = next(get_db())
            
            entry = WellnessEntry(
                id=str(uuid.uuid4()),
                user_id=user_id,
                entry_type="mood",
                value=mood_value,
                description=description,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(entry)
            db.commit()
            db.refresh(entry)
            
            return {
                "success": True,
                "entry_id": entry.id,
                "message": "Mood tracked successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to track mood: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to track mood"
            }
    
    async def get_wellness_history(
        self,
        user_id: str,
        timeframe: str = "30d",
        entry_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get user's wellness history
        """
        try:
            db = next(get_db())
            
            # Calculate date range
            end_date = datetime.utcnow()
            if timeframe == "7d":
                start_date = end_date - timedelta(days=7)
            elif timeframe == "30d":
                start_date = end_date - timedelta(days=30)
            elif timeframe == "90d":
                start_date = end_date - timedelta(days=90)
            else:
                start_date = end_date - timedelta(days=30)
            
            # Build query
            query = db.query(WellnessEntry).filter(
                and_(
                    WellnessEntry.user_id == user_id,
                    WellnessEntry.created_at >= start_date,
                    WellnessEntry.created_at <= end_date
                )
            )
            
            if entry_types:
                query = query.filter(WellnessEntry.entry_type.in_(entry_types))
            
            entries = query.order_by(WellnessEntry.created_at.desc()).all()
            
            # Apply privacy controls
            entries = self.privacy_manager.filter_entries(entries, user_id)
            
            return {
                "success": True,
                "entries": [entry.to_dict() for entry in entries],
                "count": len(entries),
                "timeframe": timeframe
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get wellness history: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve wellness history"
            }
    
    async def get_wellness_analytics(
        self,
        user_id: str,
        timeframe: str = "30d"
    ) -> Dict[str, Any]:
        """
        Get comprehensive wellness analytics
        """
        try:
            # Get wellness history
            history_result = await self.get_wellness_history(user_id, timeframe)
            if not history_result["success"]:
                return history_result
            
            entries = history_result["entries"]
            
            # Generate analytics
            analytics = self.analytics.generate_user_analytics(entries, timeframe)
            
            # Apply privacy controls
            analytics = self.privacy_manager.apply_privacy_controls(analytics, user_id)
            
            return {
                "success": True,
                "analytics": analytics,
                "timeframe": timeframe
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get wellness analytics: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate analytics"
            }
    
    async def get_recommendations(
        self,
        user_id: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get personalized wellness recommendations
        """
        try:
            # Get user's recent wellness data
            history_result = await self.get_wellness_history(user_id, "30d")
            if not history_result["success"]:
                return history_result
            
            entries = history_result["entries"]
            
            # Use AI agents to generate recommendations
            agent_context = {
                "user_id": user_id,
                "wellness_history": entries,
                "context": context or "general wellness"
            }
            
            result = await self.agent_orchestrator.orchestrate_collaboration(
                context=agent_context,
                data={"request_type": "recommendations", "context": context},
                collaboration_pattern="emergent"
            )
            
            if result.success:
                recommendations = result.final_response.data.get("recommendations", [])
            else:
                # Fallback to basic recommendations
                recommendations = self._generate_basic_recommendations(entries)
            
            return {
                "success": True,
                "recommendations": recommendations,
                "context": context
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get recommendations: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate recommendations"
            }
    
    async def send_conversation_message(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a message to the wellness chat
        """
        try:
            db = next(get_db())
            
            # Create or get conversation session
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Save user message
            user_message = Conversation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                session_id=session_id,
                message=message,
                sender="user",
                created_at=datetime.utcnow()
            )
            
            db.add(user_message)
            db.commit()
            
            # Get AI response using agent orchestration
            agent_context = {
                "user_id": user_id,
                "session_id": session_id,
                "conversation_history": await self._get_conversation_history(session_id)
            }
            
            result = await self.agent_orchestrator.orchestrate_collaboration(
                context=agent_context,
                data={"request_type": "conversation", "message": message},
                collaboration_pattern="emergent"
            )
            
            if result.success:
                ai_response = result.final_response.data.get("response", "I'm here to help with your wellness journey.")
                sentiment = result.final_response.data.get("sentiment", "neutral")
                risk_level = result.final_response.data.get("risk_level", "low")
            else:
                ai_response = "I'm here to support you. How can I help with your wellness today?"
                sentiment = "neutral"
                risk_level = "low"
            
            # Save AI response
            ai_message = Conversation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                session_id=session_id,
                message=ai_response,
                sender="ai",
                metadata={
                    "sentiment": sentiment,
                    "risk_level": risk_level,
                    "agent_response": True
                },
                created_at=datetime.utcnow()
            )
            
            db.add(ai_message)
            db.commit()
            
            return {
                "success": True,
                "session_id": session_id,
                "response": ai_response,
                "sentiment": sentiment,
                "risk_level": risk_level
            }
            
        except Exception as e:
            self.logger.error(f"Failed to send conversation message: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process message"
            }
    
    async def get_conversation_history(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get conversation history
        """
        try:
            db = next(get_db())
            
            query = db.query(Conversation).filter(Conversation.user_id == user_id)
            
            if session_id:
                query = query.filter(Conversation.session_id == session_id)
            
            conversations = query.order_by(Conversation.created_at.desc()).limit(limit).all()
            
            # Apply privacy controls
            conversations = self.privacy_manager.filter_conversations(conversations, user_id)
            
            return {
                "success": True,
                "conversations": [conv.to_dict() for conv in conversations],
                "count": len(conversations)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get conversation history: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve conversation history"
            }
    
    async def _generate_wellness_insights(
        self,
        user_id: str,
        metrics: WellnessMetrics
    ) -> WellnessInsights:
        """
        Generate wellness insights using AI agents
        """
        try:
            # Calculate overall score
            overall_score = (
                metrics.mood * 0.3 +
                (10 - metrics.stress) * 0.25 +
                metrics.energy * 0.2 +
                metrics.sleep_quality * 0.15 +
                metrics.work_life_balance * 0.1
            )
            
            # Determine trend (simplified - would use historical data in real implementation)
            if overall_score >= 7:
                trend = "improving"
            elif overall_score >= 5:
                trend = "stable"
            else:
                trend = "declining"
            
            # Assess risk level
            if overall_score >= 7:
                risk_level = "low"
            elif overall_score >= 5:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            # Generate recommendations using AI
            agent_context = {
                "user_id": user_id,
                "metrics": metrics.__dict__,
                "overall_score": overall_score,
                "risk_level": risk_level
            }
            
            result = await self.agent_orchestrator.orchestrate_collaboration(
                context=agent_context,
                data={"request_type": "insights", "metrics": metrics.__dict__},
                collaboration_pattern="emergent"
            )
            
            if result.success:
                recommendations = result.final_response.data.get("recommendations", [])
                alerts = result.final_response.data.get("alerts", [])
            else:
                recommendations = self._generate_basic_recommendations_from_metrics(metrics)
                alerts = []
            
            return WellnessInsights(
                overall_score=overall_score,
                trend=trend,
                risk_level=risk_level,
                recommendations=recommendations,
                alerts=alerts
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate insights: {e}")
            # Return basic insights as fallback
            return WellnessInsights(
                overall_score=5.0,
                trend="stable",
                risk_level="medium",
                recommendations=["Consider taking regular breaks", "Practice stress management techniques"],
                alerts=[]
            )
    
    def _generate_basic_recommendations(
        self,
        entries: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate basic recommendations from wellness entries
        """
        recommendations = []
        
        if not entries:
            recommendations.append("Start with a wellness check-in to get personalized recommendations")
            return recommendations
        
        # Analyze recent entries
        recent_entries = entries[:5]
        avg_mood = sum(entry.get("value", 5) for entry in recent_entries) / len(recent_entries)
        
        if avg_mood < 4:
            recommendations.append("Consider speaking with a mental health professional")
            recommendations.append("Try stress management techniques like deep breathing")
        elif avg_mood < 6:
            recommendations.append("Practice mindfulness or meditation")
            recommendations.append("Ensure you're getting adequate sleep")
        else:
            recommendations.append("Keep up the great work with your wellness routine")
            recommendations.append("Consider sharing your positive practices with colleagues")
        
        return recommendations
    
    def _generate_basic_recommendations_from_metrics(
        self,
        metrics: WellnessMetrics
    ) -> List[str]:
        """
        Generate basic recommendations from current metrics
        """
        recommendations = []
        
        if metrics.stress > 7:
            recommendations.append("Consider taking short breaks throughout the day")
            recommendations.append("Try deep breathing exercises or meditation")
        
        if metrics.energy < 4:
            recommendations.append("Ensure you're getting adequate sleep")
            recommendations.append("Consider light physical activity to boost energy")
        
        if metrics.sleep_quality < 4:
            recommendations.append("Establish a consistent bedtime routine")
            recommendations.append("Limit screen time before bed")
        
        if metrics.work_life_balance < 4:
            recommendations.append("Set clear boundaries between work and personal time")
            recommendations.append("Schedule regular breaks and time off")
        
        if not recommendations:
            recommendations.append("Keep up the great work! Your wellness routine is working well.")
        
        return recommendations
    
    async def _get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a specific session
        """
        try:
            db = next(get_db())
            conversations = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).order_by(Conversation.created_at.desc()).limit(limit).all()
            
            return [conv.to_dict() for conv in conversations]
        except Exception as e:
            self.logger.error(f"Failed to get conversation history: {e}")
            return []
