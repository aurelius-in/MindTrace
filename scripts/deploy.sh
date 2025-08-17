#!/bin/bash

# Enterprise Employee Wellness AI - Deployment Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="enterprise-wellness-ai"
NAMESPACE="wellness-ai"
DOCKER_REGISTRY="your-registry.com"
IMAGE_TAG="latest"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if kubectl is installed (for Kubernetes deployment)
    if ! command -v kubectl &> /dev/null; then
        log_warning "kubectl is not installed. Kubernetes deployment will be skipped."
    fi
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        log_error ".env file not found. Please copy env.example to .env and configure it."
        exit 1
    fi
    
    log_success "Prerequisites check completed."
}

setup_environment() {
    log_info "Setting up environment..."
    
    # Create necessary directories
    mkdir -p data/chromadb logs certs monitoring/grafana/dashboards monitoring/grafana/datasources policies nginx/ssl
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        cp env.example .env
        log_warning "Please edit .env file with your configuration before continuing."
        exit 1
    fi
    
    # Load environment variables
    source .env
    
    log_success "Environment setup completed."
}

build_images() {
    log_info "Building Docker images..."
    
    # Build main application image
    docker build -t ${DOCKER_REGISTRY}/${PROJECT_NAME}:${IMAGE_TAG} .
    
    # Build frontend image if it exists
    if [ -d "frontend" ]; then
        docker build -t ${DOCKER_REGISTRY}/${PROJECT_NAME}-frontend:${IMAGE_TAG} ./frontend
    fi
    
    log_success "Docker images built successfully."
}

push_images() {
    log_info "Pushing Docker images to registry..."
    
    docker push ${DOCKER_REGISTRY}/${PROJECT_NAME}:${IMAGE_TAG}
    
    if [ -d "frontend" ]; then
        docker push ${DOCKER_REGISTRY}/${PROJECT_NAME}-frontend:${IMAGE_TAG}
    fi
    
    log_success "Docker images pushed successfully."
}

deploy_docker_compose() {
    log_info "Deploying with Docker Compose..."
    
    # Stop existing containers
    docker-compose down
    
    # Start services
    docker-compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "Application is healthy and running."
    else
        log_error "Application health check failed."
        exit 1
    fi
    
    log_success "Docker Compose deployment completed."
}

deploy_kubernetes() {
    log_info "Deploying to Kubernetes..."
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        log_warning "kubectl not found. Skipping Kubernetes deployment."
        return
    fi
    
    # Create namespace
    kubectl apply -f k8s/namespace.yaml
    
    # Apply ConfigMap and Secrets
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/secret.yaml
    
    # Deploy database services
    kubectl apply -f k8s/postgres-deployment.yaml
    kubectl apply -f k8s/redis-deployment.yaml
    kubectl apply -f k8s/chromadb-deployment.yaml
    
    # Wait for database services to be ready
    log_info "Waiting for database services to be ready..."
    kubectl wait --for=condition=ready pod -l app=wellness-postgres -n ${NAMESPACE} --timeout=300s
    kubectl wait --for=condition=ready pod -l app=wellness-redis -n ${NAMESPACE} --timeout=300s
    kubectl wait --for=condition=ready pod -l app=wellness-chromadb -n ${NAMESPACE} --timeout=300s
    
    # Deploy monitoring services
    kubectl apply -f k8s/prometheus-deployment.yaml
    kubectl apply -f k8s/grafana-deployment.yaml
    kubectl apply -f k8s/opa-deployment.yaml
    
    # Deploy main application
    kubectl apply -f k8s/deployment.yaml
    kubectl apply -f k8s/service.yaml
    
    # Deploy ingress
    kubectl apply -f k8s/ingress.yaml
    
    # Wait for application to be ready
    log_info "Waiting for application to be ready..."
    kubectl wait --for=condition=ready pod -l app=wellness-ai-backend -n ${NAMESPACE} --timeout=300s
    
    log_success "Kubernetes deployment completed."
}

setup_monitoring() {
    log_info "Setting up monitoring..."
    
    # Create Prometheus configuration
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'wellness-ai'
    static_configs:
      - targets: ['wellness-ai-backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF
    
    # Create Grafana datasource configuration
    mkdir -p monitoring/grafana/datasources
    cat > monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://wellness-prometheus:9090
    isDefault: true
EOF
    
    log_success "Monitoring setup completed."
}

setup_ssl_certificates() {
    log_info "Setting up SSL certificates..."
    
    # Create self-signed certificates for development
    if [ ! -f nginx/ssl/wellness-ai.crt ]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/wellness-ai.key \
            -out nginx/ssl/wellness-ai.crt \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=wellness-ai.local"
    fi
    
    log_success "SSL certificates setup completed."
}

create_nginx_config() {
    log_info "Creating Nginx configuration..."
    
    cat > nginx/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream wellness_backend {
        server wellness-ai-backend:8000;
    }
    
    upstream wellness_frontend {
        server wellness-frontend:3000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        location / {
            proxy_pass http://wellness_frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        location /api/ {
            proxy_pass http://wellness_backend/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        location /health {
            proxy_pass http://wellness_backend/health;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF
    
    log_success "Nginx configuration created."
}

run_migrations() {
    log_info "Running database migrations..."
    
    # Wait for database to be ready
    sleep 10
    
    # Run migrations using Docker Compose
    docker-compose exec wellness-ai python -m alembic upgrade head
    
    log_success "Database migrations completed."
}

initialize_data() {
    log_info "Initializing application data..."
    
    # Create initial wellness resources
    docker-compose exec wellness-ai python -m scripts.init_data
    
    log_success "Data initialization completed."
}

show_status() {
    log_info "Deployment Status:"
    echo "=================="
    
    # Docker Compose status
    if command -v docker-compose &> /dev/null; then
        echo "Docker Compose Services:"
        docker-compose ps
        echo ""
    fi
    
    # Kubernetes status
    if command -v kubectl &> /dev/null; then
        echo "Kubernetes Pods:"
        kubectl get pods -n ${NAMESPACE}
        echo ""
        
        echo "Kubernetes Services:"
        kubectl get services -n ${NAMESPACE}
        echo ""
    fi
    
    # Application health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "Application is healthy!"
        echo "Access URLs:"
        echo "  - Application: http://localhost:8000"
        echo "  - API Docs: http://localhost:8000/docs"
        echo "  - Health Check: http://localhost:8000/health"
        echo "  - Grafana: http://localhost:3000"
        echo "  - Prometheus: http://localhost:9090"
    else
        log_error "Application health check failed."
    fi
}

cleanup() {
    log_info "Cleaning up..."
    
    # Stop Docker Compose services
    docker-compose down
    
    # Remove Kubernetes resources
    if command -v kubectl &> /dev/null; then
        kubectl delete namespace ${NAMESPACE} --ignore-not-found=true
    fi
    
    log_success "Cleanup completed."
}

# Main script
main() {
    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            setup_environment
            build_images
            setup_monitoring
            setup_ssl_certificates
            create_nginx_config
            deploy_docker_compose
            run_migrations
            initialize_data
            show_status
            ;;
        "kubernetes")
            check_prerequisites
            setup_environment
            build_images
            push_images
            deploy_kubernetes
            show_status
            ;;
        "build")
            check_prerequisites
            setup_environment
            build_images
            ;;
        "status")
            show_status
            ;;
        "cleanup")
            cleanup
            ;;
        "help")
            echo "Usage: $0 [deploy|kubernetes|build|status|cleanup|help]"
            echo ""
            echo "Commands:"
            echo "  deploy     - Deploy using Docker Compose (default)"
            echo "  kubernetes - Deploy to Kubernetes"
            echo "  build      - Build Docker images only"
            echo "  status     - Show deployment status"
            echo "  cleanup    - Clean up all resources"
            echo "  help       - Show this help message"
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use '$0 help' for usage information."
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
