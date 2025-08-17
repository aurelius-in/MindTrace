from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from typing import Dict, Any, Optional, List
import logging
import asyncio
import json
from datetime import datetime
import re

from config.settings import settings
from agents.orchestrator import AgentOrchestrator
from security.auth import session_manager

logger = logging.getLogger(__name__)

class SlackIntegration:
    """Slack integration for the wellness platform."""
    
    def __init__(self):
        self.client = WebClient(token=settings.integrations.slack_bot_token)
        self.socket_client = None
        self.orchestrator = AgentOrchestrator()
        self.app_token = settings.integrations.slack_app_token
        
        # Bot configuration
        self.bot_name = "Wellness Companion"
        self.bot_icon = ":heart:"
        
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
    
    async def start(self):
        """Start the Slack integration."""
        try:
            if self.app_token:
                self.socket_client = SocketModeClient(
                    app_token=self.app_token,
                    web_client=self.client
                )
                
                # Register event handlers
                self.socket_client.socket_mode_request_listeners.append(self._handle_socket_request)
                
                # Start the client
                await self.socket_client.start_async()
                logger.info("Slack Socket Mode client started successfully")
            else:
                logger.warning("Slack app token not configured, Socket Mode disabled")
                
        except Exception as e:
            logger.error(f"Failed to start Slack integration: {e}")
            raise
    
    async def stop(self):
        """Stop the Slack integration."""
        if self.socket_client:
            await self.socket_client.stop_async()
            logger.info("Slack Socket Mode client stopped")
    
    async def _handle_socket_request(self, client: SocketModeClient, req: SocketModeRequest):
        """Handle incoming Socket Mode requests."""
        try:
            if req.type == "events_api":
                await self._handle_event(req.payload)
            elif req.type == "interactive":
                await self._handle_interaction(req.payload)
            elif req.type == "slash_commands":
                await self._handle_slash_command(req.payload)
            
            # Acknowledge the request
            client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
            
        except Exception as e:
            logger.error(f"Error handling Socket Mode request: {e}")
            client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
    
    async def _handle_event(self, payload: Dict[str, Any]):
        """Handle Slack events."""
        event = payload.get("event", {})
        event_type = event.get("type")
        
        if event_type == "message":
            await self._handle_message_event(event)
        elif event_type == "app_mention":
            await self._handle_app_mention(event)
        elif event_type == "reaction_added":
            await self._handle_reaction_added(event)
    
    async def _handle_message_event(self, event: Dict[str, Any]):
        """Handle message events."""
        # Only process messages from users (not bots)
        if event.get("bot_id"):
            return
        
        user_id = event.get("user")
        channel_id = event.get("channel")
        text = event.get("text", "").strip()
        
        # Check if this is a DM with the bot
        if channel_id.startswith("D"):
            await self._process_direct_message(user_id, text, channel_id)
    
    async def _handle_app_mention(self, event: Dict[str, Any]):
        """Handle app mention events."""
        user_id = event.get("user")
        channel_id = event.get("channel")
        text = event.get("text", "").strip()
        
        # Remove the bot mention from the text
        text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
        
        await self._process_direct_message(user_id, text, channel_id)
    
    async def _handle_reaction_added(self, event: Dict[str, Any]):
        """Handle reaction added events."""
        user_id = event.get("user")
        reaction = event.get("reaction")
        
        # Handle mood reactions
        if reaction in ["+1", "heart", "smile", "slightly_smiling_face"]:
            await self._handle_mood_reaction(user_id, reaction, "positive")
        elif reaction in ["-1", "broken_heart", "cry", "slightly_frowning_face"]:
            await self._handle_mood_reaction(user_id, reaction, "negative")
    
    async def _handle_interaction(self, payload: Dict[str, Any]):
        """Handle interactive components (buttons, menus, etc.)."""
        try:
            payload_data = json.loads(payload.get("payload", "{}"))
            callback_id = payload_data.get("callback_id")
            
            if callback_id == "mood_checkin":
                await self._handle_mood_checkin_interaction(payload_data)
            elif callback_id == "resource_selection":
                await self._handle_resource_selection_interaction(payload_data)
            elif callback_id == "wellness_report":
                await self._handle_wellness_report_interaction(payload_data)
                
        except Exception as e:
            logger.error(f"Error handling interaction: {e}")
    
    async def _handle_slash_command(self, payload: Dict[str, Any]):
        """Handle slash commands."""
        command = payload.get("command", "").lstrip("/")
        user_id = payload.get("user_id")
        text = payload.get("text", "").strip()
        
        if command in self.commands:
            await self.commands[command](user_id, text, payload)
        else:
            await self._send_ephemeral_message(
                user_id, 
                payload.get("channel_id"),
                f"Unknown command: `/{command}`. Use `/wellness help` for available commands."
            )
    
    async def _handle_help_command(self, user_id: str, text: str, payload: Dict[str, Any]):
        """Handle the help command."""
        help_text = """
*Wellness Companion Commands*

• `/wellness help` - Show this help message
• `/wellness checkin` - Start a wellness check-in
• `/wellness mood <1-10>` - Log your current mood (1=very low, 10=excellent)
• `/wellness resources [topic]` - Get wellness resources
• `/wellness report` - Get your wellness summary

*Quick Actions*
• React with :heart: or :+1: to log positive mood
• React with :broken_heart: or :-1: to log negative mood
• Mention me in any channel for a quick chat

*Privacy*
Your wellness data is private and anonymized. Only you can see your personal data.
        """
        
        await self._send_ephemeral_message(user_id, payload.get("channel_id"), help_text)
    
    async def _handle_checkin_command(self, user_id: str, text: str, payload: Dict[str, Any]):
        """Handle the checkin command."""
        # Create mood check-in buttons
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "How are you feeling today? Please rate your mood:"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "😢 1-2"},
                        "value": "1-2",
                        "action_id": "mood_1_2"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "😕 3-4"},
                        "value": "3-4",
                        "action_id": "mood_3_4"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "😐 5-6"},
                        "value": "5-6",
                        "action_id": "mood_5_6"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "🙂 7-8"},
                        "value": "7-8",
                        "action_id": "mood_7_8"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "😊 9-10"},
                        "value": "9-10",
                        "action_id": "mood_9_10"
                    }
                ]
            }
        ]
        
        await self._send_ephemeral_message(
            user_id, 
            payload.get("channel_id"),
            "How are you feeling today?",
            blocks=blocks
        )
    
    async def _handle_mood_command(self, user_id: str, text: str, payload: Dict[str, Any]):
        """Handle the mood command."""
        try:
            # Extract mood value from text
            mood_match = re.search(r'(\d+)', text)
            if mood_match:
                mood_value = int(mood_match.group(1))
                if 1 <= mood_value <= 10:
                    await self._log_mood(user_id, mood_value)
                    await self._send_ephemeral_message(
                        user_id,
                        payload.get("channel_id"),
                        f"Thanks! I've logged your mood as {mood_value}/10. Keep up the great work! 💪"
                    )
                else:
                    await self._send_ephemeral_message(
                        user_id,
                        payload.get("channel_id"),
                        "Please provide a mood value between 1 and 10."
                    )
            else:
                await self._send_ephemeral_message(
                    user_id,
                    payload.get("channel_id"),
                    "Please provide a mood value: `/wellness mood 7`"
                )
        except ValueError:
            await self._send_ephemeral_message(
                user_id,
                payload.get("channel_id"),
                "Please provide a valid number for your mood."
            )
    
    async def _handle_resources_command(self, user_id: str, text: str, payload: Dict[str, Any]):
        """Handle the resources command."""
        topic = text.strip() if text else "general"
        
        try:
            # Get user context
            user_info = await self._get_user_info(user_id)
            
            # Get resource recommendations
            result = await self.orchestrator.recommend_resources(
                user_needs=topic,
                user_preferences={"platform": "slack"},
                user_id=user_id,
                user_role=user_info.get("role", "employee")
            )
            
            if result.get("success") and result.get("data", {}).get("recommendations"):
                recommendations = result["data"]["recommendations"][:3]  # Limit to 3
                
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Wellness Resources for: {topic.title()}*"
                        }
                    }
                ]
                
                for rec in recommendations:
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{rec['title']}*\n{rec['description']}\nDuration: {rec.get('duration_minutes', 'N/A')} min"
                        }
                    })
                
                await self._send_ephemeral_message(
                    user_id,
                    payload.get("channel_id"),
                    f"Here are some wellness resources for '{topic}':",
                    blocks=blocks
                )
            else:
                await self._send_ephemeral_message(
                    user_id,
                    payload.get("channel_id"),
                    f"I couldn't find specific resources for '{topic}', but here are some general wellness tips:\n\n• Take regular breaks\n• Practice deep breathing\n• Stay hydrated\n• Move your body"
                )
                
        except Exception as e:
            logger.error(f"Error getting resources: {e}")
            await self._send_ephemeral_message(
                user_id,
                payload.get("channel_id"),
                "Sorry, I couldn't get resources right now. Please try again later."
            )
    
    async def _handle_report_command(self, user_id: str, text: str, payload: Dict[str, Any]):
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
                
                report_text = f"""
*Your Wellness Summary (Last 7 Days)*

📊 *Overall Wellness Score:* {data.get('overall_score', 'N/A')}/10
😊 *Average Mood:* {data.get('avg_mood', 'N/A')}/10
😰 *Stress Level:* {data.get('stress_level', 'N/A')}/10
💪 *Energy Level:* {data.get('energy_level', 'N/A')}/10

*Recent Activity:*
• Check-ins: {data.get('checkins_count', 0)}
• Resources used: {data.get('resources_used', 0)}
• Conversations: {data.get('conversations_count', 0)}

*Trends:*
{data.get('trends', 'No recent trends available')}
                """
                
                await self._send_ephemeral_message(
                    user_id,
                    payload.get("channel_id"),
                    report_text
                )
            else:
                await self._send_ephemeral_message(
                    user_id,
                    payload.get("channel_id"),
                    "I don't have enough data to generate a report yet. Try logging your mood and using the wellness features more!"
                )
                
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            await self._send_ephemeral_message(
                user_id,
                payload.get("channel_id"),
                "Sorry, I couldn't generate your report right now. Please try again later."
            )
    
    async def _process_direct_message(self, user_id: str, text: str, channel_id: str):
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
                await self._send_message(channel_id, response)
                
                # Handle high-risk situations
                if risk_level > 0.7:
                    await self._handle_high_risk_situation(user_id, channel_id, text, risk_level)
                    
            else:
                await self._send_message(
                    channel_id,
                    "I'm having trouble processing your message right now. Please try again later."
                )
                
        except Exception as e:
            logger.error(f"Error processing direct message: {e}")
            await self._send_message(
                channel_id,
                "Sorry, I encountered an error. Please try again later."
            )
    
    async def _handle_mood_reaction(self, user_id: str, reaction: str, mood_type: str):
        """Handle mood reactions."""
        try:
            # Map reaction to mood value
            mood_mapping = {
                "positive": {"+1": 8, "heart": 9, "smile": 7, "slightly_smiling_face": 6},
                "negative": {"-1": 3, "broken_heart": 2, "cry": 1, "slightly_frowning_face": 4}
            }
            
            mood_value = mood_mapping[mood_type].get(reaction, 5)
            await self._log_mood(user_id, mood_value)
            
            # Send confirmation
            user_info = await self._get_user_info(user_id)
            await self._send_ephemeral_message(
                user_id,
                user_id,  # DM channel
                f"Thanks for sharing your mood! I've logged it as {mood_value}/10. Keep taking care of yourself! 💙"
            )
            
        except Exception as e:
            logger.error(f"Error handling mood reaction: {e}")
    
    async def _handle_mood_checkin_interaction(self, payload: Dict[str, Any]):
        """Handle mood check-in button interactions."""
        user_id = payload.get("user", {}).get("id")
        action_id = payload.get("actions", [{}])[0].get("action_id")
        value = payload.get("actions", [{}])[0].get("value")
        
        if user_id and value:
            try:
                # Extract mood value from button value
                mood_range = value.split("-")
                mood_value = int(mood_range[0]) + (int(mood_range[1]) - int(mood_range[0])) // 2
                
                await self._log_mood(user_id, mood_value)
                
                # Update the message
                response_url = payload.get("response_url")
                if response_url:
                    await self._update_message(
                        response_url,
                        f"Thanks! I've logged your mood as {mood_value}/10. How can I help you today?"
                    )
                    
            except Exception as e:
                logger.error(f"Error handling mood check-in: {e}")
    
    async def _handle_resource_selection_interaction(self, payload: Dict[str, Any]):
        """Handle resource selection interactions."""
        user_id = payload.get("user", {}).get("id")
        selected_resource = payload.get("actions", [{}])[0].get("value")
        
        if user_id and selected_resource:
            try:
                # Get resource details
                result = await self.orchestrator.recommend_resources(
                    user_needs=selected_resource,
                    user_preferences={"platform": "slack"},
                    user_id=user_id,
                    user_role="employee"
                )
                
                if result.get("success") and result.get("data", {}).get("recommendations"):
                    resource = result["data"]["recommendations"][0]
                    
                    response_text = f"""
*{resource['title']}*

{resource['description']}

*Duration:* {resource.get('duration_minutes', 'N/A')} minutes
*Category:* {resource.get('category', 'N/A')}

{resource.get('content', 'No content available')}
                    """
                    
                    response_url = payload.get("response_url")
                    if response_url:
                        await self._update_message(response_url, response_text)
                        
            except Exception as e:
                logger.error(f"Error handling resource selection: {e}")
    
    async def _handle_wellness_report_interaction(self, payload: Dict[str, Any]):
        """Handle wellness report interactions."""
        # Similar to _handle_report_command but for interactive components
        pass
    
    async def _handle_high_risk_situation(self, user_id: str, channel_id: str, message: str, risk_level: float):
        """Handle high-risk situations."""
        try:
            # Send immediate support message
            support_message = """
🚨 *I'm concerned about what you're sharing.*

You're not alone, and there are people who want to help:

*Immediate Support:*
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

*Workplace Support:*
• Your HR department
• Employee Assistance Program (EAP)
• Your manager or trusted colleague

Would you like me to help you connect with any of these resources?
            """
            
            await self._send_message(channel_id, support_message)
            
            # Log the incident
            logger.warning(f"High-risk situation detected for user {user_id}: {message} (risk: {risk_level})")
            
            # TODO: Implement escalation to HR or management
            # await self._escalate_to_hr(user_id, message, risk_level)
            
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
        """Get user information from Slack."""
        try:
            user_info = self.client.users_info(user=user_id)
            return {
                "id": user_id,
                "name": user_info["user"]["name"],
                "real_name": user_info["user"]["real_name"],
                "email": user_info["user"].get("profile", {}).get("email"),
                "role": "employee"  # Default role, could be enhanced with user mapping
            }
        except SlackApiError as e:
            logger.error(f"Error getting user info: {e}")
            return {"id": user_id, "role": "employee"}
    
    def _get_session_id(self, user_id: str) -> str:
        """Get or create session ID for user."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = f"slack_{user_id}_{datetime.now().timestamp()}"
        return self.user_sessions[user_id]
    
    async def _send_message(self, channel_id: str, text: str, blocks: List[Dict] = None):
        """Send a message to a channel."""
        try:
            kwargs = {
                "channel": channel_id,
                "text": text,
                "username": self.bot_name,
                "icon_emoji": self.bot_icon
            }
            
            if blocks:
                kwargs["blocks"] = blocks
            
            self.client.chat_postMessage(**kwargs)
            
        except SlackApiError as e:
            logger.error(f"Error sending message: {e}")
    
    async def _send_ephemeral_message(self, user_id: str, channel_id: str, text: str, blocks: List[Dict] = None):
        """Send an ephemeral message to a user."""
        try:
            kwargs = {
                "channel": channel_id,
                "user": user_id,
                "text": text,
                "username": self.bot_name,
                "icon_emoji": self.bot_icon
            }
            
            if blocks:
                kwargs["blocks"] = blocks
            
            self.client.chat_postEphemeral(**kwargs)
            
        except SlackApiError as e:
            logger.error(f"Error sending ephemeral message: {e}")
    
    async def _update_message(self, response_url: str, text: str, blocks: List[Dict] = None):
        """Update a message using response URL."""
        try:
            import httpx
            
            payload = {
                "text": text,
                "username": self.bot_name,
                "icon_emoji": self.bot_icon
            }
            
            if blocks:
                payload["blocks"] = blocks
            
            async with httpx.AsyncClient() as client:
                await client.post(response_url, json=payload)
                
        except Exception as e:
            logger.error(f"Error updating message: {e}")
    
    async def _escalate_to_hr(self, user_id: str, message: str, risk_level: float):
        """Escalate high-risk situation to HR."""
        # TODO: Implement HR escalation
        logger.warning(f"HR escalation needed for user {user_id} with risk level {risk_level}")
        pass

# Global Slack integration instance
slack_integration = SlackIntegration()

# Export commonly used functions and classes
__all__ = [
    'SlackIntegration',
    'slack_integration'
]
