from microsoft_graph_python import GraphServiceClient
from microsoft_graph_python.models import ChatMessage, ItemBody, BodyType
from typing import Dict, Any, Optional, List
import logging
import asyncio
import json
from datetime import datetime
import re
import httpx

from config.settings import settings
from agents.orchestrator import AgentOrchestrator
from security.auth import session_manager

logger = logging.getLogger(__name__)

class TeamsIntegration:
    """Microsoft Teams integration for the wellness platform."""
    
    def __init__(self):
        self.graph_client = GraphServiceClient(
            credentials=settings.integrations.teams_client_credentials
        )
        self.orchestrator = AgentOrchestrator()
        
        # Bot configuration
        self.bot_name = "Wellness Companion"
        self.bot_id = settings.integrations.teams_bot_id
        
        # Message patterns
        self.commands = {
            "help": self._handle_help_command,
            "checkin": self._handle_checkin_command,
            "mood": self._handle_mood_command,
            "resources": self._handle_resources_command,
            "report": self._handle_report_command
        }
        
        # User sessions
        self.user_sessions = {}
        
        # Teams app configuration
        self.app_id = settings.integrations.teams_app_id
        self.app_password = settings.integrations.teams_app_password
    
    async def start(self):
        """Start the Teams integration."""
        try:
            # Initialize Teams bot framework
            # Note: This is a simplified implementation
            # In production, you would use the Microsoft Bot Framework SDK
            logger.info("Teams integration initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to start Teams integration: {e}")
            raise
    
    async def stop(self):
        """Stop the Teams integration."""
        logger.info("Teams integration stopped")
    
    async def handle_message(self, message_data: Dict[str, Any]):
        """Handle incoming Teams messages."""
        try:
            message_type = message_data.get("type")
            
            if message_type == "message":
                await self._handle_text_message(message_data)
            elif message_type == "reaction":
                await self._handle_reaction(message_data)
            elif message_type == "mention":
                await self._handle_mention(message_data)
            elif message_type == "command":
                await self._handle_command(message_data)
                
        except Exception as e:
            logger.error(f"Error handling Teams message: {e}")
    
    async def _handle_text_message(self, message_data: Dict[str, Any]):
        """Handle text messages."""
        user_id = message_data.get("from", {}).get("id")
        conversation_id = message_data.get("conversation", {}).get("id")
        text = message_data.get("text", "").strip()
        
        if not text or not user_id:
            return
        
        # Check if this is a direct message
        if message_data.get("conversationType") == "personal":
            await self._process_direct_message(user_id, text, conversation_id)
    
    async def _handle_reaction(self, message_data: Dict[str, Any]):
        """Handle message reactions."""
        user_id = message_data.get("from", {}).get("id")
        reaction_type = message_data.get("reactionType")
        
        if reaction_type in ["like", "heart", "smile"]:
            await self._handle_mood_reaction(user_id, reaction_type, "positive")
        elif reaction_type in ["dislike", "sad", "angry"]:
            await self._handle_mood_reaction(user_id, reaction_type, "negative")
    
    async def _handle_mention(self, message_data: Dict[str, Any]):
        """Handle bot mentions."""
        user_id = message_data.get("from", {}).get("id")
        conversation_id = message_data.get("conversation", {}).get("id")
        text = message_data.get("text", "").strip()
        
        # Remove bot mention from text
        text = re.sub(r'@WellnessCompanion\s*', '', text).strip()
        
        if text:
            await self._process_direct_message(user_id, text, conversation_id)
    
    async def _handle_command(self, message_data: Dict[str, Any]):
        """Handle slash commands."""
        user_id = message_data.get("from", {}).get("id")
        conversation_id = message_data.get("conversation", {}).get("id")
        command = message_data.get("command", "").lstrip("/")
        text = message_data.get("text", "").strip()
        
        if command in self.commands:
            await self.commands[command](user_id, text, conversation_id)
        else:
            await self._send_message(
                conversation_id,
                f"Unknown command: `/{command}`. Use `/wellness help` for available commands."
            )
    
    async def _handle_help_command(self, user_id: str, text: str, conversation_id: str):
        """Handle the help command."""
        help_text = """
**Wellness Companion Commands**

• `/wellness help` - Show this help message
• `/wellness checkin` - Start a wellness check-in
• `/wellness mood <1-10>` - Log your current mood (1=very low, 10=excellent)
• `/wellness resources [topic]` - Get wellness resources
• `/wellness report` - Get your wellness summary

**Quick Actions**
• React with 👍 or ❤️ to log positive mood
• React with 👎 or 😢 to log negative mood
• Mention me in any channel for a quick chat

**Privacy**
Your wellness data is private and anonymized. Only you can see your personal data.
        """
        
        await self._send_message(conversation_id, help_text)
    
    async def _handle_checkin_command(self, user_id: str, text: str, conversation_id: str):
        """Handle the checkin command."""
        # Create adaptive card for mood check-in
        card = {
            "type": "AdaptiveCard",
            "version": "1.3",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "How are you feeling today? Please rate your mood:",
                    "weight": "Bolder",
                    "size": "Medium"
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "😢 1-2",
                    "data": {"action": "mood_checkin", "value": "1-2"}
                },
                {
                    "type": "Action.Submit",
                    "title": "😕 3-4",
                    "data": {"action": "mood_checkin", "value": "3-4"}
                },
                {
                    "type": "Action.Submit",
                    "title": "😐 5-6",
                    "data": {"action": "mood_checkin", "value": "5-6"}
                },
                {
                    "type": "Action.Submit",
                    "title": "🙂 7-8",
                    "data": {"action": "mood_checkin", "value": "7-8"}
                },
                {
                    "type": "Action.Submit",
                    "title": "😊 9-10",
                    "data": {"action": "mood_checkin", "value": "9-10"}
                }
            ]
        }
        
        await self._send_adaptive_card(conversation_id, card)
    
    async def _handle_mood_command(self, user_id: str, text: str, conversation_id: str):
        """Handle the mood command."""
        try:
            # Extract mood value from text
            mood_match = re.search(r'(\d+)', text)
            if mood_match:
                mood_value = int(mood_match.group(1))
                if 1 <= mood_value <= 10:
                    await self._log_mood(user_id, mood_value)
                    await self._send_message(
                        conversation_id,
                        f"Thanks! I've logged your mood as {mood_value}/10. Keep up the great work! 💪"
                    )
                else:
                    await self._send_message(
                        conversation_id,
                        "Please provide a mood value between 1 and 10."
                    )
            else:
                await self._send_message(
                    conversation_id,
                    "Please provide a mood value: `/wellness mood 7`"
                )
        except ValueError:
            await self._send_message(
                conversation_id,
                "Please provide a valid number for your mood."
            )
    
    async def _handle_resources_command(self, user_id: str, text: str, conversation_id: str):
        """Handle the resources command."""
        topic = text.strip() if text else "general"
        
        try:
            # Get user context
            user_info = await self._get_user_info(user_id)
            
            # Get resource recommendations
            result = await self.orchestrator.recommend_resources(
                user_needs=topic,
                user_preferences={"platform": "teams"},
                user_id=user_id,
                user_role=user_info.get("role", "employee")
            )
            
            if result.get("success") and result.get("data", {}).get("recommendations"):
                recommendations = result["data"]["recommendations"][:3]  # Limit to 3
                
                # Create adaptive card for resources
                card = {
                    "type": "AdaptiveCard",
                    "version": "1.3",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": f"**Wellness Resources for: {topic.title()}**",
                            "weight": "Bolder",
                            "size": "Medium"
                        }
                    ]
                }
                
                for rec in recommendations:
                    card["body"].extend([
                        {
                            "type": "TextBlock",
                            "text": f"**{rec['title']}**",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text": rec['description'],
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"Duration: {rec.get('duration_minutes', 'N/A')} min",
                            "isSubtle": True
                        },
                        {
                            "type": "Action.Submit",
                            "title": "View Details",
                            "data": {"action": "view_resource", "resource_id": rec.get("id")}
                        },
                        {
                            "type": "TextBlock",
                            "text": "---",
                            "separator": True
                        }
                    ])
                
                await self._send_adaptive_card(conversation_id, card)
            else:
                await self._send_message(
                    conversation_id,
                    f"I couldn't find specific resources for '{topic}', but here are some general wellness tips:\n\n• Take regular breaks\n• Practice deep breathing\n• Stay hydrated\n• Move your body"
                )
                
        except Exception as e:
            logger.error(f"Error getting resources: {e}")
            await self._send_message(
                conversation_id,
                "Sorry, I couldn't get resources right now. Please try again later."
            )
    
    async def _handle_report_command(self, user_id: str, text: str, conversation_id: str):
        """Handle the report command."""
        try:
            # Get user's wellness summary
            result = await self.orchestrator.generate_analytics_report(
                report_type="personal_wellness",
                timeframe="7d",
                filters={"user_id": user_id},
                user_role="employee",
                user_id=user_id
            )
            
            if result.get("success") and result.get("data"):
                data = result["data"]
                
                # Create adaptive card for report
                card = {
                    "type": "AdaptiveCard",
                    "version": "1.3",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "**Your Wellness Summary (Last 7 Days)**",
                            "weight": "Bolder",
                            "size": "Large"
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {
                                    "title": "Overall Wellness Score:",
                                    "value": f"{data.get('overall_score', 'N/A')}/10"
                                },
                                {
                                    "title": "Average Mood:",
                                    "value": f"{data.get('avg_mood', 'N/A')}/10"
                                },
                                {
                                    "title": "Stress Level:",
                                    "value": f"{data.get('stress_level', 'N/A')}/10"
                                },
                                {
                                    "title": "Energy Level:",
                                    "value": f"{data.get('energy_level', 'N/A')}/10"
                                }
                            ]
                        },
                        {
                            "type": "TextBlock",
                            "text": "**Recent Activity:**",
                            "weight": "Bolder"
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {
                                    "title": "Check-ins:",
                                    "value": str(data.get('checkins_count', 0))
                                },
                                {
                                    "title": "Resources used:",
                                    "value": str(data.get('resources_used', 0))
                                },
                                {
                                    "title": "Conversations:",
                                    "value": str(data.get('conversations_count', 0))
                                }
                            ]
                        },
                        {
                            "type": "TextBlock",
                            "text": f"**Trends:**\n{data.get('trends', 'No recent trends available')}",
                            "wrap": True
                        }
                    ]
                }
                
                await self._send_adaptive_card(conversation_id, card)
            else:
                await self._send_message(
                    conversation_id,
                    "I don't have enough data to generate a report yet. Try logging your mood and using the wellness features more!"
                )
                
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            await self._send_message(
                conversation_id,
                "Sorry, I couldn't generate your report right now. Please try again later."
            )
    
    async def _process_direct_message(self, user_id: str, text: str, conversation_id: str):
        """Process direct messages with the wellness agent."""
        try:
            # Get user context
            user_info = await self._get_user_info(user_id)
            
            # Process with wellness companion agent
            result = await self.orchestrator.process_employee_conversation(
                user_id=user_id,
                message=text,
                session_id=self._get_session_id(user_id),
                user_role=user_info.get("role", "employee")
            )
            
            if result.get("success"):
                response = result["data"]["response"]
                risk_level = result["data"].get("risk_level", 0)
                
                # Send response
                await self._send_message(conversation_id, response)
                
                # Handle high-risk situations
                if risk_level > 0.7:
                    await self._handle_high_risk_situation(user_id, conversation_id, text, risk_level)
                    
            else:
                await self._send_message(
                    conversation_id,
                    "I'm having trouble processing your message right now. Please try again later."
                )
                
        except Exception as e:
            logger.error(f"Error processing direct message: {e}")
            await self._send_message(
                conversation_id,
                "Sorry, I encountered an error. Please try again later."
            )
    
    async def _handle_mood_reaction(self, user_id: str, reaction: str, mood_type: str):
        """Handle mood reactions."""
        try:
            # Map reaction to mood value
            mood_mapping = {
                "positive": {"like": 8, "heart": 9, "smile": 7},
                "negative": {"dislike": 3, "sad": 2, "angry": 1}
            }
            
            mood_value = mood_mapping[mood_type].get(reaction, 5)
            await self._log_mood(user_id, mood_value)
            
            # Send confirmation
            await self._send_message(
                user_id,  # DM channel
                f"Thanks for sharing your mood! I've logged it as {mood_value}/10. Keep taking care of yourself! 💙"
            )
            
        except Exception as e:
            logger.error(f"Error handling mood reaction: {e}")
    
    async def _handle_adaptive_card_action(self, action_data: Dict[str, Any]):
        """Handle adaptive card actions."""
        action = action_data.get("action")
        user_id = action_data.get("from", {}).get("id")
        conversation_id = action_data.get("conversation", {}).get("id")
        
        if action == "mood_checkin":
            value = action_data.get("value")
            if value and user_id:
                try:
                    # Extract mood value from button value
                    mood_range = value.split("-")
                    mood_value = int(mood_range[0]) + (int(mood_range[1]) - int(mood_range[0])) // 2
                    
                    await self._log_mood(user_id, mood_value)
                    await self._send_message(
                        conversation_id,
                        f"Thanks! I've logged your mood as {mood_value}/10. How can I help you today?"
                    )
                    
                except Exception as e:
                    logger.error(f"Error handling mood check-in: {e}")
        
        elif action == "view_resource":
            resource_id = action_data.get("resource_id")
            if resource_id and user_id:
                try:
                    # Get resource details
                    result = await self.orchestrator.recommend_resources(
                        user_needs=resource_id,
                        user_preferences={"platform": "teams"},
                        user_id=user_id,
                        user_role="employee"
                    )
                    
                    if result.get("success") and result.get("data", {}).get("recommendations"):
                        resource = result["data"]["recommendations"][0]
                        
                        response_text = f"""
**{resource['title']}**

{resource['description']}

**Duration:** {resource.get('duration_minutes', 'N/A')} minutes
**Category:** {resource.get('category', 'N/A')}

{resource.get('content', 'No content available')}
                        """
                        
                        await self._send_message(conversation_id, response_text)
                        
                except Exception as e:
                    logger.error(f"Error handling resource selection: {e}")
    
    async def _handle_high_risk_situation(self, user_id: str, conversation_id: str, message: str, risk_level: float):
        """Handle high-risk situations."""
        try:
            # Send immediate support message
            support_message = """
🚨 **I'm concerned about what you're sharing.**

You're not alone, and there are people who want to help:

**Immediate Support:**
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

**Workplace Support:**
• Your HR department
• Employee Assistance Program (EAP)
• Your manager or trusted colleague

Would you like me to help you connect with any of these resources?
            """
            
            await self._send_message(conversation_id, support_message)
            
            # Log the incident
            logger.warning(f"High-risk situation detected for user {user_id}: {message} (risk: {risk_level})")
            
            # Escalate to HR or management
            await self._escalate_to_hr(user_id, message, risk_level)
            
        except Exception as e:
            logger.error(f"Error handling high-risk situation: {e}")
    
    async def _log_mood(self, user_id: str, mood_value: int):
        """Log user mood."""
        try:
            # Create wellness entry
            result = await self.orchestrator.process_employee_conversation(
                user_id=user_id,
                message=f"mood check-in: {mood_value}/10",
                session_id=self._get_session_id(user_id),
                user_role="employee"
            )
            
            if result.get("success"):
                logger.info(f"Logged mood {mood_value}/10 for user {user_id}")
            else:
                logger.error(f"Failed to log mood for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error logging mood: {e}")
    
    async def _get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get user information from Teams."""
        try:
            # Use Microsoft Graph API to get user info
            user = await self.graph_client.users.by_user_id(user_id).get()
            return {
                "id": user_id,
                "name": user.display_name,
                "email": user.mail or user.user_principal_name,
                "role": "employee"  # Default role, could be enhanced with user mapping
            }
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {"id": user_id, "role": "employee"}
    
    def _get_session_id(self, user_id: str) -> str:
        """Get or create session ID for user."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = f"teams_{user_id}_{datetime.now().timestamp()}"
        return self.user_sessions[user_id]
    
    async def _send_message(self, conversation_id: str, text: str):
        """Send a message to a conversation."""
        try:
            # Create message using Microsoft Graph API
            message = ChatMessage(
                body=ItemBody(
                    content=text,
                    content_type=BodyType.HTML
                )
            )
            
            await self.graph_client.chats.by_chat_id(conversation_id).messages.post(message)
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def _send_adaptive_card(self, conversation_id: str, card: Dict[str, Any]):
        """Send an adaptive card to a conversation."""
        try:
            # Create message with adaptive card
            message = ChatMessage(
                body=ItemBody(
                    content="",
                    content_type=BodyType.HTML
                ),
                attachments=[
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": card
                    }
                ]
            )
            
            await self.graph_client.chats.by_chat_id(conversation_id).messages.post(message)
            
        except Exception as e:
            logger.error(f"Error sending adaptive card: {e}")
    
    async def _escalate_to_hr(self, user_id: str, message: str, risk_level: float):
        """Escalate high-risk situation to HR."""
        try:
            # Get user information
            user_info = await self._get_user_info(user_id)
            
            # Create escalation record
            escalation_data = {
                "user_id": user_id,
                "user_name": user_info.get("display_name", "Unknown"),
                "user_email": user_info.get("email", ""),
                "message": message,
                "risk_level": risk_level,
                "timestamp": datetime.now().isoformat(),
                "status": "pending",
                "escalation_type": "high_risk_situation"
            }
            
            # Store escalation in database
            from database.repository import analytics_repo
            await analytics_repo.create_escalation_record(escalation_data)
            
            # Send notification to HR channel
            hr_channel = getattr(settings.integrations, 'teams_hr_channel_id', None)
            if hr_channel:
                hr_message = f"""
🚨 High-Risk Situation Escalation

User: {user_info.get("display_name", "Unknown")} ({user_id})
Risk Level: {risk_level:.2f}
Message: {message[:200]}{"..." if len(message) > 200 else ""}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please review and take appropriate action.
                """
                
                await self._send_message(hr_channel, hr_message)
            
            # Send email notification to HR team
            await self._send_hr_email_notification(escalation_data)
            
            logger.warning(f"HR escalation completed for user {user_id} with risk level {risk_level}")
            
        except Exception as e:
            logger.error(f"Error escalating to HR: {e}")
    
    async def _send_hr_email_notification(self, escalation_data: Dict[str, Any]):
        """Send email notification to HR team"""
        try:
            from utils.email import send_email
            
            subject = f"High-Risk Wellness Situation - {escalation_data['user_name']}"
            
            body = f"""
High-Risk Wellness Situation Detected

User: {escalation_data['user_name']} ({escalation_data['user_email']})
Risk Level: {escalation_data['risk_level']:.2f}
Time: {escalation_data['timestamp']}

Message: {escalation_data['message']}

Please review and take appropriate action immediately.

This is an automated notification from the Enterprise Wellness AI system.
            """
            
            # Send to HR team
            hr_emails = getattr(settings.integrations, 'hr_team_emails', [])
            if hr_emails:
                await send_email(
                    to_emails=hr_emails,
                    subject=subject,
                    body=body,
                    priority="high"
                )
                
        except Exception as e:
            logger.error(f"Error sending HR email notification: {e}")
    
    async def send_proactive_message(self, user_id: str, message: str):
        """Send a proactive message to a user."""
        try:
            # Get user's personal chat
            personal_chat = await self.graph_client.users.by_user_id(user_id).chats.get()
            
            if personal_chat:
                await self._send_message(personal_chat.id, message)
            else:
                logger.warning(f"Could not find personal chat for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error sending proactive message: {e}")
    
    async def send_wellness_reminder(self, user_id: str):
        """Send a wellness check-in reminder."""
        reminder_message = """
🌟 **Time for your wellness check-in!**

How are you feeling today? Take a moment to reflect on your well-being.

You can:
• Reply to this message to chat with me
• Use `/wellness checkin` for a quick mood check
• Use `/wellness mood <1-10>` to log your mood directly

Remember, taking care of yourself is important! 💙
        """
        
        await self.send_proactive_message(user_id, reminder_message)
    
    async def send_weekly_report(self, user_id: str):
        """Send a weekly wellness report."""
        try:
            # Generate weekly report
            result = await self.orchestrator.generate_analytics_report(
                report_type="personal_wellness",
                timeframe="7d",
                filters={"user_id": user_id},
                user_role="employee",
                user_id=user_id
            )
            
            if result.get("success") and result.get("data"):
                data = result["data"]
                
                report_message = f"""
📊 **Your Weekly Wellness Report**

**Overall Wellness Score:** {data.get('overall_score', 'N/A')}/10
**Average Mood:** {data.get('avg_mood', 'N/A')}/10
**Stress Level:** {data.get('stress_level', 'N/A')}/10

**This Week's Activity:**
• Check-ins: {data.get('checkins_count', 0)}
• Resources used: {data.get('resources_used', 0)}
• Conversations: {data.get('conversations_count', 0)}

**Trends:** {data.get('trends', 'No recent trends available')}

Keep up the great work on your wellness journey! 🌟
                """
                
                await self.send_proactive_message(user_id, report_message)
                
        except Exception as e:
            logger.error(f"Error sending weekly report: {e}")

# Global Teams integration instance
teams_integration = TeamsIntegration()

# Export commonly used functions and classes
__all__ = [
    'TeamsIntegration',
    'teams_integration'
]
