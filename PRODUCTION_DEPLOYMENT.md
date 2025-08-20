# Production Deployment Guide

This guide provides comprehensive instructions for deploying the Enterprise Employee Wellness AI platform to production environments.

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Docker & Docker Compose**
- **Kubernetes** (for K8s deployment)
- **PostgreSQL 13+**
- **Redis 6+**
- **OpenAI API Key**
- **Anthropic API Key**

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/aurelius-in/MindTrace.git
cd MindTrace

# Copy environment template
cp env.example .env

# Generate secure keys
python -c "from config.production import generate_secure_keys; print(generate_secure_keys())"
```

### 2. Configure Environment Variables

Edit `.env` file with your production values:

```bash
# Required - Security
SECRET_KEY=your-32-character-secret-key
ENCRYPTION_KEY=your-32-character-encryption-key

# Required - Database
DATABASE_URL=postgresql://user:password@host:5432/wellness_db
REDIS_URL=redis://host:6379/0
VECTOR_DB_URL=your-vector-db-connection-string

# Required - AI Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Required - Email
SMTP_HOST=your-smtp-host
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-smtp-password
FROM_EMAIL=noreply@yourcompany.com

# Required - CORS
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]

# Optional - Enterprise Integrations
SLACK_BOT_TOKEN=your-slack-bot-token
TEAMS_APP_ID=your-teams-app-id
```

### 3. Deploy

#### Option A: Docker Compose (Recommended for small-medium deployments)

```bash
# Run deployment script
python scripts/deploy_production.py --method docker-compose

# Or manually
docker-compose up -d
```

#### Option B: Kubernetes (Recommended for large-scale deployments)

```bash
# Deploy to Kubernetes
python scripts/deploy_production.py --method kubernetes

# Or manually
kubectl apply -f k8s/
```

## 🔒 Security Configuration

### 1. Network Security

```bash
# Configure firewall rules
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 22/tcp   # SSH
sudo ufw enable
```

### 2. SSL/TLS Configuration

```bash
# Install Certbot
sudo apt install certbot

# Generate SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure Nginx with SSL
sudo cp nginx/ssl.conf /etc/nginx/sites-available/wellness-ai
sudo ln -s /etc/nginx/sites-available/wellness-ai /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 3. Database Security

```sql
-- Create dedicated database user
CREATE USER wellness_user WITH PASSWORD 'strong-password';
GRANT CONNECT ON DATABASE wellness_db TO wellness_user;
GRANT USAGE ON SCHEMA public TO wellness_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO wellness_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO wellness_user;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/path/to/server.crt';
ALTER SYSTEM SET ssl_key_file = '/path/to/server.key';
```

## 📊 Monitoring & Observability

### 1. Prometheus & Grafana Setup

```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
# URL: http://yourdomain.com:3000
# Default credentials: admin/admin
```

### 2. Log Aggregation

```bash
# Configure log forwarding to ELK stack
docker-compose -f docker-compose.logging.yml up -d
```

### 3. Health Checks

```bash
# Check system health
curl https://yourdomain.com/health

# Check database connectivity
curl https://yourdomain.com/health/database

# Check external services
curl https://yourdomain.com/health/external
```

## 🔄 Backup & Recovery

### 1. Automated Backups

```bash
# Configure backup schedule
crontab -e

# Add backup job (daily at 2 AM)
0 2 * * * /path/to/MindTrace/scripts/backup.sh
```

### 2. Manual Backup

```bash
# Create backup
python scripts/backup.py --type full

# Restore from backup
python scripts/restore.py --backup-id backup_1234567890
```

## 🚨 Incident Response

### 1. Rollback Procedure

```bash
# Rollback deployment
python scripts/deploy_production.py --rollback

# Check rollback status
docker-compose ps
```

### 2. Emergency Contacts

- **System Administrator**: admin@yourcompany.com
- **DevOps Team**: devops@yourcompany.com
- **Security Team**: security@yourcompany.com

## 📈 Performance Optimization

### 1. Database Optimization

```sql
-- Create indexes for performance
CREATE INDEX idx_wellness_entries_user_timestamp ON wellness_entries(user_id, timestamp);
CREATE INDEX idx_analytics_metrics_timestamp ON analytics_metrics(timestamp);
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
```

### 2. Caching Configuration

```bash
# Configure Redis caching
redis-cli CONFIG SET maxmemory 2gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### 3. Load Balancing

```nginx
# Nginx load balancer configuration
upstream wellness_backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://wellness_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔐 Compliance & Privacy

### 1. GDPR Compliance

```bash
# Enable data anonymization
export ENABLE_PRIVACY_CONTROLS=true
export ANONYMIZE_DATA=true

# Configure data retention
export DATA_RETENTION_DAYS=365
```

### 2. HIPAA Compliance

```bash
# Enable encryption at rest
export ENCRYPTION_ENABLED=true

# Configure audit logging
export AUDIT_LOGGING_ENABLED=true
```

### 3. SOC2 Compliance

```bash
# Enable security monitoring
export SECURITY_MONITORING_ENABLED=true

# Configure access controls
export ACCESS_CONTROL_ENABLED=true
```

## 🧪 Testing

### 1. Load Testing

```bash
# Run load tests
python scripts/load_test.py --users 100 --duration 300

# Monitor performance
python scripts/monitor_performance.py
```

### 2. Security Testing

```bash
# Run security scan
python scripts/security_scan.py

# Check for vulnerabilities
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy image mindtrace-backend:latest
```

### 3. Integration Testing

```bash
# Run integration tests
pytest tests/integration/ -v

# Run API tests
pytest tests/api/ -v
```

## 📋 Maintenance

### 1. Regular Maintenance Tasks

```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Clean up old logs
python scripts/cleanup_logs.py --days 30

# Optimize database
python scripts/optimize_database.py
```

### 2. Monitoring Alerts

Configure alerts for:
- CPU usage > 80%
- Memory usage > 85%
- Disk usage > 90%
- Database connections > 80%
- API response time > 2s
- Error rate > 5%

### 3. Health Checks

```bash
# Automated health checks
crontab -e

# Add health check job (every 5 minutes)
*/5 * * * * curl -f https://yourdomain.com/health || echo "Health check failed"
```

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database connectivity
   docker-compose exec backend python -c "from database.connection import check_db_connection; print(check_db_connection())"
   ```

2. **Redis Connection Issues**
   ```bash
   # Check Redis connectivity
   docker-compose exec redis redis-cli ping
   ```

3. **API Timeout Issues**
   ```bash
   # Check API response times
   curl -w "@curl-format.txt" -o /dev/null -s https://yourdomain.com/health
   ```

4. **Memory Issues**
   ```bash
   # Check memory usage
   docker stats
   ```

### Log Analysis

```bash
# View application logs
docker-compose logs -f backend

# View error logs
docker-compose logs backend | grep ERROR

# Analyze log patterns
python scripts/analyze_logs.py
```

## 📞 Support

### Getting Help

1. **Documentation**: Check the `/docs` directory
2. **Issues**: Create an issue on GitHub
3. **Email**: support@yourcompany.com
4. **Slack**: #wellness-ai-support

### Escalation Process

1. **Level 1**: System Administrator
2. **Level 2**: DevOps Team
3. **Level 3**: Development Team
4. **Level 4**: Security Team

## 🔄 Updates & Upgrades

### 1. Application Updates

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python -m database.migrations

# Restart services
docker-compose restart
```

### 2. Database Migrations

```bash
# Run migrations
python -m database.migrations

# Verify migration status
python -m database.migrations --status
```

### 3. Configuration Updates

```bash
# Update configuration
python scripts/update_config.py

# Validate configuration
python config/production.py
```

## 📊 Performance Metrics

### Key Performance Indicators (KPIs)

- **Response Time**: < 200ms (95th percentile)
- **Availability**: > 99.9%
- **Error Rate**: < 0.1%
- **Throughput**: > 1000 requests/second
- **User Satisfaction**: > 4.5/5

### Monitoring Dashboard

Access the monitoring dashboard at:
- **Grafana**: http://yourdomain.com:3000
- **Prometheus**: http://yourdomain.com:9090
- **Kibana**: http://yourdomain.com:5601

## 🎯 Best Practices

1. **Security First**: Always prioritize security over convenience
2. **Automation**: Automate repetitive tasks
3. **Monitoring**: Monitor everything
4. **Backup**: Regular backups are essential
5. **Documentation**: Keep documentation updated
6. **Testing**: Test everything before production
7. **Rollback Plan**: Always have a rollback plan
8. **Incident Response**: Have clear incident response procedures

---

**⚠️ Important**: This is a production deployment guide. Always test in a staging environment first and ensure you have proper backup and rollback procedures in place before deploying to production.
