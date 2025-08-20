"""
Base Agent Class for Enterprise Employee Wellness AI
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel

from config.settings import settings


class AgentType(Enum):
    """Enumeration of agent types"""
    WELLNESS_COMPANION = "wellness_companion"
    RESOURCE_RECOMMENDATION = "resource_recommendation"
    SENTIMENT_RISK_DETECTION = "sentiment_risk_detection"
    ANALYTICS_REPORTING = "analytics_reporting"
    POLICY_PRIVACY = "policy_privacy"


@dataclass
class AgentContext:
    """Context information passed between agents"""
    user_id: str
    session_id: str
    timestamp: datetime
    metadata: Dict[str, Any]
    privacy_level: str = "standard"  # standard, sensitive, critical


@dataclass
class AgentResponse:
    """Standardized response format for all agents"""
    success: bool
    data: Dict[str, Any]
    message: str
    risk_level: Optional[float] = None
    requires_escalation: bool = False
    privacy_flags: List[str] = None


class BaseAgent(ABC):
    """
    Base class for all agents in the Enterprise Employee Wellness AI system
    """
    
    def __init__(self, agent_type: AgentType, config: Dict[str, Any] = None):
        self.agent_type = agent_type
        self.config = config or {}
        self.memory = ConversationBufferMemory(return_messages=True)
        self.logger = logging.getLogger(f"agent.{agent_type.value}")
        
        # Performance metrics
        self.request_count = 0
        self.response_times = []
        self.error_count = 0
        
        # Initialize agent-specific components
        self._initialize_agent()
    
    @abstractmethod
    def _initialize_agent(self):
        """Initialize agent-specific components"""
        pass
    
    @abstractmethod
    async def process_request(self, context: AgentContext, data: Dict[str, Any]) -> AgentResponse:
        """Process a request and return a response"""
        pass
    
    async def handle_request(self, context: AgentContext, data: Dict[str, Any]) -> AgentResponse:
        """Main request handler with logging and monitoring"""
        start_time = datetime.now()
        self.request_count += 1
        
        try:
            # Log incoming request
            self.logger.info(f"Processing request for user {context.user_id}", extra={
                "user_id": context.user_id,
                "session_id": context.session_id,
                "agent_type": self.agent_type.value,
                "data_keys": list(data.keys())
            })
            
            # Process the request
            response = await self.process_request(context, data)
            
            # Update metrics
            response_time = (datetime.now() - start_time).total_seconds()
            self.response_times.append(response_time)
            
            # Log response
            self.logger.info(f"Request completed successfully", extra={
                "user_id": context.user_id,
                "response_time": response_time,
                "success": response.success,
                "risk_level": response.risk_level
            })
            
            return response
            
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error processing request: {str(e)}", extra={
                "user_id": context.user_id,
                "error": str(e),
                "agent_type": self.agent_type.value
            })
            
            return AgentResponse(
                success=False,
                data={},
                message=f"Error processing request: {str(e)}",
                requires_escalation=True
            )
    
    def get_memory(self) -> List[BaseMessage]:
        """Get conversation memory"""
        return self.memory.chat_memory.messages
    
    def add_to_memory(self, message: BaseMessage):
        """Add message to conversation memory"""
        self.memory.chat_memory.add_message(message)
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        return {
            "agent_type": self.agent_type.value,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "success_rate": (self.request_count - self.error_count) / self.request_count if self.request_count > 0 else 0,
            "average_response_time": avg_response_time,
            "memory_size": len(self.get_memory())
        }
    
    def validate_privacy_compliance(self, data: Dict[str, Any]) -> List[str]:
        """Validate data for privacy compliance"""
        flags = []
        
        # Check for PII patterns
        for field, pattern in settings.agents.privacy_scrubbing_rules.items():
            if any(pattern in str(value) for value in data.values()):
                flags.append(f"potential_{field}_detected")
        
        return flags
    
    async def escalate_to_human(self, context: AgentContext, reason: str):
        """Escalate to human intervention"""
        try:
            self.logger.warning(f"Escalating to human: {reason}", extra={
                "user_id": context.user_id,
                "reason": reason,
                "agent_type": self.agent_type.value
            })
            
            # Create escalation record
            escalation_data = {
                "user_id": context.user_id,
                "reason": reason,
                "agent_type": self.agent_type.value,
                "timestamp": datetime.now().isoformat(),
                "status": "pending",
                "escalation_type": "human_intervention",
                "context_data": {
                    "session_id": context.session_id,
                    "user_role": context.user_role,
                    "conversation_history": len(self.get_memory())
                }
            }
            
            # Store escalation in database
            from database.repository import analytics_repo
            await analytics_repo.create_escalation_record(escalation_data)
            
            # Send notification to appropriate channels
            await self._send_escalation_notifications(escalation_data)
            
            # Log for audit purposes
            self.logger.info(f"Human escalation created for user {context.user_id}: {reason}")
            
        except Exception as e:
            self.logger.error(f"Error escalating to human: {e}")
    
    async def _send_escalation_notifications(self, escalation_data: Dict[str, Any]):
        """Send escalation notifications to appropriate channels"""
        try:
            from utils.email import send_email
            
            subject = f"Human Intervention Required - {escalation_data['agent_type']}"
            
            body = f"""
Human Intervention Required

User ID: {escalation_data['user_id']}
Agent Type: {escalation_data['agent_type']}
Reason: {escalation_data['reason']}
Time: {escalation_data['timestamp']}

Context: {escalation_data.get('context_data', {})}

Please review and provide human intervention as needed.

This is an automated notification from the Enterprise Wellness AI system.
            """
            
            # Send to designated escalation contacts
            escalation_emails = getattr(settings, 'escalation_emails', [])
            if escalation_emails:
                await send_email(
                    to_emails=escalation_emails,
                    subject=subject,
                    body=body,
                    priority="high"
                )
                
        except Exception as e:
            self.logger.error(f"Error sending escalation notifications: {e}")
    
    def __str__(self):
        return f"{self.agent_type.value}_agent"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(type={self.agent_type.value})>"
