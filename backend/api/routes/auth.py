"""
Authentication API Routes - User authentication and authorization
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import logging

from utils.auth import (
    authenticate_user, create_user_tokens, refresh_access_token,
    get_password_hash, get_current_user, update_last_login
)
from database.connection import get_db
from database.schema import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()


# Pydantic models
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = "employee"
    department: Optional[str] = None
    position: Optional[str] = None

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.post("/login", response_model=AuthResponse)
async def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    User login endpoint
    """
    try:
        # Authenticate user
        user = authenticate_user(db, request.email, request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is deactivated"
            )
        
        # Create tokens
        tokens = create_user_tokens(user)
        
        # Update last login
        update_last_login(user, db)
        
        return AuthResponse(
            success=True,
            message="Login successful",
            data={
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "department": user.department,
                    "position": user.position
                },
                "tokens": tokens
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/register", response_model=AuthResponse)
async def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    User registration endpoint
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(request.password)
        new_user = User(
            email=request.email,
            password_hash=hashed_password,
            first_name=request.first_name,
            last_name=request.last_name,
            role=request.role,
            department=request.department,
            position=request.position,
            is_active=True,
            is_verified=False
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create tokens
        tokens = create_user_tokens(new_user)
        
        return AuthResponse(
            success=True,
            message="Registration successful",
            data={
                "user": {
                    "id": new_user.id,
                    "email": new_user.email,
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name,
                    "role": new_user.role,
                    "department": new_user.department,
                    "position": new_user.position
                },
                "tokens": tokens
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    request: TokenRefreshRequest
):
    """
    Refresh access token using refresh token
    """
    try:
        new_access_token = refresh_access_token(request.refresh_token)
        if not new_access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        return AuthResponse(
            success=True,
            message="Token refreshed successfully",
            data={
                "access_token": new_access_token,
                "token_type": "bearer"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/change-password", response_model=AuthResponse)
async def change_password(
    request: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    try:
        # Verify current password
        if not authenticate_user(db, current_user.email, request.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        current_user.password_hash = get_password_hash(request.new_password)
        db.commit()
        
        return AuthResponse(
            success=True,
            message="Password changed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change failed: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.get("/me", response_model=AuthResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information
    """
    try:
        return AuthResponse(
            success=True,
            message="User information retrieved successfully",
            data={
                "user": {
                    "id": current_user.id,
                    "email": current_user.email,
                    "first_name": current_user.first_name,
                    "last_name": current_user.last_name,
                    "role": current_user.role,
                    "department": current_user.department,
                    "position": current_user.position,
                    "is_active": current_user.is_active,
                    "is_verified": current_user.is_verified,
                    "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
                    "created_at": current_user.created_at.isoformat(),
                    "updated_at": current_user.updated_at.isoformat()
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )


@router.post("/logout", response_model=AuthResponse)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    User logout endpoint
    """
    try:
        # In a real implementation, you might want to blacklist the token
        # For now, we'll just return a success response
        return AuthResponse(
            success=True,
            message="Logout successful"
        )
        
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.post("/verify-email", response_model=AuthResponse)
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Verify user email address
    """
    try:
        # In a real implementation, you would verify the token
        # For now, we'll just return a success response
        return AuthResponse(
            success=True,
            message="Email verification successful"
        )
        
    except Exception as e:
        logger.error(f"Email verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )


@router.post("/forgot-password", response_model=AuthResponse)
async def forgot_password(
    email: EmailStr,
    db: Session = Depends(get_db)
):
    """
    Send password reset email
    """
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Don't reveal if user exists or not
            return AuthResponse(
                success=True,
                message="If the email exists, a password reset link has been sent"
            )
        
        # In a real implementation, you would send a password reset email
        # For now, we'll just return a success response
        return AuthResponse(
            success=True,
            message="If the email exists, a password reset link has been sent"
        )
        
    except Exception as e:
        logger.error(f"Forgot password failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process password reset request"
        )


@router.post("/reset-password", response_model=AuthResponse)
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    Reset password using reset token
    """
    try:
        # In a real implementation, you would verify the token and get the user
        # For now, we'll just return a success response
        return AuthResponse(
            success=True,
            message="Password reset successful"
        )
        
    except Exception as e:
        logger.error(f"Password reset failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )
