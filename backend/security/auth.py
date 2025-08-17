from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import logging
import secrets
import hashlib

from config.settings import settings
from database.connection import get_db_session
from database.schema import User, Role

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

class AuthManager:
    """Authentication and authorization manager."""
    
    def __init__(self):
        self.secret_key = settings.security.secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.security.access_token_expire_minutes
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def get_user_by_email(self, email: str, db: Session) -> Optional[User]:
        """Get a user by email."""
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_external_id(self, external_id: str, db: Session) -> Optional[User]:
        """Get a user by external ID."""
        return db.query(User).filter(User.external_id == external_id).first()
    
    def authenticate_user(self, email: str, password: str, db: Session) -> Optional[User]:
        """Authenticate a user with email and password."""
        user = self.get_user_by_email(email, db)
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user
    
    def create_user(self, user_data: Dict[str, Any], db: Session) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = self.get_user_by_email(user_data["email"], db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Hash password
        hashed_password = self.get_password_hash(user_data["password"])
        
        # Create user
        user = User(
            external_id=user_data["external_id"],
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            department=user_data.get("department"),
            position=user_data.get("position"),
            password_hash=hashed_password,
            consent_given=user_data.get("consent_given", False),
            consent_date=datetime.utcnow() if user_data.get("consent_given") else None
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    def update_user_consent(self, user_id: str, consent_given: bool, db: Session) -> User:
        """Update user consent status."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.consent_given = consent_given
        user.consent_date = datetime.utcnow() if consent_given else None
        
        db.commit()
        db.refresh(user)
        
        return user

# Global auth manager instance
auth_manager = AuthManager()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
) -> User:
    """Get the current authenticated user."""
    token = credentials.credentials
    payload = auth_manager.verify_token(token)
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def require_consent(current_user: User = Depends(get_current_user)) -> User:
    """Require user consent for data processing."""
    if not current_user.consent_given:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User consent required for this operation"
        )
    return current_user

def require_role(required_roles: List[str]):
    """Decorator to require specific roles."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_roles = [role.name for role in current_user.roles]
        
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {required_roles}"
            )
        
        return current_user
    
    return role_checker

def require_permission(permission: str, resource: str = None):
    """Decorator to require specific permissions."""
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        user_permissions = []
        for role in current_user.roles:
            if role.permissions:
                for resource_type, perms in role.permissions.items():
                    if resource is None or resource_type == resource:
                        user_permissions.extend(perms)
        
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required permission: {permission}"
            )
        
        return current_user
    
    return permission_checker

# Role-based dependencies
def require_employee_role():
    """Require employee role."""
    return require_role(["employee", "manager", "hr", "admin"])

def require_manager_role():
    """Require manager role."""
    return require_role(["manager", "hr", "admin"])

def require_hr_role():
    """Require HR role."""
    return require_role(["hr", "admin"])

def require_admin_role():
    """Require admin role."""
    return require_role(["admin"])

# Permission-based dependencies
def require_wellness_read():
    """Require wellness read permission."""
    return require_permission("read", "wellness")

def require_wellness_create():
    """Require wellness create permission."""
    return require_permission("create", "wellness")

def require_analytics_read():
    """Require analytics read permission."""
    return require_permission("read_own", "analytics")

def require_analytics_team_read():
    """Require team analytics read permission."""
    return require_permission("read_team", "analytics")

def require_analytics_org_read():
    """Require organizational analytics read permission."""
    return require_permission("read_org", "analytics")

class SecurityUtils:
    """Security utility functions."""
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a secure random token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_data(data: str) -> str:
        """Hash data using SHA-256."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength."""
        errors = []
        warnings = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            warnings.append("Password should contain at least one special character")
        
        if len(password) < 12:
            warnings.append("Consider using a longer password for better security")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        import html
        return html.escape(input_str.strip())
    
    @staticmethod
    def rate_limit_key(user_id: str, action: str) -> str:
        """Generate a rate limiting key."""
        return f"rate_limit:{user_id}:{action}"

class SessionManager:
    """Session management utilities."""
    
    def __init__(self):
        self.active_sessions = {}
    
    def create_session(self, user_id: str, session_data: Dict[str, Any] = None) -> str:
        """Create a new session for a user."""
        session_id = SecurityUtils.generate_secure_token()
        session_info = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "data": session_data or {}
        }
        self.active_sessions[session_id] = session_info
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information."""
        session = self.active_sessions.get(session_id)
        if session:
            session["last_activity"] = datetime.utcnow()
        return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]):
        """Update session data."""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["data"].update(data)
            self.active_sessions[session_id]["last_activity"] = datetime.utcnow()
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    def cleanup_expired_sessions(self, max_age_hours: int = 24):
        """Clean up expired sessions."""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        expired_sessions = [
            session_id for session_id, session in self.active_sessions.items()
            if session["last_activity"] < cutoff_time
        ]
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

# Global session manager instance
session_manager = SessionManager()

# Export commonly used functions and classes
__all__ = [
    'AuthManager',
    'auth_manager',
    'get_current_user',
    'get_current_active_user',
    'require_consent',
    'require_role',
    'require_permission',
    'require_employee_role',
    'require_manager_role',
    'require_hr_role',
    'require_admin_role',
    'require_wellness_read',
    'require_wellness_create',
    'require_analytics_read',
    'require_analytics_team_read',
    'require_analytics_org_read',
    'SecurityUtils',
    'SessionManager',
    'session_manager'
]
