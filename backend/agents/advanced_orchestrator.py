"""
Advanced Agent Orchestrator - Demonstrates sophisticated multi-agent collaboration
"""

from typing import Dict, Any, List, Optional, Tuple, Callable
from datetime import datetime, timedelta
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
import uuid
import json
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from collections import defaultdict

from .base_agent import BaseAgent, AgentType, AgentContext, AgentResponse
from .wellness_companion_agent import WellnessCompanionAgent
from .resource_recommendation_agent import ResourceRecommendationAgent
from .sentiment_risk_detection_agent import SentimentRiskDetectionAgent
from .analytics_reporting_agent import AnalyticsReportingAgent
from .policy_privacy_agent import PolicyPrivacyAgent

from config.settings import settings


class CollaborationPattern(Enum):
    """Advanced collaboration patterns for agent interaction"""
    HIERARCHICAL = "hierarchical"  # Top-down decision making
    PEER_TO_PEER = "peer_to_peer"  # Equal agent collaboration
    EMERGENT = "emergent"  # Self-organizing behavior
    CONSENSUS = "consensus"  # Group decision making
    COMPETITIVE = "competitive"  # Agent competition for resources


class AgentCapability(Enum):
    """Agent capabilities for dynamic composition"""
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    RISK_DETECTION = "risk_detection"
    RESOURCE_MATCHING = "resource_matching"
    PRIVACY_ENFORCEMENT = "privacy_enforcement"
    ANALYTICS_GENERATION = "analytics_generation"
    CONVERSATION_MANAGEMENT = "conversation_management"
    CRISIS_INTERVENTION = "crisis_intervention"
    PREDICTIVE_MODELING = "predictive_modeling"


@dataclass
class AgentState:
    """Dynamic agent state for collaboration"""
    agent_id: str
    agent_type: AgentType
    capabilities: List[AgentCapability]
    current_load: float
    performance_score: float
    availability: bool
    last_activity: datetime
    collaboration_history: List[str] = field(default_factory=list)
    trust_score: float = 1.0


@dataclass
class CollaborationRequest:
    """Request for agent collaboration"""
    request_id: str
    initiator_agent: AgentType
    target_agents: List[AgentType]
    collaboration_pattern: CollaborationPattern
    context: AgentContext
    data: Dict[str, Any]
    priority: int = 1
    timeout: float = 30.0
    required_capabilities: List[AgentCapability] = field(default_factory=list)


@dataclass
class CollaborationResult:
    """Result of agent collaboration"""
    request_id: str
    success: bool
    participating_agents: List[AgentType]
    final_response: AgentResponse
    collaboration_time: float
    agent_contributions: Dict[AgentType, Dict[str, Any]]
    emergent_insights: List[str]
    trust_updates: Dict[AgentType, float]


class AdvancedAgentOrchestrator:
    """
    Advanced Agent Orchestrator demonstrating sophisticated multi-agent collaboration:
    - Dynamic workflow composition
    - Agent negotiation and consensus building
    - Emergent behavior patterns
    - Adaptive collaboration strategies
    - Performance-based agent selection
    """
    
    def __init__(self):
        self.logger = logging.getLogger("advanced_agent_orchestrator")
        
        # Initialize agents with enhanced capabilities
        self.agents = {}
        self.agent_states = {}
        self._initialize_agents()
        
        # Collaboration management
        self.active_collaborations = {}
        self.collaboration_history = []
        self.trust_network = defaultdict(lambda: defaultdict(float))
        
        # Performance tracking
        self.performance_metrics = defaultdict(list)
        self.workload_distribution = defaultdict(float)
        
        # Dynamic composition engine
        self.composition_engine = DynamicCompositionEngine()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _initialize_agents(self):
        """Initialize agents with enhanced capabilities"""
        try:
            # Create agents with specific capabilities
            wellness_agent = WellnessCompanionAgent()
            wellness_agent.capabilities = [
                AgentCapability.CONVERSATION_MANAGEMENT,
                AgentCapability.CRISIS_INTERVENTION
            ]
            
            resource_agent = ResourceRecommendationAgent()
            resource_agent.capabilities = [
                AgentCapability.RESOURCE_MATCHING,
                AgentCapability.PREDICTIVE_MODELING
            ]
            
            sentiment_agent = SentimentRiskDetectionAgent()
            sentiment_agent.capabilities = [
                AgentCapability.SENTIMENT_ANALYSIS,
                AgentCapability.RISK_DETECTION
            ]
            
            analytics_agent = AnalyticsReportingAgent()
            analytics_agent.capabilities = [
                AgentCapability.ANALYTICS_GENERATION,
                AgentCapability.PREDICTIVE_MODELING
            ]
            
            privacy_agent = PolicyPrivacyAgent()
            privacy_agent.capabilities = [
                AgentCapability.PRIVACY_ENFORCEMENT
            ]
            
            self.agents = {
                AgentType.WELLNESS_COMPANION: wellness_agent,
                AgentType.RESOURCE_RECOMMENDATION: resource_agent,
                AgentType.SENTIMENT_RISK_DETECTION: sentiment_agent,
                AgentType.ANALYTICS_REPORTING: analytics_agent,
                AgentType.POLICY_PRIVACY: privacy_agent,
            }
            
            # Initialize agent states
            for agent_type, agent in self.agents.items():
                self.agent_states[agent_type] = AgentState(
                    agent_id=str(uuid.uuid4()),
                    agent_type=agent_type,
                    capabilities=getattr(agent, 'capabilities', []),
                    current_load=0.0,
                    performance_score=1.0,
                    availability=True,
                    last_activity=datetime.now()
                )
            
            self.logger.info("Advanced agents initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize advanced agents: {e}")
            raise
    
    async def orchestrate_collaboration(
        self,
        context: AgentContext,
        data: Dict[str, Any],
        collaboration_pattern: CollaborationPattern = CollaborationPattern.EMERGENT
    ) -> CollaborationResult:
        """
        Orchestrate sophisticated multi-agent collaboration
        """
        request_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # Create collaboration request
        request = CollaborationRequest(
            request_id=request_id,
            initiator_agent=AgentType.WELLNESS_COMPANION,  # Default initiator
            target_agents=[],
            collaboration_pattern=collaboration_pattern,
            context=context,
            data=data,
            required_capabilities=self._determine_required_capabilities(data)
        )
        
        try:
            # Select optimal agent combination
            selected_agents = await self._select_optimal_agents(request)
            request.target_agents = selected_agents
            
            # Execute collaboration based on pattern
            if collaboration_pattern == CollaborationPattern.EMERGENT:
                result = await self._execute_emergent_collaboration(request)
            elif collaboration_pattern == CollaborationPattern.CONSENSUS:
                result = await self._execute_consensus_collaboration(request)
            elif collaboration_pattern == CollaborationPattern.HIERARCHICAL:
                result = await self._execute_hierarchical_collaboration(request)
            elif collaboration_pattern == CollaborationPattern.PEER_TO_PEER:
                result = await self._execute_peer_collaboration(request)
            else:
                result = await self._execute_competitive_collaboration(request)
            
            # Update performance metrics
            collaboration_time = (datetime.now() - start_time).total_seconds()
            result.collaboration_time = collaboration_time
            
            # Update trust network
            await self._update_trust_network(result)
            
            # Store collaboration history
            self.collaboration_history.append(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Collaboration failed: {e}")
            return CollaborationResult(
                request_id=request_id,
                success=False,
                participating_agents=[],
                final_response=AgentResponse(
                    success=False,
                    data={},
                    message=f"Collaboration failed: {str(e)}"
                ),
                collaboration_time=(datetime.now() - start_time).total_seconds(),
                agent_contributions={},
                emergent_insights=[],
                trust_updates={}
            )
    
    async def _select_optimal_agents(self, request: CollaborationRequest) -> List[AgentType]:
        """
        Select optimal agents based on capabilities, performance, and availability
        """
        available_agents = []
        
        for agent_type, state in self.agent_states.items():
            if not state.availability or state.current_load > 0.8:
                continue
                
            # Check if agent has required capabilities
            has_required_capabilities = all(
                capability in state.capabilities 
                for capability in request.required_capabilities
            )
            
            if has_required_capabilities:
                # Calculate selection score based on performance and load
                selection_score = (
                    state.performance_score * 0.4 +
                    (1 - state.current_load) * 0.3 +
                    state.trust_score * 0.3
                )
                
                available_agents.append((agent_type, selection_score))
        
        # Sort by selection score and return top agents
        available_agents.sort(key=lambda x: x[1], reverse=True)
        
        # Limit to reasonable number of agents (2-4 for most collaborations)
        max_agents = min(len(available_agents), 4)
        return [agent_type for agent_type, _ in available_agents[:max_agents]]
    
    async def _execute_emergent_collaboration(self, request: CollaborationRequest) -> CollaborationResult:
        """
        Execute emergent collaboration where agents self-organize
        """
        agent_contributions = {}
        emergent_insights = []
        
        # Start all agents simultaneously
        tasks = []
        for agent_type in request.target_agents:
            task = asyncio.create_task(
                self._execute_agent_with_context(agent_type, request.context, request.data)
            )
            tasks.append((agent_type, task))
        
        # Collect initial responses
        initial_responses = {}
        for agent_type, task in tasks:
            try:
                response = await asyncio.wait_for(task, timeout=request.timeout)
                initial_responses[agent_type] = response
                agent_contributions[agent_type] = {
                    "initial_response": response,
                    "contribution_type": "primary_analysis"
                }
            except asyncio.TimeoutError:
                self.logger.warning(f"Agent {agent_type} timed out")
                continue
        
        # Emergent behavior: agents react to each other's responses
        for agent_type, response in initial_responses.items():
            if response.success and response.data:
                # Other agents can build upon this response
                for other_agent_type in request.target_agents:
                    if other_agent_type != agent_type:
                        try:
                            enhanced_data = {
                                **request.data,
                                "peer_insights": response.data,
                                "peer_agent": agent_type.value
                            }
                            
                            enhanced_response = await self._execute_agent_with_context(
                                other_agent_type, request.context, enhanced_data
                            )
                            
                            if enhanced_response.success:
                                agent_contributions[other_agent_type]["enhanced_response"] = enhanced_response
                                emergent_insights.append(
                                    f"{other_agent_type.value} built upon {agent_type.value}'s insights"
                                )
                                
                        except Exception as e:
                            self.logger.error(f"Emergent collaboration failed for {other_agent_type}: {e}")
        
        # Synthesize final response
        final_response = await self._synthesize_collaboration_results(
            agent_contributions, request.context
        )
        
        return CollaborationResult(
            request_id=request.request_id,
            success=final_response.success,
            participating_agents=request.target_agents,
            final_response=final_response,
            collaboration_time=0.0,  # Will be set by caller
            agent_contributions=agent_contributions,
            emergent_insights=emergent_insights,
            trust_updates={}
        )
    
    async def _execute_consensus_collaboration(self, request: CollaborationRequest) -> CollaborationResult:
        """
        Execute consensus-based collaboration where agents must agree
        """
        agent_contributions = {}
        consensus_rounds = []
        
        # Initial round: all agents provide their analysis
        initial_responses = {}
        for agent_type in request.target_agents:
            response = await self._execute_agent_with_context(agent_type, request.context, request.data)
            initial_responses[agent_type] = response
            agent_contributions[agent_type] = {
                "initial_response": response,
                "consensus_votes": []
            }
        
        # Consensus building rounds
        max_rounds = 3
        consensus_reached = False
        
        for round_num in range(max_rounds):
            round_responses = {}
            
            # Each agent reviews others' responses and provides consensus vote
            for agent_type in request.target_agents:
                consensus_data = {
                    **request.data,
                    "consensus_round": round_num,
                    "peer_responses": {
                        agent: resp.data for agent, resp in initial_responses.items()
                        if agent != agent_type and resp.success
                    }
                }
                
                consensus_response = await self._execute_agent_with_context(
                    agent_type, request.context, consensus_data
                )
                
                round_responses[agent_type] = consensus_response
                agent_contributions[agent_type]["consensus_votes"].append(consensus_response)
            
            # Check for consensus
            consensus_scores = []
            for agent_type, response in round_responses.items():
                if response.success and "consensus_score" in response.data:
                    consensus_scores.append(response.data["consensus_score"])
            
            if len(consensus_scores) > 0 and np.mean(consensus_scores) > 0.8:
                consensus_reached = True
                break
            
            consensus_rounds.append(round_responses)
        
        # Synthesize consensus result
        final_response = await self._synthesize_consensus_results(
            agent_contributions, consensus_rounds, request.context
        )
        
        return CollaborationResult(
            request_id=request.request_id,
            success=final_response.success,
            participating_agents=request.target_agents,
            final_response=final_response,
            collaboration_time=0.0,
            agent_contributions=agent_contributions,
            emergent_insights=[f"Consensus {'reached' if consensus_reached else 'not reached'} after {len(consensus_rounds)} rounds"],
            trust_updates={}
        )
    
    async def _execute_hierarchical_collaboration(self, request: CollaborationRequest) -> CollaborationResult:
        """
        Execute hierarchical collaboration with clear decision hierarchy
        """
        agent_contributions = {}
        
        # Define hierarchy: Privacy -> Sentiment -> Analytics -> Resource -> Wellness
        hierarchy = [
            AgentType.POLICY_PRIVACY,
            AgentType.SENTIMENT_RISK_DETECTION,
            AgentType.ANALYTICS_REPORTING,
            AgentType.RESOURCE_RECOMMENDATION,
            AgentType.WELLNESS_COMPANION
        ]
        
        # Filter to available agents in hierarchy
        available_hierarchy = [agent for agent in hierarchy if agent in request.target_agents]
        
        current_data = request.data
        hierarchical_responses = {}
        
        # Execute in hierarchical order
        for agent_type in available_hierarchy:
            try:
                response = await self._execute_agent_with_context(
                    agent_type, request.context, current_data
                )
                
                hierarchical_responses[agent_type] = response
                agent_contributions[agent_type] = {
                    "hierarchical_response": response,
                    "level": available_hierarchy.index(agent_type)
                }
                
                # Pass enhanced data to next level
                if response.success and response.data:
                    current_data = {**current_data, **response.data}
                    
            except Exception as e:
                self.logger.error(f"Hierarchical collaboration failed at {agent_type}: {e}")
                break
        
        # Final response comes from the highest level agent that participated
        final_agent = available_hierarchy[-1] if available_hierarchy else request.initiator_agent
        final_response = hierarchical_responses.get(final_agent, AgentResponse(
            success=False, data={}, message="Hierarchical collaboration failed"
        ))
        
        return CollaborationResult(
            request_id=request.request_id,
            success=final_response.success,
            participating_agents=available_hierarchy,
            final_response=final_response,
            collaboration_time=0.0,
            agent_contributions=agent_contributions,
            emergent_insights=[f"Hierarchical collaboration completed with {len(available_hierarchy)} levels"],
            trust_updates={}
        )
    
    async def _execute_peer_collaboration(self, request: CollaborationRequest) -> CollaborationResult:
        """
        Execute peer-to-peer collaboration where agents work as equals
        """
        agent_contributions = {}
        
        # Execute all agents in parallel
        tasks = []
        for agent_type in request.target_agents:
            task = asyncio.create_task(
                self._execute_agent_with_context(agent_type, request.context, request.data)
            )
            tasks.append((agent_type, task))
        
        # Collect responses
        peer_responses = {}
        for agent_type, task in tasks:
            try:
                response = await asyncio.wait_for(task, timeout=request.timeout)
                peer_responses[agent_type] = response
                agent_contributions[agent_type] = {
                    "peer_response": response,
                    "collaboration_type": "parallel"
                }
            except asyncio.TimeoutError:
                self.logger.warning(f"Peer agent {agent_type} timed out")
                continue
        
        # Synthesize peer responses
        final_response = await self._synthesize_peer_results(peer_responses, request.context)
        
        return CollaborationResult(
            request_id=request.request_id,
            success=final_response.success,
            participating_agents=request.target_agents,
            final_response=final_response,
            collaboration_time=0.0,
            agent_contributions=agent_contributions,
            emergent_insights=["Peer collaboration completed successfully"],
            trust_updates={}
        )
    
    async def _execute_competitive_collaboration(self, request: CollaborationRequest) -> CollaborationResult:
        """
        Execute competitive collaboration where agents compete for best solution
        """
        agent_contributions = {}
        competitive_responses = {}
        
        # All agents compete to provide the best solution
        tasks = []
        for agent_type in request.target_agents:
            task = asyncio.create_task(
                self._execute_agent_with_context(agent_type, request.context, request.data)
            )
            tasks.append((agent_type, task))
        
        # Collect competitive responses
        for agent_type, task in tasks:
            try:
                response = await asyncio.wait_for(task, timeout=request.timeout)
                competitive_responses[agent_type] = response
                agent_contributions[agent_type] = {
                    "competitive_response": response,
                    "competition_type": "solution_quality"
                }
            except asyncio.TimeoutError:
                self.logger.warning(f"Competitive agent {agent_type} timed out")
                continue
        
        # Evaluate and select best response
        best_response = await self._evaluate_competitive_responses(
            competitive_responses, request.context
        )
        
        return CollaborationResult(
            request_id=request.request_id,
            success=best_response.success,
            participating_agents=request.target_agents,
            final_response=best_response,
            collaboration_time=0.0,
            agent_contributions=agent_contributions,
            emergent_insights=["Competitive collaboration completed, best solution selected"],
            trust_updates={}
        )
    
    async def _execute_agent_with_context(
        self, 
        agent_type: AgentType, 
        context: AgentContext, 
        data: Dict[str, Any]
    ) -> AgentResponse:
        """Execute an agent with proper context and error handling"""
        try:
            # Update agent state
            self.agent_states[agent_type].current_load += 0.1
            self.agent_states[agent_type].last_activity = datetime.now()
            
            # Execute agent
            agent = self.agents[agent_type]
            response = await agent.handle_request(context, data)
            
            # Update performance metrics
            self.performance_metrics[agent_type].append({
                "timestamp": datetime.now(),
                "response_time": getattr(response, 'response_time', 0),
                "success": response.success
            })
            
            return response
            
        except Exception as e:
            self.logger.error(f"Agent {agent_type} execution failed: {e}")
            return AgentResponse(
                success=False,
                data={},
                message=f"Agent execution failed: {str(e)}"
            )
        finally:
            # Update agent state
            self.agent_states[agent_type].current_load = max(0, self.agent_states[agent_type].current_load - 0.1)
    
    async def _synthesize_collaboration_results(
        self, 
        agent_contributions: Dict[AgentType, Dict[str, Any]], 
        context: AgentContext
    ) -> AgentResponse:
        """Synthesize results from emergent collaboration"""
        # Combine insights from all agents
        combined_data = {}
        insights = []
        
        for agent_type, contributions in agent_contributions.items():
            if "initial_response" in contributions:
                response = contributions["initial_response"]
                if response.success and response.data:
                    combined_data[f"{agent_type.value}_insights"] = response.data
                    insights.append(f"{agent_type.value}: {response.message}")
            
            if "enhanced_response" in contributions:
                response = contributions["enhanced_response"]
                if response.success and response.data:
                    combined_data[f"{agent_type.value}_enhanced"] = response.data
        
        return AgentResponse(
            success=len(combined_data) > 0,
            data=combined_data,
            message=f"Emergent collaboration completed with {len(insights)} insights",
            risk_level=self._calculate_aggregate_risk(agent_contributions)
        )
    
    async def _synthesize_consensus_results(
        self,
        agent_contributions: Dict[AgentType, Dict[str, Any]],
        consensus_rounds: List[Dict[AgentType, AgentResponse]],
        context: AgentContext
    ) -> AgentResponse:
        """Synthesize results from consensus collaboration"""
        # Analyze consensus patterns
        consensus_data = {
            "consensus_rounds": len(consensus_rounds),
            "participating_agents": list(agent_contributions.keys()),
            "consensus_reached": len(consensus_rounds) > 0
        }
        
        # Combine final consensus insights
        final_insights = {}
        for agent_type, contributions in agent_contributions.items():
            if contributions["consensus_votes"]:
                final_vote = contributions["consensus_votes"][-1]
                if final_vote.success:
                    final_insights[agent_type.value] = final_vote.data
        
        consensus_data["final_insights"] = final_insights
        
        return AgentResponse(
            success=len(final_insights) > 0,
            data=consensus_data,
            message=f"Consensus collaboration completed with {len(final_insights)} agreeing agents"
        )
    
    async def _synthesize_peer_results(
        self,
        peer_responses: Dict[AgentType, AgentResponse],
        context: AgentContext
    ) -> AgentResponse:
        """Synthesize results from peer collaboration"""
        # Combine all peer responses
        combined_data = {}
        successful_responses = 0
        
        for agent_type, response in peer_responses.items():
            if response.success:
                combined_data[agent_type.value] = response.data
                successful_responses += 1
        
        return AgentResponse(
            success=successful_responses > 0,
            data=combined_data,
            message=f"Peer collaboration completed with {successful_responses} successful responses"
        )
    
    async def _evaluate_competitive_responses(
        self,
        competitive_responses: Dict[AgentType, AgentResponse],
        context: AgentContext
    ) -> AgentResponse:
        """Evaluate and select the best competitive response"""
        best_response = None
        best_score = -1
        
        for agent_type, response in competitive_responses.items():
            if response.success:
                # Calculate quality score based on response characteristics
                score = self._calculate_response_quality(response, agent_type)
                if score > best_score:
                    best_score = score
                    best_response = response
        
        if best_response:
            best_response.data["competitive_score"] = best_score
            best_response.data["competing_agents"] = len(competitive_responses)
        
        return best_response or AgentResponse(
            success=False,
            data={},
            message="No successful competitive responses"
        )
    
    def _calculate_response_quality(self, response: AgentResponse, agent_type: AgentType) -> float:
        """Calculate quality score for competitive evaluation"""
        score = 0.0
        
        # Base score for successful response
        if response.success:
            score += 0.3
        
        # Score based on data richness
        if response.data:
            score += min(len(response.data) * 0.1, 0.3)
        
        # Score based on agent performance history
        if agent_type in self.performance_metrics:
            recent_performance = self.performance_metrics[agent_type][-10:]
            if recent_performance:
                avg_success = sum(1 for p in recent_performance if p["success"]) / len(recent_performance)
                score += avg_success * 0.2
        
        # Score based on risk assessment
        if response.risk_level is not None:
            score += (1 - response.risk_level) * 0.2
        
        return min(score, 1.0)
    
    def _calculate_aggregate_risk(self, agent_contributions: Dict[AgentType, Dict[str, Any]]) -> float:
        """Calculate aggregate risk level from all agent contributions"""
        risk_scores = []
        
        for agent_type, contributions in agent_contributions.items():
            if "initial_response" in contributions:
                response = contributions["initial_response"]
                if response.risk_level is not None:
                    risk_scores.append(response.risk_level)
        
        return np.mean(risk_scores) if risk_scores else 0.0
    
    def _determine_required_capabilities(self, data: Dict[str, Any]) -> List[AgentCapability]:
        """Determine required capabilities based on request data"""
        required_capabilities = []
        
        if "message" in data or "conversation" in data:
            required_capabilities.append(AgentCapability.CONVERSATION_MANAGEMENT)
        
        if any(keyword in str(data).lower() for keyword in ["stress", "anxiety", "depression", "crisis"]):
            required_capabilities.append(AgentCapability.CRISIS_INTERVENTION)
        
        if "sentiment" in data or "mood" in data:
            required_capabilities.append(AgentCapability.SENTIMENT_ANALYSIS)
        
        if "risk" in data or "burnout" in data:
            required_capabilities.append(AgentCapability.RISK_DETECTION)
        
        if "resource" in data or "recommendation" in data:
            required_capabilities.append(AgentCapability.RESOURCE_MATCHING)
        
        if "analytics" in data or "report" in data:
            required_capabilities.append(AgentCapability.ANALYTICS_GENERATION)
        
        if "privacy" in data or "compliance" in data:
            required_capabilities.append(AgentCapability.PRIVACY_ENFORCEMENT)
        
        return required_capabilities
    
    async def _update_trust_network(self, result: CollaborationResult):
        """Update trust network based on collaboration results"""
        for agent_type in result.participating_agents:
            if agent_type in result.trust_updates:
                # Update trust score for this agent
                current_trust = self.agent_states[agent_type].trust_score
                trust_update = result.trust_updates[agent_type]
                self.agent_states[agent_type].trust_score = max(0, min(1, current_trust + trust_update))
    
    def _start_background_tasks(self):
        """Start background tasks for performance monitoring and optimization"""
        asyncio.create_task(self._performance_monitoring_task())
        asyncio.create_task(self._workload_balancing_task())
    
    async def _performance_monitoring_task(self):
        """Background task for monitoring agent performance"""
        while True:
            try:
                # Update performance scores based on recent metrics
                for agent_type, metrics in self.performance_metrics.items():
                    if metrics:
                        recent_metrics = metrics[-20:]  # Last 20 interactions
                        success_rate = sum(1 for m in recent_metrics if m["success"]) / len(recent_metrics)
                        avg_response_time = np.mean([m["response_time"] for m in recent_metrics if m["response_time"] > 0])
                        
                        # Update performance score
                        performance_score = success_rate * 0.7 + (1 - min(avg_response_time / 10, 1)) * 0.3
                        self.agent_states[agent_type].performance_score = performance_score
                
                await asyncio.sleep(60)  # Update every minute
                
            except Exception as e:
                self.logger.error(f"Performance monitoring task failed: {e}")
                await asyncio.sleep(60)
    
    async def _workload_balancing_task(self):
        """Background task for workload balancing"""
        while True:
            try:
                # Gradually reduce load for all agents
                for agent_type, state in self.agent_states.items():
                    state.current_load = max(0, state.current_load - 0.05)
                
                await asyncio.sleep(30)  # Update every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Workload balancing task failed: {e}")
                await asyncio.sleep(30)


class DynamicCompositionEngine:
    """
    Engine for dynamically composing agent workflows based on requirements
    """
    
    def __init__(self):
        self.composition_rules = {}
        self.workflow_templates = {}
        self._initialize_composition_rules()
    
    def _initialize_composition_rules(self):
        """Initialize rules for dynamic workflow composition"""
        self.composition_rules = {
            "crisis_detection": {
                "required_agents": [
                    AgentType.SENTIMENT_RISK_DETECTION,
                    AgentType.WELLNESS_COMPANION
                ],
                "optional_agents": [
                    AgentType.RESOURCE_RECOMMENDATION
                ],
                "collaboration_pattern": CollaborationPattern.HIERARCHICAL
            },
            "wellness_assessment": {
                "required_agents": [
                    AgentType.WELLNESS_COMPANION,
                    AgentType.SENTIMENT_RISK_DETECTION
                ],
                "optional_agents": [
                    AgentType.ANALYTICS_REPORTING
                ],
                "collaboration_pattern": CollaborationPattern.PEER_TO_PEER
            },
            "resource_recommendation": {
                "required_agents": [
                    AgentType.RESOURCE_RECOMMENDATION
                ],
                "optional_agents": [
                    AgentType.ANALYTICS_REPORTING,
                    AgentType.SENTIMENT_RISK_DETECTION
                ],
                "collaboration_pattern": CollaborationPattern.EMERGENT
            }
        }
    
    def compose_workflow(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Compose a workflow based on requirements"""
        workflow_type = requirements.get("workflow_type", "general")
        
        if workflow_type in self.composition_rules:
            rule = self.composition_rules[workflow_type]
            return {
                "agents": rule["required_agents"] + rule["optional_agents"],
                "pattern": rule["collaboration_pattern"],
                "priority": requirements.get("priority", 1)
            }
        
        # Default composition
        return {
            "agents": [AgentType.WELLNESS_COMPANION],
            "pattern": CollaborationPattern.PEER_TO_PEER,
            "priority": 1
        }
