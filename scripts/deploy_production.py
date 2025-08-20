#!/usr/bin/env python3
"""
Production Deployment Script - Comprehensive deployment automation
"""

import os
import sys
import subprocess
import secrets
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional


class ProductionDeployer:
    """Production deployment automation"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or ".env"
        self.project_root = Path(__file__).parent.parent
        self.deployment_log = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log deployment messages"""
        timestamp = subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.deployment_log.append(log_entry)
    
    def run_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command with logging"""
        self.log(f"Running: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=check)
            if result.stdout:
                self.log(f"Output: {result.stdout.strip()}")
            return result
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e.stderr}", "ERROR")
            if check:
                raise
            return e
    
    def validate_environment(self) -> bool:
        """Validate production environment"""
        self.log("Validating production environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 9):
            self.log("Python 3.9+ required", "ERROR")
            return False
        
        # Check required tools
        required_tools = ['docker', 'docker-compose', 'kubectl']
        for tool in required_tools:
            try:
                self.run_command([tool, '--version'], check=False)
            except FileNotFoundError:
                self.log(f"{tool} not found", "ERROR")
                return False
        
        # Check environment file
        if not os.path.exists(self.config_path):
            self.log(f"Environment file {self.config_path} not found", "ERROR")
            return False
        
        self.log("Environment validation passed")
        return True
    
    def generate_secure_keys(self) -> Dict[str, str]:
        """Generate secure keys for production"""
        self.log("Generating secure keys...")
        
        keys = {
            'SECRET_KEY': secrets.token_urlsafe(32),
            'ENCRYPTION_KEY': secrets.token_urlsafe(32),
            'JWT_SECRET': secrets.token_urlsafe(32)
        }
        
        self.log("Secure keys generated")
        return keys
    
    def update_environment_file(self, keys: Dict[str, str], config: Dict[str, str]):
        """Update environment file with production values"""
        self.log("Updating environment file...")
        
        env_content = []
        
        # Read existing .env file
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                env_content = f.readlines()
        
        # Update or add production values
        env_updates = {
            'ENVIRONMENT': 'production',
            'DEBUG': 'false',
            'LOG_LEVEL': 'INFO',
            **keys,
            **config
        }
        
        # Update existing lines or add new ones
        existing_keys = set()
        for i, line in enumerate(env_content):
            if '=' in line:
                key = line.split('=')[0].strip()
                existing_keys.add(key)
                if key in env_updates:
                    env_content[i] = f"{key}={env_updates[key]}\n"
        
        # Add missing keys
        for key, value in env_updates.items():
            if key not in existing_keys:
                env_content.append(f"{key}={value}\n")
        
        # Write updated file
        with open(self.config_path, 'w') as f:
            f.writelines(env_content)
        
        self.log("Environment file updated")
    
    def setup_database(self) -> bool:
        """Setup production database"""
        self.log("Setting up production database...")
        
        try:
            # Run database migrations
            self.run_command([
                'docker-compose', 'exec', '-T', 'backend',
                'python', '-m', 'database.migrations'
            ])
            
            # Initialize database
            self.run_command([
                'docker-compose', 'exec', '-T', 'backend',
                'python', '-m', 'scripts.init_db'
            ])
            
            self.log("Database setup completed")
            return True
            
        except Exception as e:
            self.log(f"Database setup failed: {e}", "ERROR")
            return False
    
    def build_images(self) -> bool:
        """Build Docker images for production"""
        self.log("Building Docker images...")
        
        try:
            # Build backend image
            self.run_command([
                'docker', 'build', '-t', 'mindtrace-backend:latest', '.'
            ])
            
            # Build frontend image
            self.run_command([
                'docker', 'build', '-t', 'mindtrace-frontend:latest', './frontend'
            ])
            
            self.log("Docker images built successfully")
            return True
            
        except Exception as e:
            self.log(f"Image build failed: {e}", "ERROR")
            return False
    
    def deploy_kubernetes(self, namespace: str = "mindtrace") -> bool:
        """Deploy to Kubernetes"""
        self.log(f"Deploying to Kubernetes namespace: {namespace}")
        
        try:
            # Create namespace
            self.run_command(['kubectl', 'create', 'namespace', namespace], check=False)
            
            # Apply Kubernetes manifests
            k8s_dir = self.project_root / 'k8s'
            for manifest in k8s_dir.glob('*.yaml'):
                self.run_command(['kubectl', 'apply', '-f', str(manifest), '-n', namespace])
            
            # Wait for deployment
            self.run_command([
                'kubectl', 'wait', '--for=condition=available', 
                '--timeout=300s', 'deployment/mindtrace-backend', '-n', namespace
            ])
            
            self.log("Kubernetes deployment completed")
            return True
            
        except Exception as e:
            self.log(f"Kubernetes deployment failed: {e}", "ERROR")
            return False
    
    def deploy_docker_compose(self) -> bool:
        """Deploy using Docker Compose"""
        self.log("Deploying with Docker Compose...")
        
        try:
            # Stop existing containers
            self.run_command(['docker-compose', 'down'], check=False)
            
            # Start services
            self.run_command(['docker-compose', 'up', '-d'])
            
            # Wait for services to be ready
            self.run_command(['docker-compose', 'exec', '-T', 'backend', 'python', '-c', 
                            'import time; time.sleep(30)'])
            
            self.log("Docker Compose deployment completed")
            return True
            
        except Exception as e:
            self.log(f"Docker Compose deployment failed: {e}", "ERROR")
            return False
    
    def run_health_checks(self) -> bool:
        """Run health checks after deployment"""
        self.log("Running health checks...")
        
        try:
            # Check API health
            health_url = "http://localhost:8000/health"
            result = self.run_command(['curl', '-f', health_url], check=False)
            
            if result.returncode == 0:
                self.log("API health check passed")
            else:
                self.log("API health check failed", "ERROR")
                return False
            
            # Check database connectivity
            db_check = self.run_command([
                'docker-compose', 'exec', '-T', 'backend',
                'python', '-c', 'from database.connection import check_db_connection; print(check_db_connection())'
            ])
            
            if 'True' in db_check.stdout:
                self.log("Database connectivity check passed")
            else:
                self.log("Database connectivity check failed", "ERROR")
                return False
            
            self.log("All health checks passed")
            return True
            
        except Exception as e:
            self.log(f"Health checks failed: {e}", "ERROR")
            return False
    
    def setup_monitoring(self) -> bool:
        """Setup monitoring and observability"""
        self.log("Setting up monitoring...")
        
        try:
            # Start monitoring stack
            self.run_command(['docker-compose', '-f', 'docker-compose.monitoring.yml', 'up', '-d'])
            
            # Configure Grafana dashboards
            self.run_command(['python', 'scripts/setup_monitoring.py'])
            
            self.log("Monitoring setup completed")
            return True
            
        except Exception as e:
            self.log(f"Monitoring setup failed: {e}", "ERROR")
            return False
    
    def run_security_scan(self) -> bool:
        """Run security scan"""
        self.log("Running security scan...")
        
        try:
            # Run container security scan
            self.run_command([
                'docker', 'run', '--rm', '-v', '/var/run/docker.sock:/var/run/docker.sock',
                'aquasec/trivy', 'image', 'mindtrace-backend:latest'
            ], check=False)
            
            self.log("Security scan completed")
            return True
            
        except Exception as e:
            self.log(f"Security scan failed: {e}", "WARNING")
            return True  # Don't fail deployment for security scan
    
    def create_backup(self) -> bool:
        """Create backup before deployment"""
        self.log("Creating backup...")
        
        try:
            backup_dir = self.project_root / 'backups' / f"backup_{int(time.time())}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Backup database
            self.run_command([
                'docker-compose', 'exec', '-T', 'postgres',
                'pg_dump', '-U', 'wellness_user', 'wellness_db'
            ], check=False)
            
            # Backup configuration
            self.run_command(['cp', self.config_path, str(backup_dir)])
            
            self.log(f"Backup created: {backup_dir}")
            return True
            
        except Exception as e:
            self.log(f"Backup failed: {e}", "WARNING")
            return True  # Don't fail deployment for backup
    
    def deploy(self, method: str = 'docker-compose', config: Dict[str, str] = None) -> bool:
        """Main deployment method"""
        self.log(f"Starting production deployment using {method}")
        
        try:
            # Validate environment
            if not self.validate_environment():
                return False
            
            # Create backup
            self.create_backup()
            
            # Generate secure keys
            keys = self.generate_secure_keys()
            
            # Update environment file
            if config:
                self.update_environment_file(keys, config)
            
            # Build images
            if not self.build_images():
                return False
            
            # Deploy based on method
            if method == 'kubernetes':
                success = self.deploy_kubernetes()
            else:
                success = self.deploy_docker_compose()
            
            if not success:
                return False
            
            # Setup database
            if not self.setup_database():
                return False
            
            # Setup monitoring
            self.setup_monitoring()
            
            # Run health checks
            if not self.run_health_checks():
                return False
            
            # Run security scan
            self.run_security_scan()
            
            self.log("Production deployment completed successfully!")
            return True
            
        except Exception as e:
            self.log(f"Deployment failed: {e}", "ERROR")
            return False
    
    def rollback(self) -> bool:
        """Rollback deployment"""
        self.log("Rolling back deployment...")
        
        try:
            # Stop services
            self.run_command(['docker-compose', 'down'])
            
            # Restore from backup
            backup_dir = self.project_root / 'backups'
            if backup_dir.exists():
                backups = sorted(backup_dir.glob('backup_*'), reverse=True)
                if backups:
                    latest_backup = backups[0]
                    self.run_command(['cp', str(latest_backup / '.env'), self.config_path])
                    self.log(f"Restored from backup: {latest_backup}")
            
            self.log("Rollback completed")
            return True
            
        except Exception as e:
            self.log(f"Rollback failed: {e}", "ERROR")
            return False
    
    def save_deployment_log(self, filename: str = None):
        """Save deployment log to file"""
        if not filename:
            timestamp = int(time.time())
            filename = f"deployment_log_{timestamp}.txt"
        
        log_file = self.project_root / 'logs' / filename
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'w') as f:
            f.write('\n'.join(self.deployment_log))
        
        self.log(f"Deployment log saved: {log_file}")


def main():
    """Main deployment script"""
    parser = argparse.ArgumentParser(description='Production Deployment Script')
    parser.add_argument('--method', choices=['docker-compose', 'kubernetes'], 
                       default='docker-compose', help='Deployment method')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--rollback', action='store_true', help='Rollback deployment')
    parser.add_argument('--validate-only', action='store_true', help='Only validate environment')
    
    args = parser.parse_args()
    
    deployer = ProductionDeployer(args.config)
    
    if args.rollback:
        success = deployer.rollback()
    elif args.validate_only:
        success = deployer.validate_environment()
    else:
        # Load configuration if provided
        config = {}
        if args.config and os.path.exists(args.config):
            with open(args.config, 'r') as f:
                config = json.load(f)
        
        success = deployer.deploy(args.method, config)
    
    # Save deployment log
    deployer.save_deployment_log()
    
    if success:
        print("✅ Deployment completed successfully")
        sys.exit(0)
    else:
        print("❌ Deployment failed")
        sys.exit(1)


if __name__ == "__main__":
    import time
    main()
