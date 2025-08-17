"""
Wellness API Routes - Endpoints for wellness management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

from services.wellness_service import WellnessService, WellnessMetrics
from utils.auth import get_current_user
from database.schema import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/wellness", tags=["wellness"])
security = HTTPBearer()

# Pydantic models for request/response
class WellnessCheckInRequest(BaseModel):
    mood: float
    stress: float
    energy: float
    sleep_quality: float
    work_life_balance: float
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None

class MoodCheckInRequest(BaseModel):
    value: float
    description: Optional[str] = None

class WellnessHistoryRequest(BaseModel):
    timeframe: str = "30d"  # 7d, 30d, 90d
    entry_types: Optional[List[str]] = None

class ConversationRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class WellnessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

# Initialize wellness service
wellness_service = WellnessService()


@router.post("/check-in", response_model=WellnessResponse)
async def create_wellness_checkin(
    request: WellnessCheckInRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a comprehensive wellness check-in
    """
    try:
        metrics = WellnessMetrics(
            mood=request.mood,
            stress=request.stress,
            energy=request.energy,
            sleep_quality=request.sleep_quality,
            work_life_balance=request.work_life_balance,
            description=request.description,
            tags=request.tags
        )
        
        result = await wellness_service.create_wellness_checkin(
            user_id=current_user.id,
            metrics=metrics,
            metadata=request.metadata
        )
        
        if result["success"]:
            return WellnessResponse(
                success=True,
                message=result["message"],
                data={
                    "entry_id": result["entry_id"],
                    "insights": result["insights"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Failed to create wellness check-in: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create wellness check-in"
        )


@router.post("/mood", response_model=WellnessResponse)
async def track_mood(
    request: MoodCheckInRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Track a quick mood check-in
    """
    try:
        result = await wellness_service.track_mood(
            user_id=current_user.id,
            mood_value=request.value,
            description=request.description
        )
        
        if result["success"]:
            return WellnessResponse(
                success=True,
                message=result["message"],
                data={"entry_id": result["entry_id"]}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Failed to track mood: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track mood"
        )


@router.get("/history", response_model=WellnessResponse)
async def get_wellness_history(
    timeframe: str = "30d",
    entry_types: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get user's wellness history
    """
    try:
        # Parse entry types if provided
        parsed_entry_types = None
        if entry_types:
            parsed_entry_types = entry_types.split(",")
        
        result = await wellness_service.get_wellness_history(
            user_id=current_user.id,
            timeframe=timeframe,
            entry_types=parsed_entry_types
        )
        
        if result["success"]:
            return WellnessResponse(
                success=True,
                message="Wellness history retrieved successfully",
                data={
                    "entries": result["entries"],
                    "count": result["count"],
                    "timeframe": result["timeframe"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Failed to get wellness history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve wellness history"
        )


@router.get("/analytics", response_model=WellnessResponse)
async def get_wellness_analytics(
    timeframe: str = "30d",
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive wellness analytics
    """
    try:
        result = await wellness_service.get_wellness_analytics(
            user_id=current_user.id,
            timeframe=timeframe
        )
        
        if result["success"]:
            return WellnessResponse(
                success=True,
                message="Analytics generated successfully",
                data={
                    "analytics": result["analytics"],
                    "timeframe": result["timeframe"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Failed to get wellness analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate analytics"
        )


@router.get("/recommendations", response_model=WellnessResponse)
async def get_recommendations(
    context: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized wellness recommendations
    """
    try:
        result = await wellness_service.get_recommendations(
            user_id=current_user.id,
            context=context
        )
        
        if result["success"]:
            return WellnessResponse(
                success=True,
                message="Recommendations generated successfully",
                data={
                    "recommendations": result["recommendations"],
                    "context": result["context"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )


@router.post("/conversation", response_model=WellnessResponse)
async def send_conversation_message(
    request: ConversationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Send a message to the wellness chat
    """
    try:
        result = await wellness_service.send_conversation_message(
            user_id=current_user.id,
            message=request.message,
            session_id=request.session_id
        )
        
        if result["success"]:
            return WellnessResponse(
                success=True,
                message="Message sent successfully",
                data={
                    "session_id": result["session_id"],
                    "response": result["response"],
                    "sentiment": result["sentiment"],
                    "risk_level": result["risk_level"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Failed to send conversation message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message"
        )


@router.get("/conversations", response_model=WellnessResponse)
async def get_conversation_history(
    session_id: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """
    Get conversation history
    """
    try:
        result = await wellness_service.get_conversation_history(
            user_id=current_user.id,
            session_id=session_id,
            limit=limit
        )
        
        if result["success"]:
            return WellnessResponse(
                success=True,
                message="Conversation history retrieved successfully",
                data={
                    "conversations": result["conversations"],
                    "count": result["count"]
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
            
    except Exception as e:
        logger.error(f"Failed to get conversation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation history"
        )


@router.get("/summary", response_model=WellnessResponse)
async def get_wellness_summary(
    current_user: User = Depends(get_current_user)
):
    """
    Get a summary of user's wellness status
    """
    try:
        # Get recent wellness data
        history_result = await wellness_service.get_wellness_history(
            user_id=current_user.id,
            timeframe="7d"
        )
        
        if not history_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=history_result["message"]
            )
        
        entries = history_result["entries"]
        
        # Calculate summary metrics
        if entries:
            recent_entries = entries[:5]  # Last 5 entries
            avg_mood = sum(entry["value"] for entry in recent_entries) / len(recent_entries)
            
            # Determine trend
            if len(entries) >= 2:
                current_avg = sum(entry["value"] for entry in entries[:3]) / 3
                previous_avg = sum(entry["value"] for entry in entries[3:6]) / 3 if len(entries) >= 6 else current_avg
                trend = "improving" if current_avg > previous_avg else "declining" if current_avg < previous_avg else "stable"
            else:
                trend = "stable"
            
            summary = {
                "current_mood": avg_mood,
                "trend": trend,
                "entries_count": len(entries),
                "last_checkin": entries[0]["created_at"] if entries else None,
                "consistency_score": len(entries) / 7 * 100  # Percentage of days with check-ins
            }
        else:
            summary = {
                "current_mood": None,
                "trend": "no_data",
                "entries_count": 0,
                "last_checkin": None,
                "consistency_score": 0
            }
        
        return WellnessResponse(
            success=True,
            message="Wellness summary retrieved successfully",
            data={"summary": summary}
        )
        
    except Exception as e:
        logger.error(f"Failed to get wellness summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate wellness summary"
        )


@router.get("/stats", response_model=WellnessResponse)
async def get_wellness_stats(
    current_user: User = Depends(get_current_user)
):
    """
    Get wellness statistics
    """
    try:
        # Get wellness history for different timeframes
        timeframes = ["7d", "30d", "90d"]
        stats = {}
        
        for timeframe in timeframes:
            result = await wellness_service.get_wellness_history(
                user_id=current_user.id,
                timeframe=timeframe
            )
            
            if result["success"]:
                entries = result["entries"]
                if entries:
                    avg_value = sum(entry["value"] for entry in entries) / len(entries)
                    stats[timeframe] = {
                        "entries_count": len(entries),
                        "average_score": round(avg_value, 2),
                        "consistency": len(entries) / (7 if timeframe == "7d" else 30 if timeframe == "30d" else 90) * 100
                    }
                else:
                    stats[timeframe] = {
                        "entries_count": 0,
                        "average_score": 0,
                        "consistency": 0
                    }
        
        return WellnessResponse(
            success=True,
            message="Wellness statistics retrieved successfully",
            data={"stats": stats}
        )
        
    except Exception as e:
        logger.error(f"Failed to get wellness stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve wellness statistics"
        )
