"""
Enterprise Employee Wellness AI - FastAPI Backend
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging
import time
import uuid
from datetime import datetime
import asyncio

from config.settings import settings
from agents.orchestrator import AgentOrchestrator
from monitoring.metrics import MetricsCollector
from integrations.slack import SlackIntegration
from integrations.teams import TeamsIntegration
from database.connection import get_database
from security.auth import verify_token, get_current_user
from privacy.anonymizer import DataAnonymizer

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.monitoring.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise Employee Wellness AI Platform",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

# Security
security = HTTPBearer()

# Initialize core components
orchestrator = None
metrics_collector = None
slack_integration = None
teams_integration = None
data_anonymizer = None

# Pydantic models
class ConversationRequest(BaseModel):
    message: str = Field(..., description="User message")
    user_role: str = Field("employee", description="User role")
    session_id: Optional[str] = Field(None, description="Session ID")

class AnalyticsRequest(BaseModel):
    report_type: str = Field(..., description="Type of report to generate")
    timeframe: str = Field("30d", description="Timeframe for analysis")
    filters: Dict[str, Any] = Field({}, description="Additional filters")
    user_role: str = Field(..., description="User role requesting report")

class ResourceRequest(BaseModel):
    needs: str = Field(..., description="User needs description")
    preferences: Dict[str, Any] = Field({}, description="User preferences")
    user_role: str = Field("employee", description="User role")

class RiskAssessmentRequest(BaseModel):
    text_content: str = Field(..., description="Text content to assess")
    content_type: str = Field("conversation", description="Type of content")

class ComplianceAuditRequest(BaseModel):
    system_data: Dict[str, Any] = Field(..., description="System data to audit")

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup"""
    global orchestrator, metrics_collector, slack_integration, teams_integration, data_anonymizer
    
    logger.info("Starting Enterprise Employee Wellness AI Platform")
    
    try:
        # Initialize agent orchestrator
        orchestrator = AgentOrchestrator()
        logger.info("Agent orchestrator initialized")
        
        # Initialize metrics collector
        metrics_collector = MetricsCollector()
        logger.info("Metrics collector initialized")
        
        # Initialize integrations
        if settings.integrations.slack_bot_token:
            slack_integration = SlackIntegration()
            logger.info("Slack integration initialized")
        
        if settings.integrations.teams_app_id:
            teams_integration = TeamsIntegration()
            logger.info("Teams integration initialized")
        
        # Initialize data anonymizer
        data_anonymizer = DataAnonymizer()
        logger.info("Data anonymizer initialized")
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Enterprise Employee Wellness AI Platform")
    
    # Cleanup connections and resources
    if metrics_collector:
        await metrics_collector.cleanup()

# Middleware for request logging and metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and collect metrics"""
    start_time = time.time()
    
    # Generate request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Log request
    logger.info(f"Request {request_id}: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    # Collect metrics
    if metrics_collector:
        await metrics_collector.record_request_metrics(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=process_time
        )
    
    # Log response
    logger.info(f"Request {request_id} completed: {response.status_code} in {process_time:.3f}s")
    
    return response

# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    components = {}
    
    # Check agent orchestrator
    if orchestrator:
        health = orchestrator.get_system_health()
        components["agent_orchestrator"] = health["overall_status"]
    else:
        components["agent_orchestrator"] = "unavailable"
    
    # Check database
    try:
        db = await get_database()
        await db.execute("SELECT 1")
        components["database"] = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        components["database"] = "unhealthy"
    
    # Check integrations
    components["slack_integration"] = "healthy" if slack_integration else "not_configured"
    components["teams_integration"] = "healthy" if teams_integration else "not_configured"
    
    # Determine overall status
    overall_status = "healthy" if all(
        status in ["healthy", "not_configured"] for status in components.values()
    ) else "degraded"
    
    return HealthCheckResponse(
        status=overall_status,
        timestamp=datetime.now().isoformat(),
        version=settings.app_version,
        components=components
    )

# Employee conversation endpoint
@app.post("/api/v1/conversation")
async def process_conversation(
    request: ConversationRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Process employee conversation through the agent workflow"""
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process conversation through orchestrator
        result = await orchestrator.process_employee_conversation(
            user_id=current_user["user_id"],
            message=request.message,
            session_id=session_id,
            user_role=request.user_role
        )
        
        # Add analytics to background tasks
        background_tasks.add_task(
            orchestrator.generate_analytics_report,
            "conversation_analytics",
            "1d",
            {"session_id": session_id},
            request.user_role,
            current_user["user_id"]
        )
        
        return {
            "success": result["success"],
            "session_id": session_id,
            "response": result["ai_response"],
            "suggestions": result["wellness_suggestions"],
            "resources": result["resource_recommendations"],
            "risk_level": result["risk_level"],
            "sentiment": result["sentiment_analysis"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Conversation processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoint
@app.post("/api/v1/analytics")
async def generate_analytics(
    request: AnalyticsRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate analytics reports"""
    
    try:
        result = await orchestrator.generate_analytics_report(
            report_type=request.report_type,
            timeframe=request.timeframe,
            filters=request.filters,
            user_role=request.user_role,
            user_id=current_user["user_id"]
        )
        
        return {
            "success": result["success"],
            "report": result["report"],
            "generated_at": datetime.now().isoformat(),
            "execution_time": result["execution_time"]
        }
        
    except Exception as e:
        logger.error(f"Analytics generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Resource recommendation endpoint
@app.post("/api/v1/resources")
async def recommend_resources(
    request: ResourceRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get resource recommendations"""
    
    try:
        result = await orchestrator.recommend_resources(
            user_needs=request.needs,
            user_preferences=request.preferences,
            user_id=current_user["user_id"],
            user_role=request.user_role
        )
        
        return {
            "success": result["success"],
            "recommendations": result["resource_recommendations"],
            "effectiveness": result["recommendation_effectiveness"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Resource recommendation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Risk assessment endpoint
@app.post("/api/v1/risk-assessment")
async def assess_risk(
    request: RiskAssessmentRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Assess risk in text content"""
    
    try:
        result = await orchestrator.assess_risk(
            text_content=request.text_content,
            user_id=current_user["user_id"],
            content_type=request.content_type
        )
        
        return {
            "success": result["success"],
            "risk_analysis": result["risk_analysis"],
            "risk_level": result["risk_level"],
            "trends": result["risk_trends"],
            "predictions": result["risk_predictions"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Compliance audit endpoint
@app.post("/api/v1/compliance/audit")
async def audit_compliance(
    request: ComplianceAuditRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Perform compliance audit"""
    
    try:
        result = await orchestrator.audit_compliance(
            system_data=request.system_data,
            user_id=current_user["user_id"]
        )
        
        return {
            "success": result["success"],
            "compliance_report": result["compliance_report"],
            "trends": result["compliance_trends"],
            "recommendations": result["compliance_recommendations"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Compliance audit failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# System metrics endpoint
@app.get("/api/v1/metrics")
async def get_metrics(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get system metrics and performance data"""
    
    try:
        # Get agent metrics
        agent_metrics = orchestrator.get_agent_metrics()
        
        # Get workflow statistics
        workflow_stats = orchestrator.get_workflow_stats()
        
        # Get system health
        system_health = orchestrator.get_system_health()
        
        # Get application metrics
        app_metrics = await metrics_collector.get_application_metrics()
        
        return {
            "agent_metrics": agent_metrics,
            "workflow_stats": workflow_stats,
            "system_health": system_health,
            "application_metrics": app_metrics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Slack integration endpoints
@app.post("/api/v1/integrations/slack/events")
async def slack_events(request: Request):
    """Handle Slack events"""
    
    if not slack_integration:
        raise HTTPException(status_code=501, detail="Slack integration not configured")
    
    try:
        body = await request.body()
        result = await slack_integration.handle_event(body, request.headers)
        return result
        
    except Exception as e:
        logger.error(f"Slack event handling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/integrations/slack/commands")
async def slack_commands(request: Request):
    """Handle Slack slash commands"""
    
    if not slack_integration:
        raise HTTPException(status_code=501, detail="Slack integration not configured")
    
    try:
        form_data = await request.form()
        result = await slack_integration.handle_command(form_data)
        return result
        
    except Exception as e:
        logger.error(f"Slack command handling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Teams integration endpoints
@app.post("/api/v1/integrations/teams/messages")
async def teams_messages(request: Request):
    """Handle Teams messages"""
    
    if not teams_integration:
        raise HTTPException(status_code=501, detail="Teams integration not configured")
    
    try:
        body = await request.json()
        result = await teams_integration.handle_message(body)
        return result
        
    except Exception as e:
        logger.error(f"Teams message handling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Privacy and compliance endpoints
@app.post("/api/v1/privacy/anonymize")
async def anonymize_data(
    data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Anonymize data for privacy compliance"""
    
    try:
        anonymized_data = await data_anonymizer.anonymize(data)
        
        return {
            "success": True,
            "anonymized_data": anonymized_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Data anonymization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/privacy/audit-log")
async def get_audit_log(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get privacy audit log"""
    
    try:
        # Get audit log from privacy agent
        privacy_agent = orchestrator.agents.get("policy_privacy")
        if not privacy_agent:
            raise HTTPException(status_code=501, detail="Privacy agent not available")
        
        audit_log = privacy_agent.get_audit_log(start_date, end_date)
        
        return {
            "success": True,
            "audit_log": audit_log,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Audit log retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(request.state, "request_id", "unknown")
        }
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Enterprise Employee Wellness AI Platform",
        "docs": "/docs" if settings.debug else None,
        "health": "/health",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.monitoring.log_level.lower()
    )
