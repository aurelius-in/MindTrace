"""
Agent Orchestrator - Coordinates all agents in the Enterprise Employee Wellness AI system
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

from .base_agent import BaseAgent, AgentType, AgentContext, AgentResponse
from .wellness_companion_agent import WellnessCompanionAgent
from .resource_recommendation_agent import ResourceRecommendationAgent
from .sentiment_risk_detection_agent import SentimentRiskDetectionAgent
from .analytics_reporting_agent import AnalyticsReportingAgent
from .policy_privacy_agent import PolicyPrivacyAgent

from config.settings import settings


class WorkflowType(Enum):
    """Types of workflows that can be orchestrated"""
    EMPLOYEE_CONVERSATION = "employee_conversation"
    RISK_ASSESSMENT = "risk_assessment"
    RESOURCE_RECOMMENDATION = "resource_recommendation"
    ANALYTICS_GENERATION = "analytics_generation"
    COMPLIANCE_AUDIT = "compliance_audit"


@dataclass
class WorkflowStep:
    """Workflow step definition"""
    agent_type: AgentType
    operation: str
    input_mapping: Dict[str, str]
    output_mapping: Dict[str, str]
    required: bool = True
    parallel: bool = False


@dataclass
class WorkflowResult:
    """Result of a workflow execution"""
    workflow_type: WorkflowType
    success: bool
    steps_completed: List[str]
    final_output: Dict[str, Any]
    errors: List[str]
    execution_time: float


class AgentOrchestrator:
    """
    Agent Orchestrator coordinates all agents in the system:
    - Wellness Companion Agent
    - Resource Recommendation Agent
    - Sentiment & Risk Detection Agent
    - Analytics & Reporting Agent
    - Policy & Privacy Agent
    """
    
    def __init__(self):
        self.logger = logging.getLogger("agent_orchestrator")
        
        # Initialize all agents
        self.agents = {}
        self._initialize_agents()
        
        # Define workflows
        self.workflows = {}
        self._define_workflows()
        
        # Performance tracking
        self.workflow_stats = {}
    
    def _initialize_agents(self):
        """Initialize all agents in the system"""
        try:
            self.agents[AgentType.WELLNESS_COMPANION] = WellnessCompanionAgent()
            self.agents[AgentType.RESOURCE_RECOMMENDATION] = ResourceRecommendationAgent()
            self.agents[AgentType.SENTIMENT_RISK_DETECTION] = SentimentRiskDetectionAgent()
            self.agents[AgentType.ANALYTICS_REPORTING] = AnalyticsReportingAgent()
            self.agents[AgentType.POLICY_PRIVACY] = PolicyPrivacyAgent()
            
            self.logger.info("All agents initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agents: {e}")
            raise
    
    def _define_workflows(self):
        """Define the workflows for different use cases"""
        
        # Employee conversation workflow
        self.workflows[WorkflowType.EMPLOYEE_CONVERSATION] = [
            WorkflowStep(
                agent_type=AgentType.POLICY_PRIVACY,
                operation="privacy_check",
                input_mapping={"content": "user_message"},
                output_mapping={"anonymized_content": "cleaned_message"}
            ),
            WorkflowStep(
                agent_type=AgentType.SENTIMENT_RISK_DETECTION,
                operation="process_request",
                input_mapping={"text": "cleaned_message"},
                output_mapping={"risk_level": "risk_assessment", "sentiment": "sentiment_analysis"}
            ),
            WorkflowStep(
                agent_type=AgentType.WELLNESS_COMPANION,
                operation="process_request",
                input_mapping={"message": "cleaned_message", "risk_level": "risk_assessment"},
                output_mapping={"response": "ai_response", "suggestions": "wellness_suggestions"}
            ),
            WorkflowStep(
                agent_type=AgentType.RESOURCE_RECOMMENDATION,
                operation="process_request",
                input_mapping={"needs": "cleaned_message", "risk_level": "risk_assessment"},
                output_mapping={"recommendations": "resource_recommendations"},
                required=False
            ),
            WorkflowStep(
                agent_type=AgentType.ANALYTICS_REPORTING,
                operation="process_request",
                input_mapping={"user_data": "all_data"},
                output_mapping={"insights": "analytics_insights"},
                required=False,
                parallel=True
            )
        ]
        
        # Risk assessment workflow
        self.workflows[WorkflowType.RISK_ASSESSMENT] = [
            WorkflowStep(
                agent_type=AgentType.POLICY_PRIVACY,
                operation="privacy_check",
                input_mapping={"content": "input_data"},
                output_mapping={"anonymized_content": "cleaned_data"}
            ),
            WorkflowStep(
                agent_type=AgentType.SENTIMENT_RISK_DETECTION,
                operation="process_request",
                input_mapping={"text": "cleaned_data"},
                output_mapping={"risk_indicators": "risk_analysis", "overall_risk": "risk_level"}
            ),
            WorkflowStep(
                agent_type=AgentType.ANALYTICS_REPORTING,
                operation="process_request",
                input_mapping={"risk_data": "risk_analysis"},
                output_mapping={"trends": "risk_trends", "predictions": "risk_predictions"}
            )
        ]
        
        # Resource recommendation workflow
        self.workflows[WorkflowType.RESOURCE_RECOMMENDATION] = [
            WorkflowStep(
                agent_type=AgentType.POLICY_PRIVACY,
                operation="privacy_check",
                input_mapping={"content": "user_needs"},
                output_mapping={"anonymized_content": "cleaned_needs"}
            ),
            WorkflowStep(
                agent_type=AgentType.RESOURCE_RECOMMENDATION,
                operation="process_request",
                input_mapping={"needs": "cleaned_needs", "preferences": "user_preferences"},
                output_mapping={"recommendations": "resource_recommendations"}
            ),
            WorkflowStep(
                agent_type=AgentType.ANALYTICS_REPORTING,
                operation="process_request",
                input_mapping={"recommendation_data": "resource_recommendations"},
                output_mapping={"effectiveness": "recommendation_effectiveness"},
                required=False
            )
        ]
        
        # Analytics generation workflow
        self.workflows[WorkflowType.ANALYTICS_GENERATION] = [
            WorkflowStep(
                agent_type=AgentType.POLICY_PRIVACY,
                operation="policy_enforcement",
                input_mapping={"content": "raw_data", "user_role": "requesting_role"},
                output_mapping={"filtered_content": "authorized_data"}
            ),
            WorkflowStep(
                agent_type=AgentType.ANALYTICS_REPORTING,
                operation="process_request",
                input_mapping={"data": "authorized_data"},
                output_mapping={"report": "analytics_report"}
            ),
            WorkflowStep(
                agent_type=AgentType.POLICY_PRIVACY,
                operation="anonymize_data",
                input_mapping={"content": "analytics_report"},
                output_mapping={"anonymized_report": "final_report"}
            )
        ]
        
        # Compliance audit workflow
        self.workflows[WorkflowType.COMPLIANCE_AUDIT] = [
            WorkflowStep(
                agent_type=AgentType.POLICY_PRIVACY,
                operation="compliance_audit",
                input_mapping={"content": "system_data"},
                output_mapping={"audit_results": "compliance_report"}
            ),
            WorkflowStep(
                agent_type=AgentType.ANALYTICS_REPORTING,
                operation="process_request",
                input_mapping={"compliance_data": "compliance_report"},
                output_mapping={"trends": "compliance_trends", "recommendations": "compliance_recommendations"}
            )
        ]
    
    async def execute_workflow(
        self, 
        workflow_type: WorkflowType, 
        input_data: Dict[str, Any], 
        context: AgentContext
    ) -> WorkflowResult:
        """Execute a complete workflow"""
        
        start_time = datetime.now()
        workflow_steps = self.workflows.get(workflow_type, [])
        
        if not workflow_steps:
            return WorkflowResult(
                workflow_type=workflow_type,
                success=False,
                steps_completed=[],
                final_output={},
                errors=[f"Unknown workflow type: {workflow_type}"],
                execution_time=0.0
            )
        
        # Initialize workflow state
        workflow_state = input_data.copy()
        completed_steps = []
        errors = []
        
        # Group steps by parallel execution
        sequential_steps = [step for step in workflow_steps if not step.parallel]
        parallel_steps = [step for step in workflow_steps if step.parallel]
        
        # Execute sequential steps
        for step in sequential_steps:
            try:
                result = await self._execute_step(step, workflow_state, context)
                if result.success:
                    # Update workflow state with step output
                    for output_key, input_key in step.output_mapping.items():
                        if output_key in result.data:
                            workflow_state[input_key] = result.data[output_key]
                    completed_steps.append(step.operation)
                else:
                    if step.required:
                        errors.append(f"Required step {step.operation} failed: {result.message}")
                        break
                    else:
                        errors.append(f"Optional step {step.operation} failed: {result.message}")
                        
            except Exception as e:
                error_msg = f"Step {step.operation} failed with exception: {str(e)}"
                if step.required:
                    errors.append(error_msg)
                    break
                else:
                    errors.append(error_msg)
        
        # Execute parallel steps if sequential steps succeeded
        if not errors or not any(step.required for step in sequential_steps):
            if parallel_steps:
                try:
                    parallel_results = await self._execute_parallel_steps(parallel_steps, workflow_state, context)
                    for step, result in parallel_results.items():
                        if result.success:
                            # Update workflow state with step output
                            step_config = next(s for s in parallel_steps if s.operation == step)
                            for output_key, input_key in step_config.output_mapping.items():
                                if output_key in result.data:
                                    workflow_state[input_key] = result.data[output_key]
                            completed_steps.append(step)
                        else:
                            errors.append(f"Parallel step {step} failed: {result.message}")
                            
                except Exception as e:
                    errors.append(f"Parallel execution failed: {str(e)}")
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Update workflow statistics
        self._update_workflow_stats(workflow_type, execution_time, len(errors) == 0)
        
        return WorkflowResult(
            workflow_type=workflow_type,
            success=len(errors) == 0,
            steps_completed=completed_steps,
            final_output=workflow_state,
            errors=errors,
            execution_time=execution_time
        )
    
    async def _execute_step(
        self, 
        step: WorkflowStep, 
        workflow_state: Dict[str, Any], 
        context: AgentContext
    ) -> AgentResponse:
        """Execute a single workflow step"""
        
        # Prepare input data for the step
        step_input = {}
        for input_key, state_key in step.input_mapping.items():
            if state_key in workflow_state:
                step_input[input_key] = workflow_state[state_key]
            else:
                self.logger.warning(f"Missing input key {state_key} for step {step.operation}")
        
        # Get the agent
        agent = self.agents.get(step.agent_type)
        if not agent:
            raise ValueError(f"Agent {step.agent_type} not found")
        
        # Execute the step
        self.logger.info(f"Executing step {step.operation} with agent {step.agent_type.value}")
        result = await agent.handle_request(context, step_input)
        
        return result
    
    async def _execute_parallel_steps(
        self, 
        steps: List[WorkflowStep], 
        workflow_state: Dict[str, Any], 
        context: AgentContext
    ) -> Dict[str, AgentResponse]:
        """Execute multiple steps in parallel"""
        
        # Create tasks for parallel execution
        tasks = {}
        for step in steps:
            task = asyncio.create_task(
                self._execute_step(step, workflow_state, context)
            )
            tasks[step.operation] = task
        
        # Wait for all tasks to complete
        results = {}
        for step_name, task in tasks.items():
            try:
                result = await task
                results[step_name] = result
            except Exception as e:
                results[step_name] = AgentResponse(
                    success=False,
                    data={},
                    message=f"Parallel step failed: {str(e)}"
                )
        
        return results
    
    def _update_workflow_stats(self, workflow_type: WorkflowType, execution_time: float, success: bool):
        """Update workflow performance statistics"""
        
        if workflow_type.value not in self.workflow_stats:
            self.workflow_stats[workflow_type.value] = {
                "total_executions": 0,
                "successful_executions": 0,
                "total_execution_time": 0.0,
                "average_execution_time": 0.0
            }
        
        stats = self.workflow_stats[workflow_type.value]
        stats["total_executions"] += 1
        stats["total_execution_time"] += execution_time
        stats["average_execution_time"] = stats["total_execution_time"] / stats["total_executions"]
        
        if success:
            stats["successful_executions"] += 1
    
    async def process_employee_conversation(
        self, 
        user_id: str, 
        message: str, 
        session_id: str,
        user_role: str = "employee"
    ) -> Dict[str, Any]:
        """Process an employee conversation through the complete workflow"""
        
        context = AgentContext(
            user_id=user_id,
            session_id=session_id,
            timestamp=datetime.now(),
            metadata={"user_role": user_role, "conversation_type": "employee_chat"}
        )
        
        input_data = {
            "user_message": message,
            "user_role": user_role
        }
        
        result = await self.execute_workflow(
            WorkflowType.EMPLOYEE_CONVERSATION,
            input_data,
            context
        )
        
        return {
            "success": result.success,
            "ai_response": result.final_output.get("ai_response", ""),
            "wellness_suggestions": result.final_output.get("wellness_suggestions", []),
            "resource_recommendations": result.final_output.get("resource_recommendations", []),
            "risk_level": result.final_output.get("risk_assessment", 0.0),
            "sentiment_analysis": result.final_output.get("sentiment_analysis", {}),
            "analytics_insights": result.final_output.get("analytics_insights", {}),
            "errors": result.errors,
            "execution_time": result.execution_time
        }
    
    async def generate_analytics_report(
        self, 
        report_type: str, 
        timeframe: str, 
        filters: Dict[str, Any],
        user_role: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Generate analytics report through the workflow"""
        
        context = AgentContext(
            user_id=user_id,
            session_id=f"analytics_{datetime.now().isoformat()}",
            timestamp=datetime.now(),
            metadata={"user_role": user_role, "report_type": report_type}
        )
        
        input_data = {
            "raw_data": {
                "report_type": report_type,
                "timeframe": timeframe,
                "filters": filters
            },
            "requesting_role": user_role
        }
        
        result = await self.execute_workflow(
            WorkflowType.ANALYTICS_GENERATION,
            input_data,
            context
        )
        
        return {
            "success": result.success,
            "report": result.final_output.get("final_report", {}),
            "errors": result.errors,
            "execution_time": result.execution_time
        }
    
    async def assess_risk(
        self, 
        text_content: str, 
        user_id: str,
        content_type: str = "conversation"
    ) -> Dict[str, Any]:
        """Assess risk through the risk assessment workflow"""
        
        context = AgentContext(
            user_id=user_id,
            session_id=f"risk_assessment_{datetime.now().isoformat()}",
            timestamp=datetime.now(),
            metadata={"content_type": content_type}
        )
        
        input_data = {
            "input_data": {
                "text": text_content,
                "type": content_type
            }
        }
        
        result = await self.execute_workflow(
            WorkflowType.RISK_ASSESSMENT,
            input_data,
            context
        )
        
        return {
            "success": result.success,
            "risk_analysis": result.final_output.get("risk_analysis", {}),
            "risk_level": result.final_output.get("risk_level", 0.0),
            "risk_trends": result.final_output.get("risk_trends", {}),
            "risk_predictions": result.final_output.get("risk_predictions", {}),
            "errors": result.errors,
            "execution_time": result.execution_time
        }
    
    async def recommend_resources(
        self, 
        user_needs: str, 
        user_preferences: Dict[str, Any],
        user_id: str,
        user_role: str = "employee"
    ) -> Dict[str, Any]:
        """Get resource recommendations through the workflow"""
        
        context = AgentContext(
            user_id=user_id,
            session_id=f"resource_recommendation_{datetime.now().isoformat()}",
            timestamp=datetime.now(),
            metadata={"user_role": user_role}
        )
        
        input_data = {
            "user_needs": user_needs,
            "user_preferences": user_preferences
        }
        
        result = await self.execute_workflow(
            WorkflowType.RESOURCE_RECOMMENDATION,
            input_data,
            context
        )
        
        return {
            "success": result.success,
            "resource_recommendations": result.final_output.get("resource_recommendations", []),
            "recommendation_effectiveness": result.final_output.get("recommendation_effectiveness", {}),
            "errors": result.errors,
            "execution_time": result.execution_time
        }
    
    async def audit_compliance(
        self, 
        system_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """Perform compliance audit through the workflow"""
        
        context = AgentContext(
            user_id=user_id,
            session_id=f"compliance_audit_{datetime.now().isoformat()}",
            timestamp=datetime.now(),
            metadata={"audit_type": "system_compliance"}
        )
        
        input_data = {
            "system_data": system_data
        }
        
        result = await self.execute_workflow(
            WorkflowType.COMPLIANCE_AUDIT,
            input_data,
            context
        )
        
        return {
            "success": result.success,
            "compliance_report": result.final_output.get("compliance_report", {}),
            "compliance_trends": result.final_output.get("compliance_trends", {}),
            "compliance_recommendations": result.final_output.get("compliance_recommendations", []),
            "errors": result.errors,
            "execution_time": result.execution_time
        }
    
    def get_agent_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for all agents"""
        
        metrics = {}
        for agent_type, agent in self.agents.items():
            metrics[agent_type.value] = agent.get_metrics()
        
        return metrics
    
    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow performance statistics"""
        
        return {
            "workflow_stats": self.workflow_stats,
            "total_workflows": sum(stats["total_executions"] for stats in self.workflow_stats.values()),
            "success_rate": sum(stats["successful_executions"] for stats in self.workflow_stats.values()) / 
                          sum(stats["total_executions"] for stats in self.workflow_stats.values())
                          if self.workflow_stats else 0.0
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        
        agent_health = {}
        for agent_type, agent in self.agents.items():
            metrics = agent.get_metrics()
            agent_health[agent_type.value] = {
                "status": "healthy" if metrics["success_rate"] > 0.9 else "degraded" if metrics["success_rate"] > 0.7 else "unhealthy",
                "success_rate": metrics["success_rate"],
                "average_response_time": metrics["average_response_time"],
                "error_count": metrics["error_count"]
            }
        
        workflow_health = self.get_workflow_stats()
        
        return {
            "overall_status": "healthy" if all(health["status"] == "healthy" for health in agent_health.values()) else "degraded",
            "agent_health": agent_health,
            "workflow_health": workflow_health,
            "timestamp": datetime.now().isoformat()
        }
