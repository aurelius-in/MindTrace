"""
Resources API Routes - Wellness resources and content management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging

from utils.auth import get_current_user, require_permission
from database.connection import get_db
from database.schema import User, Resource, ResourceInteraction

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/resources", tags=["resources"])


# Pydantic models
class ResourceCreateRequest(BaseModel):
    title: str
    description: str
    category: str
    difficulty_level: str
    duration_minutes: Optional[int] = None
    content_url: Optional[str] = None
    tags: List[str] = []
    author: Optional[str] = None

class ResourceUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_minutes: Optional[int] = None
    content_url: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    is_active: Optional[bool] = None

class ResourceInteractionRequest(BaseModel):
    interaction_type: str  # view, like, bookmark, complete, rate
    rating: Optional[int] = None
    comment: Optional[str] = None

class ResourceResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.get("/", response_model=ResourceResponse)
async def get_resources(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    limit: int = Query(20, ge=1, le=100, description="Number of resources to return"),
    offset: int = Query(0, ge=0, description="Number of resources to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get wellness resources with filtering and pagination
    """
    try:
        query = db.query(Resource).filter(Resource.is_active == True)
        
        # Apply filters
        if category:
            query = query.filter(Resource.category == category)
        
        if difficulty_level:
            query = query.filter(Resource.difficulty_level == difficulty_level)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Resource.title.ilike(search_term)) |
                (Resource.description.ilike(search_term))
            )
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        resources = query.offset(offset).limit(limit).all()
        
        return ResourceResponse(
            success=True,
            message="Resources retrieved successfully",
            data={
                "resources": [resource.to_dict() for resource in resources],
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get resources: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve resources"
        )


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific resource by ID
    """
    try:
        resource = db.query(Resource).filter(
            Resource.id == resource_id,
            Resource.is_active == True
        ).first()
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        return ResourceResponse(
            success=True,
            message="Resource retrieved successfully",
            data={"resource": resource.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get resource {resource_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve resource"
        )


@router.post("/", response_model=ResourceResponse)
async def create_resource(
    request: ResourceCreateRequest,
    current_user: User = Depends(require_permission("manage_resources")),
    db: Session = Depends(get_db)
):
    """
    Create a new wellness resource
    """
    try:
        resource = Resource(
            title=request.title,
            description=request.description,
            category=request.category,
            difficulty_level=request.difficulty_level,
            duration_minutes=request.duration_minutes,
            content_url=request.content_url,
            tags=request.tags,
            author=request.author or f"{current_user.first_name} {current_user.last_name}",
            is_active=True
        )
        
        db.add(resource)
        db.commit()
        db.refresh(resource)
        
        return ResourceResponse(
            success=True,
            message="Resource created successfully",
            data={"resource": resource.to_dict()}
        )
        
    except Exception as e:
        logger.error(f"Failed to create resource: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create resource"
        )


@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: str,
    request: ResourceUpdateRequest,
    current_user: User = Depends(require_permission("manage_resources")),
    db: Session = Depends(get_db)
):
    """
    Update an existing resource
    """
    try:
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        # Update fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resource, field, value)
        
        db.commit()
        db.refresh(resource)
        
        return ResourceResponse(
            success=True,
            message="Resource updated successfully",
            data={"resource": resource.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update resource {resource_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update resource"
        )


@router.delete("/{resource_id}", response_model=ResourceResponse)
async def delete_resource(
    resource_id: str,
    current_user: User = Depends(require_permission("manage_resources")),
    db: Session = Depends(get_db)
):
    """
    Delete a resource (soft delete by setting is_active to False)
    """
    try:
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        resource.is_active = False
        db.commit()
        
        return ResourceResponse(
            success=True,
            message="Resource deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete resource {resource_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete resource"
        )


@router.post("/{resource_id}/interact", response_model=ResourceResponse)
async def interact_with_resource(
    resource_id: str,
    request: ResourceInteractionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Record user interaction with a resource
    """
    try:
        # Check if resource exists
        resource = db.query(Resource).filter(
            Resource.id == resource_id,
            Resource.is_active == True
        ).first()
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        # Create interaction
        interaction = ResourceInteraction(
            user_id=current_user.id,
            resource_id=resource_id,
            interaction_type=request.interaction_type,
            rating=request.rating,
            comment=request.comment
        )
        
        db.add(interaction)
        
        # Update resource rating if this is a rating interaction
        if request.interaction_type == "rate" and request.rating:
            # Calculate new average rating
            all_ratings = db.query(ResourceInteraction).filter(
                ResourceInteraction.resource_id == resource_id,
                ResourceInteraction.interaction_type == "rate",
                ResourceInteraction.rating.isnot(None)
            ).all()
            
            if all_ratings:
                avg_rating = sum(r.rating for r in all_ratings) / len(all_ratings)
                resource.rating = round(avg_rating, 1)
                resource.review_count = len(all_ratings)
        
        db.commit()
        
        return ResourceResponse(
            success=True,
            message="Interaction recorded successfully",
            data={"interaction": interaction.to_dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to record interaction: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record interaction"
        )


@router.get("/{resource_id}/interactions", response_model=ResourceResponse)
async def get_resource_interactions(
    resource_id: str,
    current_user: User = Depends(require_permission("read_resources")),
    db: Session = Depends(get_db)
):
    """
    Get interactions for a specific resource
    """
    try:
        # Check if resource exists
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        interactions = db.query(ResourceInteraction).filter(
            ResourceInteraction.resource_id == resource_id
        ).all()
        
        return ResourceResponse(
            success=True,
            message="Resource interactions retrieved successfully",
            data={
                "interactions": [interaction.to_dict() for interaction in interactions],
                "count": len(interactions)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get resource interactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve resource interactions"
        )


@router.get("/user/interactions", response_model=ResourceResponse)
async def get_user_interactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's resource interactions
    """
    try:
        interactions = db.query(ResourceInteraction).filter(
            ResourceInteraction.user_id == current_user.id
        ).all()
        
        return ResourceResponse(
            success=True,
            message="User interactions retrieved successfully",
            data={
                "interactions": [interaction.to_dict() for interaction in interactions],
                "count": len(interactions)
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get user interactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user interactions"
        )


@router.get("/categories", response_model=ResourceResponse)
async def get_resource_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all available resource categories
    """
    try:
        categories = db.query(Resource.category).distinct().filter(
            Resource.is_active == True
        ).all()
        
        return ResourceResponse(
            success=True,
            message="Categories retrieved successfully",
            data={"categories": [cat[0] for cat in categories]}
        )
        
    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve categories"
        )


@router.get("/recommendations", response_model=ResourceResponse)
async def get_recommended_resources(
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized resource recommendations
    """
    try:
        # Get user's interaction history
        user_interactions = db.query(ResourceInteraction).filter(
            ResourceInteraction.user_id == current_user.id
        ).all()
        
        # Simple recommendation logic based on user preferences
        # In a real implementation, this would use ML/AI
        if user_interactions:
            # Get user's preferred categories
            preferred_categories = {}
            for interaction in user_interactions:
                resource = db.query(Resource).filter(Resource.id == interaction.resource_id).first()
                if resource:
                    category = resource.category
                    preferred_categories[category] = preferred_categories.get(category, 0) + 1
            
            # Get top category
            top_category = max(preferred_categories.items(), key=lambda x: x[1])[0] if preferred_categories else "mindfulness"
            
            # Get resources from preferred category
            recommendations = db.query(Resource).filter(
                Resource.category == top_category,
                Resource.is_active == True
            ).limit(limit).all()
        else:
            # Default recommendations for new users
            recommendations = db.query(Resource).filter(
                Resource.is_active == True
            ).order_by(Resource.rating.desc()).limit(limit).all()
        
        return ResourceResponse(
            success=True,
            message="Recommendations retrieved successfully",
            data={
                "recommendations": [resource.to_dict() for resource in recommendations],
                "count": len(recommendations)
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recommendations"
        )
