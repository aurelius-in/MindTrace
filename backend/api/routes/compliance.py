"""
Compliance API Routes - Privacy, audit trails, and compliance management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from utils.auth import get_current_user, require_permission, require_role
from database.connection import get_db
from database.schema import User, ComplianceRecord

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/compliance", tags=["compliance"])


# Pydantic models
class ComplianceRecordCreateRequest(BaseModel):
    record_type: str  # data_access, privacy_consent, audit_log
    action: str
    details: dict = {}

class ComplianceResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


@router.get("/audit-trail", response_model=ComplianceResponse)
async def get_audit_trail(
    record_type: Optional[str] = Query(None, description="Filter by record type"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=200, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    current_user: User = Depends(require_permission("view_logs")),
    db: Session = Depends(get_db)
):
    """
    Get audit trail records
    """
    try:
        query = db.query(ComplianceRecord)
        
        # Apply filters
        if record_type:
            query = query.filter(ComplianceRecord.record_type == record_type)
        
        if user_id:
            query = query.filter(ComplianceRecord.user_id == user_id)
        
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date)
                query = query.filter(ComplianceRecord.created_at >= start_datetime)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use YYYY-MM-DD"
                )
        
        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date) + timedelta(days=1)
                query = query.filter(ComplianceRecord.created_at < end_datetime)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use YYYY-MM-DD"
                )
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination and ordering
        records = query.order_by(ComplianceRecord.created_at.desc()).offset(offset).limit(limit).all()
        
        return ComplianceResponse(
            success=True,
            message="Audit trail retrieved successfully",
            data={
                "records": [record.to_dict() for record in records],
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get audit trail: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve audit trail"
        )


@router.post("/log", response_model=ComplianceResponse)
async def log_compliance_event(
    request: ComplianceRecordCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Log a compliance event
    """
    try:
        record = ComplianceRecord(
            user_id=current_user.id,
            record_type=request.record_type,
            action=request.action,
            details=request.details
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return ComplianceResponse(
            success=True,
            message="Compliance event logged successfully",
            data={"record": record.to_dict()}
        )
        
    except Exception as e:
        logger.error(f"Failed to log compliance event: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log compliance event"
        )


@router.get("/privacy-consent", response_model=ComplianceResponse)
async def get_privacy_consent_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get privacy consent status for current user
    """
    try:
        # Get latest privacy consent record
        latest_consent = db.query(ComplianceRecord).filter(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.record_type == "privacy_consent"
        ).order_by(ComplianceRecord.created_at.desc()).first()
        
        # Get all privacy-related records
        privacy_records = db.query(ComplianceRecord).filter(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.record_type.in_(["privacy_consent", "data_access"])
        ).order_by(ComplianceRecord.created_at.desc()).limit(10).all()
        
        consent_status = {
            "has_consent": latest_consent is not None and latest_consent.action == "consent_given",
            "last_updated": latest_consent.created_at.isoformat() if latest_consent else None,
            "consent_version": latest_consent.details.get("version") if latest_consent else None,
            "recent_activity": [record.to_dict() for record in privacy_records]
        }
        
        return ComplianceResponse(
            success=True,
            message="Privacy consent status retrieved successfully",
            data=consent_status
        )
        
    except Exception as e:
        logger.error(f"Failed to get privacy consent status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve privacy consent status"
        )


@router.post("/privacy-consent", response_model=ComplianceResponse)
async def update_privacy_consent(
    consent_given: bool,
    consent_version: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update privacy consent for current user
    """
    try:
        action = "consent_given" if consent_given else "consent_withdrawn"
        
        record = ComplianceRecord(
            user_id=current_user.id,
            record_type="privacy_consent",
            action=action,
            details={
                "version": consent_version,
                "timestamp": datetime.utcnow().isoformat(),
                "ip_address": "127.0.0.1"  # In real implementation, get from request
            }
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return ComplianceResponse(
            success=True,
            message=f"Privacy consent {'given' if consent_given else 'withdrawn'} successfully",
            data={"record": record.to_dict()}
        )
        
    except Exception as e:
        logger.error(f"Failed to update privacy consent: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update privacy consent"
        )


@router.get("/data-rights", response_model=ComplianceResponse)
async def get_data_rights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get data rights information for current user
    """
    try:
        # Get user's data access records
        data_access_records = db.query(ComplianceRecord).filter(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.record_type == "data_access"
        ).order_by(ComplianceRecord.created_at.desc()).limit(20).all()
        
        # Calculate data retention information
        from config.settings import settings
        retention_days = settings.DATA_RETENTION_DAYS
        
        data_rights = {
            "data_retention_days": retention_days,
            "data_anonymization": settings.ANONYMIZE_DATA,
            "compliance_framework": settings.COMPLIANCE_FRAMEWORK,
            "recent_data_access": [record.to_dict() for record in data_access_records],
            "rights": [
                "Right to access personal data",
                "Right to rectification",
                "Right to erasure",
                "Right to data portability",
                "Right to object to processing",
                "Right to withdraw consent"
            ]
        }
        
        return ComplianceResponse(
            success=True,
            message="Data rights information retrieved successfully",
            data=data_rights
        )
        
    except Exception as e:
        logger.error(f"Failed to get data rights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve data rights information"
        )


@router.post("/data-export", response_model=ComplianceResponse)
async def request_data_export(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request data export for current user
    """
    try:
        # Log the data export request
        record = ComplianceRecord(
            user_id=current_user.id,
            record_type="data_access",
            action="data_export_requested",
            details={
                "request_type": "data_export",
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending"
            }
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        # In a real implementation, this would trigger a background job
        # to prepare the data export
        
        return ComplianceResponse(
            success=True,
            message="Data export request submitted successfully",
            data={
                "request_id": record.id,
                "estimated_completion": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
                "record": record.to_dict()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to request data export: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to request data export"
        )


@router.post("/data-deletion", response_model=ComplianceResponse)
async def request_data_deletion(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request data deletion for current user
    """
    try:
        # Log the data deletion request
        record = ComplianceRecord(
            user_id=current_user.id,
            record_type="data_access",
            action="data_deletion_requested",
            details={
                "request_type": "data_deletion",
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending"
            }
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        # In a real implementation, this would trigger a background job
        # to handle the data deletion process
        
        return ComplianceResponse(
            success=True,
            message="Data deletion request submitted successfully",
            data={
                "request_id": record.id,
                "estimated_completion": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "record": record.to_dict()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to request data deletion: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to request data deletion"
        )


@router.get("/compliance-status", response_model=ComplianceResponse)
async def get_compliance_status(
    current_user: User = Depends(require_permission("view_logs")),
    db: Session = Depends(get_db)
):
    """
    Get overall compliance status
    """
    try:
        from config.settings import settings
        
        # Get compliance statistics
        total_records = db.query(ComplianceRecord).count()
        privacy_consents = db.query(ComplianceRecord).filter(
            ComplianceRecord.record_type == "privacy_consent"
        ).count()
        data_access_records = db.query(ComplianceRecord).filter(
            ComplianceRecord.record_type == "data_access"
        ).count()
        
        # Get recent compliance events
        recent_events = db.query(ComplianceRecord).order_by(
            ComplianceRecord.created_at.desc()
        ).limit(10).all()
        
        compliance_status = {
            "framework": settings.COMPLIANCE_FRAMEWORK,
            "data_retention_days": settings.DATA_RETENTION_DAYS,
            "anonymization_enabled": settings.ANONYMIZE_DATA,
            "privacy_controls_enabled": settings.ENABLE_PRIVACY_CONTROLS,
            "statistics": {
                "total_compliance_records": total_records,
                "privacy_consents": privacy_consents,
                "data_access_records": data_access_records
            },
            "recent_events": [record.to_dict() for record in recent_events],
            "compliance_checks": {
                "data_retention": "compliant",
                "privacy_consent": "compliant" if privacy_consents > 0 else "non_compliant",
                "audit_trail": "compliant" if total_records > 0 else "non_compliant"
            }
        }
        
        return ComplianceResponse(
            success=True,
            message="Compliance status retrieved successfully",
            data=compliance_status
        )
        
    except Exception as e:
        logger.error(f"Failed to get compliance status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve compliance status"
        )


@router.get("/export", response_model=ComplianceResponse)
async def export_compliance_data(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    format: str = Query("json", description="Export format (json, csv)"),
    current_user: User = Depends(require_permission("view_logs")),
    db: Session = Depends(get_db)
):
    """
    Export compliance data for reporting
    """
    try:
        # Parse dates
        try:
            start_datetime = datetime.fromisoformat(start_date)
            end_datetime = datetime.fromisoformat(end_date) + timedelta(days=1)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
        
        # Get compliance records in date range
        records = db.query(ComplianceRecord).filter(
            ComplianceRecord.created_at >= start_datetime,
            ComplianceRecord.created_at < end_datetime
        ).order_by(ComplianceRecord.created_at).all()
        
        # In a real implementation, this would generate and return a file
        # For now, we'll return the data structure
        
        return ComplianceResponse(
            success=True,
            message="Compliance data export generated successfully",
            data={
                "start_date": start_date,
                "end_date": end_date,
                "format": format,
                "record_count": len(records),
                "export_url": f"/exports/compliance_{start_date}_{end_date}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{format}",
                "records": [record.to_dict() for record in records]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export compliance data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export compliance data"
        )
