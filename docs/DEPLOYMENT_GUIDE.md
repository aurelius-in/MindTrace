# Enterprise Employee Wellness AI - Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Development Environment](#development-environment)
4. [Staging Environment](#staging-environment)
5. [Production Deployment](#production-deployment)
6. [Cloud Platform Deployments](#cloud-platform-deployments)
7. [Monitoring & Observability](#monitoring--observability)
8. [Security Configuration](#security-configuration)
9. [Backup & Recovery](#backup--recovery)
10. [Troubleshooting](#troubleshooting)

## Overview

This guide covers the complete deployment process for the Enterprise Employee Wellness AI platform across different environments. The platform is designed to be deployed using containerized microservices with support for both Docker Compose (development) and Kubernetes (production).

### Architecture Components

- **Frontend**: React application with Material-UI
- **Backend API**: FastAPI with Python 3.11+
- **Database**: PostgreSQL 14+ with Redis for caching
- **AI Services**: OpenAI/Anthropic API integration
- **Monitoring**: Prometheus + Grafana
- **Message Queue**: Redis/Celery for async tasks
- **Vector Database**: ChromaDB/Pinecone for embeddings
- **Load Balancer**: Nginx/Traefik
- **Security**: Open Policy Agent (OPA) for policy enforcement

## Prerequisites

### System Requirements

#### Development
- Docker Desktop 4.0+
- Docker Compose 2.0+
- 8GB RAM minimum
- 20GB free disk space

#### Production
- Kubernetes 1.24+
- Helm 3.8+
- 16GB RAM minimum per node
- 100GB free disk space per node
- Load balancer (AWS ALB, GCP LB, or Azure LB)

### Required Accounts & APIs

- **OpenAI API Key**: [OpenAI Platform](https://platform.openai.com/)
- **Anthropic API Key**: [Anthropic Console](https://console.anthropic.com/)
- **Pinecone API Key** (optional): [Pinecone Console](https://app.pinecone.io/)
- **Email Service**: SendGrid, AWS SES, or similar
- **Cloud Storage**: AWS S3, GCP Cloud Storage, or Azure Blob Storage

## Development Environment

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/your-org/enterprise-wellness-ai.git
cd enterprise-wellness-ai
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the development environment**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

4. **Initialize the database**
```bash
docker-compose -f docker-compose.dev.yml exec backend python -m scripts.init_db
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Grafana: http://localhost:3001 (admin/admin)

### Development Configuration

#### Environment Variables (.env)
```bash
# Application
APP_NAME=Enterprise Wellness AI
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://wellness_user:wellness_pass@localhost:5432/wellness_db
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-west1-gcp

# Security
SECRET_KEY=your-super-secret-key-for-development-only
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-32-character-encryption-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# External Integrations
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
TEAMS_APP_ID=your-teams-app-id
WORKDAY_CLIENT_ID=your-workday-client-id

# Monitoring
PROMETHEUS_ENDPOINT=http://localhost:9090
GRAFANA_URL=http://localhost:3001

# Privacy & Compliance
OPA_POLICY_URL=http://localhost:8181/v1/data
PRIVACY_MODE=development
```

#### Docker Compose Development
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://wellness_user:wellness_pass@postgres:5432/wellness_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: wellness_db
      POSTGRES_USER: wellness_user
      POSTGRES_PASSWORD: wellness_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

volumes:
  postgres_data:
  redis_data:
  grafana_data:
  prometheus_data:
```

### Development Workflow

1. **Start development environment**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

2. **Run database migrations**
```bash
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
```

3. **Seed development data**
```bash
docker-compose -f docker-compose.dev.yml exec backend python -m scripts.seed_data
```

4. **Run tests**
```bash
docker-compose -f docker-compose.dev.yml exec backend pytest
```

5. **Access development tools**
- API Documentation: http://localhost:8000/docs
- Grafana Dashboards: http://localhost:3001
- Prometheus Metrics: http://localhost:9090

## Staging Environment

### Staging Deployment

1. **Create staging environment**
```bash
# Create staging namespace
kubectl create namespace wellness-staging

# Apply staging configuration
kubectl apply -f k8s/staging/
```

2. **Deploy with Helm**
```bash
helm install wellness-staging ./helm/ \
  --namespace wellness-staging \
  --values helm/values-staging.yaml
```

3. **Verify deployment**
```bash
kubectl get pods -n wellness-staging
kubectl get services -n wellness-staging
```

### Staging Configuration

#### Helm Values (values-staging.yaml)
```yaml
# Staging environment configuration
environment: staging

# Replica counts
frontend:
  replicas: 2
backend:
  replicas: 3

# Resource limits
resources:
  frontend:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  backend:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi"
      cpu: "1000m"

# Database
database:
  host: staging-postgres
  name: wellness_staging
  user: wellness_user
  password: staging_password

# Redis
redis:
  host: staging-redis
  port: 6379

# Monitoring
monitoring:
  enabled: true
  grafana:
    adminPassword: staging-admin-pass

# Security
security:
  jwtSecret: staging-jwt-secret
  encryptionKey: staging-32-char-encryption-key

# External services
external:
  openaiApiKey: ${OPENAI_API_KEY}
  anthropicApiKey: ${ANTHROPIC_API_KEY}
```

## Production Deployment

### Production Architecture

```
Internet
    ↓
Load Balancer (AWS ALB / GCP LB / Azure LB)
    ↓
Ingress Controller (Nginx / Traefik)
    ↓
Frontend (React) → Backend API (FastAPI)
    ↓
Database (PostgreSQL) + Cache (Redis)
    ↓
Monitoring (Prometheus + Grafana)
```

### Production Deployment Steps

1. **Prepare production environment**
```bash
# Create production namespace
kubectl create namespace wellness-production

# Create secrets
kubectl create secret generic wellness-secrets \
  --namespace wellness-production \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  --from-literal=anthropic-api-key=$ANTHROPIC_API_KEY \
  --from-literal=jwt-secret=$JWT_SECRET \
  --from-literal=encryption-key=$ENCRYPTION_KEY
```

2. **Deploy with Helm**
```bash
helm install wellness-production ./helm/ \
  --namespace wellness-production \
  --values helm/values-production.yaml
```

3. **Configure ingress and SSL**
```bash
# Apply ingress configuration
kubectl apply -f k8s/production/ingress.yaml

# Configure SSL certificate
kubectl apply -f k8s/production/cert-manager.yaml
```

4. **Verify production deployment**
```bash
kubectl get pods -n wellness-production
kubectl get services -n wellness-production
kubectl get ingress -n wellness-production
```

### Production Configuration

#### Helm Values (values-production.yaml)
```yaml
# Production environment configuration
environment: production

# High availability configuration
frontend:
  replicas: 3
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

backend:
  replicas: 5
  autoscaling:
    enabled: true
    minReplicas: 5
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70

# Resource allocation
resources:
  frontend:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi"
      cpu: "1000m"
  backend:
    requests:
      memory: "1Gi"
      cpu: "1000m"
    limits:
      memory: "2Gi"
      cpu: "2000m"

# Database configuration
database:
  host: production-postgres
  name: wellness_production
  user: wellness_user
  password: ${DB_PASSWORD}
  poolSize: 20
  maxConnections: 100

# Redis configuration
redis:
  host: production-redis
  port: 6379
  password: ${REDIS_PASSWORD}
  cluster:
    enabled: true
    replicas: 3

# Monitoring and observability
monitoring:
  enabled: true
  prometheus:
    retention: 30d
    storage: 100Gi
  grafana:
    adminPassword: ${GRAFANA_PASSWORD}
    persistence:
      enabled: true
      size: 10Gi

# Security configuration
security:
  jwtSecret: ${JWT_SECRET}
  encryptionKey: ${ENCRYPTION_KEY}
  corsOrigins:
    - "https://wellness.yourcompany.com"
    - "https://admin.wellness.yourcompany.com"

# External integrations
external:
  openaiApiKey: ${OPENAI_API_KEY}
  anthropicApiKey: ${ANTHROPIC_API_KEY}
  pineconeApiKey: ${PINECONE_API_KEY}
  pineconeEnvironment: ${PINECONE_ENVIRONMENT}

# Backup configuration
backup:
  enabled: true
  schedule: "0 2 * * *"  # Daily at 2 AM
  retention: 30
  storage:
    type: s3
    bucket: wellness-backups
    region: us-west-2
```

## Cloud Platform Deployments

### AWS EKS Deployment

1. **Create EKS cluster**
```bash
eksctl create cluster \
  --name wellness-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 10 \
  --managed
```

2. **Configure AWS Load Balancer Controller**
```bash
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=wellness-cluster
```

3. **Deploy application**
```bash
helm install wellness-production ./helm/ \
  --namespace wellness-production \
  --values helm/values-aws-production.yaml
```

### Google Cloud GKE Deployment

1. **Create GKE cluster**
```bash
gcloud container clusters create wellness-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 10 \
  --machine-type e2-standard-2
```

2. **Configure Google Cloud Load Balancer**
```bash
kubectl apply -f k8s/gcp/load-balancer.yaml
```

3. **Deploy application**
```bash
helm install wellness-production ./helm/ \
  --namespace wellness-production \
  --values helm/values-gcp-production.yaml
```

### Azure AKS Deployment

1. **Create AKS cluster**
```bash
az aks create \
  --resource-group wellness-rg \
  --name wellness-cluster \
  --node-count 3 \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 10 \
  --node-vm-size Standard_D2s_v3
```

2. **Configure Azure Application Gateway**
```bash
kubectl apply -f k8s/azure/application-gateway.yaml
```

3. **Deploy application**
```bash
helm install wellness-production ./helm/ \
  --namespace wellness-production \
  --values helm/values-azure-production.yaml
```

## Monitoring & Observability

### Prometheus Configuration

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'wellness-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'wellness-frontend'
    static_configs:
      - targets: ['frontend:3000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Grafana Dashboards

#### System Health Dashboard
- CPU and Memory usage
- Network I/O
- Disk usage
- Pod status and restarts

#### Application Metrics Dashboard
- API response times
- Error rates
- Request volume
- User engagement metrics

#### Business Metrics Dashboard
- Wellness check-ins
- Risk assessments
- User satisfaction scores
- Resource utilization

### Alerting Configuration

```yaml
# monitoring/alert_rules.yml
groups:
  - name: wellness-alerts
    rules:
      - alert: HighCPUUsage
        expr: container_cpu_usage_seconds_total > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "Container {{ $labels.container }} has high CPU usage"

      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Container {{ $labels.container }} has high memory usage"

      - alert: APIDown
        expr: up{job="wellness-backend"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Backend API is down"
          description: "The wellness backend API is not responding"
```

## Security Configuration

### Network Security

```yaml
# k8s/security/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: wellness-network-policy
  namespace: wellness-production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
  - to:
    - namespaceSelector:
        matchLabels:
          name: monitoring
```

### Pod Security Standards

```yaml
# k8s/security/pod-security.yaml
apiVersion: v1
kind: PodSecurityPolicy
metadata:
  name: wellness-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  readOnlyRootFilesystem: true
```

### Secrets Management

```bash
# Create secrets
kubectl create secret generic wellness-db-secret \
  --from-literal=username=wellness_user \
  --from-literal=password=$(openssl rand -base64 32) \
  --namespace wellness-production

kubectl create secret generic wellness-api-secrets \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  --from-literal=anthropic-api-key=$ANTHROPIC_API_KEY \
  --from-literal=jwt-secret=$(openssl rand -base64 64) \
  --namespace wellness-production
```

## Backup & Recovery

### Database Backup

```yaml
# k8s/backup/backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: wellness-db-backup
  namespace: wellness-production
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:14-alpine
            command:
            - /bin/sh
            - -c
            - |
              pg_dump $DATABASE_URL | gzip > /backup/wellness-$(date +%Y%m%d-%H%M%S).sql.gz
              aws s3 cp /backup/* s3://wellness-backups/database/
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: wellness-db-secret
                  key: database-url
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access-key-id
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret-access-key
          volumes:
          - name: backup-volume
            emptyDir: {}
          restartPolicy: OnFailure
```

### Disaster Recovery

1. **Database Recovery**
```bash
# Restore from backup
kubectl exec -it postgres-0 -- pg_restore \
  -d wellness_production \
  /backup/wellness-20240125-020000.sql.gz
```

2. **Application Recovery**
```bash
# Redeploy application
helm upgrade wellness-production ./helm/ \
  --namespace wellness-production \
  --values helm/values-production.yaml
```

3. **Data Validation**
```bash
# Verify data integrity
kubectl exec -it backend-0 -- python -m scripts.validate_data
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connectivity
kubectl exec -it backend-0 -- python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
print('Database connection successful')
conn.close()
"
```

#### Redis Connection Issues
```bash
# Check Redis connectivity
kubectl exec -it backend-0 -- python -c "
import redis
r = redis.Redis.from_url('$REDIS_URL')
print('Redis connection successful')
print(r.ping())
"
```

#### AI Service Issues
```bash
# Test AI service connectivity
kubectl exec -it backend-0 -- python -c "
import openai
openai.api_key = '$OPENAI_API_KEY'
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print('AI service connection successful')
"
```

### Log Analysis

```bash
# View application logs
kubectl logs -f deployment/wellness-backend -n wellness-production

# View specific pod logs
kubectl logs -f pod/wellness-backend-abc123 -n wellness-production

# View logs with timestamps
kubectl logs --timestamps deployment/wellness-backend -n wellness-production
```

### Performance Monitoring

```bash
# Check resource usage
kubectl top pods -n wellness-production

# Check node resource usage
kubectl top nodes

# Monitor API performance
curl -H "Authorization: Bearer $TOKEN" \
  https://api.wellness.yourcompany.com/health
```

### Health Checks

```bash
# Application health check
curl https://api.wellness.yourcompany.com/health

# Database health check
curl https://api.wellness.yourcompany.com/health/db

# AI services health check
curl https://api.wellness.yourcompany.com/health/ai
```

## Support

For deployment support:
- **Documentation**: [docs.enterprise-wellness.ai](https://docs.enterprise-wellness.ai)
- **GitHub Issues**: [github.com/your-org/enterprise-wellness-ai/issues](https://github.com/your-org/enterprise-wellness-ai/issues)
- **Support Email**: deployment-support@enterprise-wellness.ai
- **Slack Channel**: #wellness-deployment
