# Enterprise Employee Wellness AI - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Enterprise Employee Wellness AI platform. The system is designed as a multi-agent AI platform that provides employee wellness support, organizational health monitoring, and privacy-compliant analytics.

## Architecture Overview

### Agent System
The platform consists of five specialized AI agents:

1. **Wellness Companion Agent** - Direct employee interaction and support
2. **Resource Recommendation Agent** - EAP and wellness resource matching
3. **Sentiment & Risk Detection Agent** - Burnout and stress pattern analysis
4. **Analytics & Reporting Agent** - HR dashboards and organizational insights
5. **Policy & Privacy Agent** - Data anonymization and compliance enforcement

### Technology Stack
- **Backend**: FastAPI, LangChain, PostgreSQL, Redis, ChromaDB
- **Frontend**: React, TypeScript, Material-UI
- **Monitoring**: Prometheus, Grafana, ELK Stack
- **Security**: OPA, JWT, Encryption
- **Deployment**: Docker, Kubernetes

## Prerequisites

### System Requirements
- Docker & Docker Compose
- Kubernetes cluster (for production)
- PostgreSQL 14+
- Redis 6+
- 8GB+ RAM
- 4+ CPU cores

### External Dependencies
- OpenAI API key
- Anthropic API key (optional)
- Slack/Teams integration tokens
- HRIS system credentials

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd enterprise-wellness-ai
cp env.example .env
```

### 2. Configure Environment
Edit `.env` file with your configuration:
```bash
# Required: AI Services
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Required: Security
SECRET_KEY=your_long_random_secret_key
ENCRYPTION_KEY=your_long_random_encryption_key

# Optional: Enterprise Integrations
SLACK_BOT_TOKEN=xoxb-your-slack-token
TEAMS_APP_ID=your-teams-app-id
```

### 3. Deploy with Docker Compose
```bash
# Make deployment script executable
chmod +x scripts/deploy.sh

# Deploy the platform
./scripts/deploy.sh deploy
```

### 4. Access the Application
- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Grafana Dashboard**: http://localhost:3000
- **Prometheus Metrics**: http://localhost:9090

## Production Deployment

### Kubernetes Deployment

1. **Prepare Kubernetes Cluster**
```bash
# Ensure kubectl is configured
kubectl cluster-info

# Create namespace
kubectl apply -f k8s/namespace.yaml
```

2. **Configure Secrets**
```bash
# Update k8s/secret.yaml with base64 encoded values
# Deploy secrets
kubectl apply -f k8s/secret.yaml
```

3. **Deploy Infrastructure**
```bash
# Deploy databases
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/chromadb-deployment.yaml

# Deploy monitoring
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/grafana-deployment.yaml
kubectl apply -f k8s/opa-deployment.yaml
```

4. **Deploy Application**
```bash
# Deploy main application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

5. **Verify Deployment**
```bash
kubectl get pods -n wellness-ai
kubectl get services -n wellness-ai
```

### Using Helm (Alternative)

```bash
# Install Helm chart
helm install wellness-ai ./helm/

# Upgrade deployment
helm upgrade wellness-ai ./helm/

# Uninstall
helm uninstall wellness-ai
```

## Configuration

### Agent Configuration

Each agent can be configured independently through environment variables:

```bash
# Wellness Companion Agent
WELLNESS_COMPANION_MODEL=gpt-4
WELLNESS_MEMORY_TYPE=episodic
WELLNESS_RISK_THRESHOLD=0.7

# Resource Recommendation Agent
RESOURCE_VECTOR_DB=chromadb
RESOURCE_EMBEDDING_MODEL=text-embedding-ada-002

# Sentiment Analysis Agent
SENTIMENT_MODELS=vader,roberta
RISK_INDICATORS=burnout,stress_spike,toxic_patterns

# Analytics Agent
ANALYTICS_AGGREGATION_WINDOW=7d
ANALYTICS_RETENTION_DAYS=365

# Privacy Agent
DP_EPSILON=1.0
ANONYMIZATION_ENABLED=true
```

### Database Configuration

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis
REDIS_URL=redis://host:6379

# ChromaDB
VECTOR_DB_URL=chromadb://host:8000
```

### Monitoring Configuration

```bash
# Prometheus
PROMETHEUS_ENDPOINT=http://prometheus:9090

# Grafana
GRAFANA_URL=http://grafana:3000

# Open Policy Agent
OPA_POLICY_URL=http://opa:8181
```

## Security Configuration

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Employee, Manager, HR, Executive)
- OAuth2 integration for enterprise SSO

### Data Privacy
- End-to-end encryption
- Differential privacy for analytics
- Automatic PII detection and anonymization
- GDPR/HIPAA compliance features

### Network Security
- TLS/SSL encryption
- API rate limiting
- CORS configuration
- Network policies (Kubernetes)

## Monitoring & Observability

### Metrics Collection
- Application performance metrics
- Agent response times and success rates
- User engagement analytics
- System resource utilization

### Logging
- Structured JSON logging
- Centralized log aggregation (ELK Stack)
- Audit trail for compliance

### Alerting
- Prometheus alerting rules
- Slack/Teams notifications
- Email alerts for critical issues

## Integration Setup

### Slack Integration
1. Create Slack app at https://api.slack.com/apps
2. Configure bot token and signing secret
3. Set up event subscriptions and slash commands
4. Deploy to workspace

### Teams Integration
1. Register app in Azure AD
2. Configure bot framework
3. Set up messaging endpoints
4. Deploy to Teams

### HRIS Integration
1. Configure Workday/BambooHR API credentials
2. Set up data synchronization
3. Configure privacy policies
4. Test data flow

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
```bash
# Check database status
docker-compose ps postgres
kubectl get pods -l app=wellness-postgres

# Check logs
docker-compose logs postgres
kubectl logs -l app=wellness-postgres
```

2. **Agent Initialization Failures**
```bash
# Check agent logs
docker-compose logs wellness-ai
kubectl logs -l app=wellness-ai-backend

# Verify API keys
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

3. **Memory Issues**
```bash
# Check resource usage
docker stats
kubectl top pods -n wellness-ai

# Adjust resource limits in deployment configs
```

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Agent health
curl http://localhost:8000/api/v1/metrics

# Database health
docker-compose exec postgres pg_isready
```

### Performance Tuning

1. **Resource Allocation**
   - Adjust CPU/memory limits based on usage
   - Scale horizontally for high traffic
   - Optimize database queries

2. **Caching Strategy**
   - Redis for session data
   - Vector database for embeddings
   - CDN for static assets

3. **Monitoring Optimization**
   - Set appropriate scrape intervals
   - Configure retention policies
   - Optimize alerting rules

## Maintenance

### Backup Procedures
```bash
# Database backup
docker-compose exec postgres pg_dump -U wellness_user wellness_db > backup.sql

# Configuration backup
tar -czf config-backup.tar.gz .env k8s/ monitoring/

# Data backup
tar -czf data-backup.tar.gz data/ logs/
```

### Update Procedures
```bash
# Update application
git pull origin main
docker-compose build
docker-compose up -d

# Update Kubernetes deployment
kubectl set image deployment/wellness-ai-backend wellness-ai=new-image:tag
```

### Scaling
```bash
# Scale Docker Compose
docker-compose up -d --scale wellness-ai=3

# Scale Kubernetes
kubectl scale deployment wellness-ai-backend --replicas=5
```

## Compliance & Auditing

### Data Retention
- Conversation logs: 90 days
- Analytics data: 365 days
- Audit logs: 7 years
- User profiles: 365 days

### Privacy Controls
- Automatic PII detection
- Data anonymization
- Consent management
- Right to erasure

### Audit Trail
- All data access logged
- Policy enforcement tracked
- Compliance reports generated
- Regular security assessments

## Support & Documentation

### API Documentation
- Interactive API docs: `/docs`
- OpenAPI specification: `/openapi.json`
- Postman collection available

### Monitoring Dashboards
- Grafana dashboards for metrics
- Kibana for log analysis
- Custom HR analytics dashboards

### Support Channels
- Technical documentation: `/docs`
- Health monitoring: `/health`
- Metrics endpoint: `/api/v1/metrics`
- Log aggregation: ELK Stack

## License & Legal

This platform is designed for enterprise use with:
- HIPAA compliance features
- GDPR compliance tools
- SOC2 readiness
- Enterprise security standards

Ensure proper legal review before production deployment.

---

For additional support, refer to the main README.md or contact the development team.
