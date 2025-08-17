"""
Users API Routes - User management and profile operations
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import logging

from utils.auth import get_current_user, require_permission, require_role
from database.connection import get_db
from database.schema import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])


# Pydantic models
class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = "employee"
    department: Optional[str] = None
    position: Optional[str] = None
    manager_id: Optional[str] = None

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    manager_id: Optional[str] = None
    is_active: Optional[bool] = None

class UserProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None

class UserResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.get("/", response_model=UserResponse)
async def get_users(
    department: Optional[str] = Query(None, description="Filter by department"),
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in name and email"),
    limit: int = Query(20, ge=1, le=100, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Number of users to skip"),
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Get users with filtering and pagination
    """
    try:
        query = db.query(User)
        
        # Apply filters
        if department:
            query = query.filter(User.department == department)
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (User.first_name.ilike(search_term)) |
                (User.last_name.ilike(search_term)) |
                (User.email.ilike(search_term))
            )
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        users = query.offset(offset).limit(limit).all()
        
        return UserResponse(
            success=True,
            message="Users retrieved successfully",
            data={
                "users": [user.to_dict() for user in users],
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID
    """
    try:
        # Check permissions - users can only view their own profile unless they have manage_users permission
        if current_user.id != user_id and not has_permission(current_user, "manage_users"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view this user"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            success=True,
            message="User retrieved successfully",
            data={"user": user.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.post("/", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Create a new user
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate manager if provided
        if request.manager_id:
            manager = db.query(User).filter(User.id == request.manager_id).first()
            if not manager:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Manager not found"
                )
        
        # Create new user
        from utils.auth import get_password_hash
        hashed_password = get_password_hash(request.password)
        
        new_user = User(
            email=request.email,
            password_hash=hashed_password,
            first_name=request.first_name,
            last_name=request.last_name,
            role=request.role,
            department=request.department,
            position=request.position,
            manager_id=request.manager_id,
            is_active=True,
            is_verified=False
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return UserResponse(
            success=True,
            message="User created successfully",
            data={"user": new_user.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Update an existing user
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate manager if provided
        if request.manager_id:
            manager = db.query(User).filter(User.id == request.manager_id).first()
            if not manager:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Manager not found"
                )
        
        # Update fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return UserResponse(
            success=True,
            message="User updated successfully",
            data={"user": user.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user {user_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Delete a user (soft delete by setting is_active to False)
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prevent self-deletion
        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        user.is_active = False
        db.commit()
        
        return UserResponse(
            success=True,
            message="User deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete user {user_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    """
    try:
        # Update fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        
        return UserResponse(
            success=True,
            message="Profile updated successfully",
            data={"user": current_user.to_dict()}
        )
        
    except Exception as e:
        logger.error(f"Failed to update profile: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/team/members", response_model=UserResponse)
async def get_team_members(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get team members for current user (if manager) or team members of current user's manager
    """
    try:
        team_members = []
        
        if current_user.role in ["manager", "hr", "admin"]:
            # Get direct reports
            direct_reports = db.query(User).filter(
                User.manager_id == current_user.id,
                User.is_active == True
            ).all()
            team_members.extend(direct_reports)
        
        # Get team members from same department
        department_members = db.query(User).filter(
            User.department == current_user.department,
            User.id != current_user.id,
            User.is_active == True
        ).all()
        team_members.extend(department_members)
        
        # Remove duplicates
        unique_members = list({member.id: member for member in team_members}.values())
        
        return UserResponse(
            success=True,
            message="Team members retrieved successfully",
            data={
                "team_members": [member.to_dict() for member in unique_members],
                "count": len(unique_members)
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get team members: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team members"
        )


@router.get("/departments", response_model=UserResponse)
async def get_departments(
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Get all departments
    """
    try:
        departments = db.query(User.department).distinct().filter(
            User.department.isnot(None),
            User.is_active == True
        ).all()
        
        return UserResponse(
            success=True,
            message="Departments retrieved successfully",
            data={"departments": [dept[0] for dept in departments]}
        )
        
    except Exception as e:
        logger.error(f"Failed to get departments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve departments"
        )


@router.get("/roles", response_model=UserResponse)
async def get_roles(
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Get all user roles
    """
    try:
        roles = db.query(User.role).distinct().filter(
            User.is_active == True
        ).all()
        
        return UserResponse(
            success=True,
            message="Roles retrieved successfully",
            data={"roles": [role[0] for role in roles]}
        )
        
    except Exception as e:
        logger.error(f"Failed to get roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve roles"
        )


@router.get("/stats", response_model=UserResponse)
async def get_user_stats(
    current_user: User = Depends(require_permission("manage_users")),
    db: Session = Depends(get_db)
):
    """
    Get user statistics
    """
    try:
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        verified_users = db.query(User).filter(User.is_verified == True).count()
        
        # Role distribution
        role_stats = {}
        roles = db.query(User.role, db.func.count(User.id)).group_by(User.role).all()
        for role, count in roles:
            role_stats[role] = count
        
        # Department distribution
        dept_stats = {}
        departments = db.query(User.department, db.func.count(User.id)).filter(
            User.department.isnot(None)
        ).group_by(User.department).all()
        for dept, count in departments:
            dept_stats[dept] = count
        
        return UserResponse(
            success=True,
            message="User statistics retrieved successfully",
            data={
                "total_users": total_users,
                "active_users": active_users,
                "verified_users": verified_users,
                "role_distribution": role_stats,
                "department_distribution": dept_stats
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get user stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user statistics"
        )


# Helper function for permission checking
def has_permission(user: User, permission: str) -> bool:
    """Check if user has a specific permission"""
    from utils.auth import get_user_permissions
    permissions = get_user_permissions(user)
    return permission in permissions
