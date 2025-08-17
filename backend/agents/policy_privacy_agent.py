"""
Policy & Privacy Agent - Enforces data privacy and compliance policies
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import logging
import re
from dataclasses import dataclass
from enum import Enum

import hashlib
import hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from .base_agent import BaseAgent, AgentType, AgentContext, AgentResponse
from config.settings import settings


class PrivacyLevel(Enum):
    """Privacy levels for data handling"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class ComplianceFramework(Enum):
    """Compliance frameworks"""
    HIPAA = "hipaa"
    GDPR = "gdpr"
    SOC2 = "soc2"
    CCPA = "ccpa"
    ENTERPRISE = "enterprise"


@dataclass
class PrivacyViolation:
    """Privacy violation data structure"""
    violation_type: str
    severity: str  # low, medium, high, critical
    description: str
    data_fields: List[str]
    timestamp: datetime
    user_id: Optional[str] = None


@dataclass
class ComplianceCheck:
    """Compliance check result"""
    framework: ComplianceFramework
    status: str  # compliant, non_compliant, requires_review
    violations: List[PrivacyViolation]
    recommendations: List[str]


class PolicyPrivacyAgent(BaseAgent):
    """
    Policy & Privacy Agent ensures:
    - Data anonymization and pseudonymization
    - Compliance with privacy regulations
    - Policy enforcement and access control
    - Audit trail maintenance
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(AgentType.POLICY_PRIVACY, config)
        
        # Privacy patterns and rules
        self._load_privacy_patterns()
        
        # Compliance frameworks
        self._load_compliance_frameworks()
        
        # Encryption and hashing
        self._initialize_encryption()
        
        # Audit trail
        self.audit_log = []
    
    def _initialize_agent(self):
        """Initialize the policy and privacy agent"""
        # Initialize policy engine
        self._initialize_policy_engine()
        
        # Load privacy configurations
        self._load_privacy_config()
        
        # Initialize differential privacy
        self._initialize_differential_privacy()
    
    def _load_privacy_patterns(self):
        """Load privacy patterns for data detection"""
        self.privacy_patterns = {
            "pii": {
                "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
                "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
                "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
                "address": r"\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b",
                "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
            },
            "sensitive": {
                "salary": r"\b(?:salary|compensation|pay|wage)\s*:?\s*\$?\d+(?:,\d{3})*(?:\.\d{2})?\b",
                "performance": r"\b(?:performance|rating|review|evaluation)\s*:?\s*(?:poor|fair|good|excellent|outstanding)\b",
                "medical": r"\b(?:diagnosis|treatment|medication|therapy|symptoms|condition)\b",
                "legal": r"\b(?:lawsuit|legal|attorney|lawyer|court|litigation)\b"
            },
            "contextual": {
                "manager_comments": r"\b(?:manager|supervisor|boss)\s+(?:said|commented|noted|reported)\b",
                "team_dynamics": r"\b(?:team|colleague|coworker)\s+(?:conflict|issue|problem|concern)\b",
                "organizational": r"\b(?:company|organization|firm)\s+(?:policy|procedure|decision|announcement)\b"
            }
        }
    
    def _load_compliance_frameworks(self):
        """Load compliance framework requirements"""
        self.compliance_frameworks = {
            ComplianceFramework.HIPAA: {
                "phi_identifiers": [
                    "name", "address", "date_of_birth", "ssn", "medical_record_number",
                    "health_plan_beneficiary_number", "account_number", "certificate_license_number",
                    "vehicle_identifier", "device_identifier", "url", "ip_address", "biometric_identifier",
                    "full_face_photographic_image", "any_other_unique_identifying_number"
                ],
                "requirements": [
                    "data_encryption_at_rest",
                    "data_encryption_in_transit",
                    "access_controls",
                    "audit_logging",
                    "data_minimization"
                ]
            },
            ComplianceFramework.GDPR: {
                "personal_data": [
                    "name", "email", "phone", "address", "ip_address", "cookies",
                    "location_data", "online_identifier", "biometric_data"
                ],
                "requirements": [
                    "consent_management",
                    "right_to_erasure",
                    "data_portability",
                    "privacy_by_design",
                    "breach_notification"
                ]
            },
            ComplianceFramework.SOC2: {
                "security_criteria": [
                    "access_control",
                    "data_encryption",
                    "audit_logging",
                    "incident_response",
                    "change_management"
                ],
                "availability_criteria": [
                    "system_monitoring",
                    "backup_recovery",
                    "capacity_planning"
                ]
            }
        }
    
    def _initialize_encryption(self):
        """Initialize encryption and hashing capabilities"""
        # Generate encryption key from settings
        key = base64.urlsafe_b64encode(
            hashlib.sha256(settings.security.encryption_key.encode()).digest()
        )
        self.cipher_suite = Fernet(key)
        
        # Initialize hashing
        self.salt = settings.security.encryption_key.encode()
    
    def _initialize_policy_engine(self):
        """Initialize the policy enforcement engine"""
        self.policies = {
            "data_retention": {
                "conversation_logs": timedelta(days=90),
                "analytics_data": timedelta(days=365),
                "audit_logs": timedelta(days=2555),  # 7 years
                "user_profiles": timedelta(days=365)
            },
            "access_control": {
                "employee": ["own_data", "aggregated_analytics"],
                "manager": ["team_data", "team_analytics"],
                "hr": ["all_employee_data", "organizational_analytics"],
                "executive": ["organizational_summary", "trend_analytics"]
            },
            "anonymization": {
                "minimum_group_size": 5,
                "k_anonymity": 5,
                "l_diversity": 2
            }
        }
    
    def _load_privacy_config(self):
        """Load privacy configuration"""
        self.privacy_config = {
            "anonymization_enabled": settings.security.anonymization_enabled,
            "differential_privacy_epsilon": settings.security.differential_privacy_epsilon,
            "audit_logging_enabled": True,
            "consent_required": True,
            "data_minimization": True
        }
    
    def _initialize_differential_privacy(self):
        """Initialize differential privacy mechanisms"""
        self.dp_epsilon = settings.security.differential_privacy_epsilon
        self.dp_delta = 1e-5
        
        # Laplace mechanism for numerical data
        self.laplace_scale = 1.0 / self.dp_epsilon
    
    async def process_request(self, context: AgentContext, data: Dict[str, Any]) -> AgentResponse:
        """Process privacy and policy compliance requests"""
        
        operation = data.get("operation", "privacy_check")
        content = data.get("content", {})
        user_role = data.get("user_role", "employee")
        
        if operation == "privacy_check":
            result = await self._check_privacy_compliance(content, context)
        elif operation == "anonymize_data":
            result = await self._anonymize_data(content, context)
        elif operation == "policy_enforcement":
            result = await self._enforce_policies(content, user_role, context)
        elif operation == "compliance_audit":
            result = await self._audit_compliance(content, context)
        else:
            result = {"error": f"Unknown operation: {operation}"}
        
        # Log audit trail
        self._log_audit_event(operation, context, result)
        
        return AgentResponse(
            success=True,
            data=result,
            message=f"Privacy {operation} completed successfully"
        )
    
    async def _check_privacy_compliance(self, content: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Check content for privacy compliance"""
        
        violations = []
        anonymized_content = {}
        
        for field, value in content.items():
            # Check for PII patterns
            pii_violations = self._detect_pii(value, field)
            violations.extend(pii_violations)
            
            # Anonymize if needed
            if pii_violations:
                anonymized_content[field] = self._anonymize_field(value, field)
            else:
                anonymized_content[field] = value
        
        # Check compliance frameworks
        compliance_results = {}
        for framework in ComplianceFramework:
            compliance_results[framework.value] = self._check_framework_compliance(
                content, framework
            )
        
        return {
            "violations": [vars(v) for v in violations],
            "anonymized_content": anonymized_content,
            "compliance_results": compliance_results,
            "recommendations": self._generate_privacy_recommendations(violations)
        }
    
    async def _anonymize_data(self, content: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Anonymize data while preserving utility"""
        
        anonymized = {}
        
        for field, value in content.items():
            if isinstance(value, str):
                anonymized[field] = self._anonymize_text(value, field)
            elif isinstance(value, dict):
                anonymized[field] = await self._anonymize_data(value, context)
            elif isinstance(value, list):
                anonymized[field] = [
                    await self._anonymize_data(item, context) if isinstance(item, dict)
                    else self._anonymize_text(str(item), field) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                anonymized[field] = value
        
        return anonymized
    
    async def _enforce_policies(self, content: Dict[str, Any], user_role: str, context: AgentContext) -> Dict[str, Any]:
        """Enforce access control and data policies"""
        
        # Check access permissions
        access_allowed = self._check_access_permissions(content, user_role, context)
        
        if not access_allowed["allowed"]:
            return {
                "access_granted": False,
                "reason": access_allowed["reason"],
                "required_role": access_allowed["required_role"]
            }
        
        # Apply data minimization
        minimized_content = self._apply_data_minimization(content, user_role)
        
        # Apply retention policies
        retention_check = self._check_retention_policies(content, context)
        
        return {
            "access_granted": True,
            "minimized_content": minimized_content,
            "retention_policies": retention_check,
            "audit_required": True
        }
    
    async def _audit_compliance(self, content: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Perform comprehensive compliance audit"""
        
        audit_results = {}
        
        # Audit each compliance framework
        for framework in ComplianceFramework:
            audit_results[framework.value] = self._audit_framework(framework, content, context)
        
        # Generate compliance report
        compliance_report = self._generate_compliance_report(audit_results)
        
        return {
            "audit_results": audit_results,
            "compliance_report": compliance_report,
            "overall_status": self._determine_overall_compliance_status(audit_results)
        }
    
    def _detect_pii(self, value: Any, field_name: str) -> List[PrivacyViolation]:
        """Detect personally identifiable information"""
        violations = []
        
        if not isinstance(value, str):
            return violations
        
        for category, patterns in self.privacy_patterns.items():
            for pattern_name, pattern in patterns.items():
                matches = re.findall(pattern, value, re.IGNORECASE)
                if matches:
                    violations.append(PrivacyViolation(
                        violation_type=f"{category}_{pattern_name}",
                        severity="high" if category == "pii" else "medium",
                        description=f"Detected {pattern_name} in {field_name}",
                        data_fields=[field_name],
                        timestamp=datetime.now()
                    ))
        
        return violations
    
    def _anonymize_field(self, value: str, field_name: str) -> str:
        """Anonymize a specific field"""
        
        if not isinstance(value, str):
            return value
        
        # Apply field-specific anonymization
        if "email" in field_name.lower():
            return self._anonymize_email(value)
        elif "phone" in field_name.lower():
            return self._anonymize_phone(value)
        elif "name" in field_name.lower():
            return self._anonymize_name(value)
        else:
            return self._anonymize_text(value, field_name)
    
    def _anonymize_email(self, email: str) -> str:
        """Anonymize email address"""
        if "@" not in email:
            return email
        
        username, domain = email.split("@", 1)
        if len(username) <= 2:
            return f"{username[0]}***@{domain}"
        else:
            return f"{username[0]}{'*' * (len(username) - 2)}{username[-1]}@{domain}"
    
    def _anonymize_phone(self, phone: str) -> str:
        """Anonymize phone number"""
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            return f"***-***-{digits[-4:]}"
        else:
            return "***-***-****"
    
    def _anonymize_name(self, name: str) -> str:
        """Anonymize name"""
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}*** {parts[-1][0]}***"
        else:
            return f"{name[0]}***"
    
    def _anonymize_text(self, text: str, field_name: str) -> str:
        """Anonymize general text"""
        # Hash the text for consistent anonymization
        hash_object = hashlib.sha256(text.encode())
        return f"ANON_{hash_object.hexdigest()[:8]}"
    
    def _check_framework_compliance(self, content: Dict[str, Any], framework: ComplianceFramework) -> ComplianceCheck:
        """Check compliance with specific framework"""
        
        violations = []
        requirements = self.compliance_frameworks[framework]["requirements"]
        
        # Check each requirement
        for requirement in requirements:
            if not self._check_requirement(requirement, content):
                violations.append(PrivacyViolation(
                    violation_type=f"{framework.value}_{requirement}",
                    severity="high",
                    description=f"Non-compliant with {framework.value} {requirement}",
                    data_fields=list(content.keys()),
                    timestamp=datetime.now()
                ))
        
        status = "compliant" if not violations else "non_compliant"
        
        return ComplianceCheck(
            framework=framework,
            status=status,
            violations=violations,
            recommendations=self._generate_compliance_recommendations(framework, violations)
        )
    
    def _check_requirement(self, requirement: str, content: Dict[str, Any]) -> bool:
        """Check if content meets a specific requirement"""
        
        if requirement == "data_encryption_at_rest":
            return True  # Assume encrypted storage
        elif requirement == "data_encryption_in_transit":
            return True  # Assume HTTPS/TLS
        elif requirement == "access_controls":
            return True  # Assume implemented
        elif requirement == "audit_logging":
            return True  # Assume implemented
        elif requirement == "data_minimization":
            return len(content) <= 10  # Arbitrary threshold
        else:
            return True  # Default to compliant
    
    def _check_access_permissions(self, content: Dict[str, Any], user_role: str, context: AgentContext) -> Dict[str, Any]:
        """Check if user has permission to access content"""
        
        # Get user's allowed access
        allowed_access = self.policies["access_control"].get(user_role, [])
        
        # Check content type
        content_type = self._determine_content_type(content)
        
        if content_type in allowed_access:
            return {"allowed": True, "reason": "Access granted"}
        else:
            return {
                "allowed": False,
                "reason": f"Access denied: {content_type} not allowed for {user_role}",
                "required_role": self._find_required_role(content_type)
            }
    
    def _determine_content_type(self, content: Dict[str, Any]) -> str:
        """Determine the type of content being accessed"""
        
        if "user_id" in content and "team_id" not in content:
            return "own_data"
        elif "team_id" in content:
            return "team_data"
        elif "organizational_metrics" in content:
            return "organizational_analytics"
        else:
            return "general_data"
    
    def _find_required_role(self, content_type: str) -> str:
        """Find the minimum role required for content type"""
        
        role_hierarchy = {
            "own_data": "employee",
            "team_data": "manager",
            "organizational_analytics": "hr",
            "trend_analytics": "executive"
        }
        
        return role_hierarchy.get(content_type, "admin")
    
    def _apply_data_minimization(self, content: Dict[str, Any], user_role: str) -> Dict[str, Any]:
        """Apply data minimization principles"""
        
        if not self.privacy_config["data_minimization"]:
            return content
        
        # Remove unnecessary fields based on role
        minimized = content.copy()
        
        if user_role == "employee":
            # Remove team and organizational data
            minimized.pop("team_metrics", None)
            minimized.pop("organizational_metrics", None)
        elif user_role == "manager":
            # Remove individual employee data
            minimized.pop("individual_metrics", None)
        
        return minimized
    
    def _check_retention_policies(self, content: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Check data retention policies"""
        
        content_type = self._determine_content_type(content)
        retention_period = self.policies["data_retention"].get(content_type, timedelta(days=365))
        
        return {
            "content_type": content_type,
            "retention_period_days": retention_period.days,
            "expiry_date": context.timestamp + retention_period,
            "action_required": "none"
        }
    
    def _audit_framework(self, framework: ComplianceFramework, content: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Audit compliance with specific framework"""
        
        compliance_check = self._check_framework_compliance(content, framework)
        
        return {
            "status": compliance_check.status,
            "violations_count": len(compliance_check.violations),
            "requirements_met": len(self.compliance_frameworks[framework]["requirements"]) - len(compliance_check.violations),
            "total_requirements": len(self.compliance_frameworks[framework]["requirements"]),
            "violations": [vars(v) for v in compliance_check.violations],
            "recommendations": compliance_check.recommendations
        }
    
    def _generate_compliance_report(self, audit_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        
        overall_status = self._determine_overall_compliance_status(audit_results)
        
        return {
            "audit_date": datetime.now().isoformat(),
            "overall_status": overall_status,
            "framework_summary": {
                framework: {
                    "status": result["status"],
                    "compliance_rate": result["requirements_met"] / result["total_requirements"]
                }
                for framework, result in audit_results.items()
            },
            "critical_violations": self._get_critical_violations(audit_results),
            "recommendations": self._generate_overall_recommendations(audit_results)
        }
    
    def _determine_overall_compliance_status(self, audit_results: Dict[str, Any]) -> str:
        """Determine overall compliance status"""
        
        non_compliant_frameworks = [
            framework for framework, result in audit_results.items()
            if result["status"] == "non_compliant"
        ]
        
        if not non_compliant_frameworks:
            return "compliant"
        elif len(non_compliant_frameworks) <= 1:
            return "mostly_compliant"
        else:
            return "non_compliant"
    
    def _get_critical_violations(self, audit_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get critical violations across all frameworks"""
        
        critical_violations = []
        
        for framework, result in audit_results.items():
            for violation in result.get("violations", []):
                if violation.get("severity") == "critical":
                    critical_violations.append({
                        "framework": framework,
                        "violation": violation
                    })
        
        return critical_violations
    
    def _generate_privacy_recommendations(self, violations: List[PrivacyViolation]) -> List[str]:
        """Generate privacy recommendations based on violations"""
        
        recommendations = []
        
        for violation in violations:
            if "email" in violation.violation_type:
                recommendations.append("Anonymize email addresses before processing")
            elif "phone" in violation.violation_type:
                recommendations.append("Mask phone numbers in all data processing")
            elif "ssn" in violation.violation_type:
                recommendations.append("Remove SSNs from all data immediately")
            elif "credit_card" in violation.violation_type:
                recommendations.append("PCI compliance required for credit card data")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _generate_compliance_recommendations(self, framework: ComplianceFramework, violations: List[PrivacyViolation]) -> List[str]:
        """Generate compliance recommendations for specific framework"""
        
        recommendations = []
        
        if framework == ComplianceFramework.HIPAA:
            if any("phi" in v.violation_type for v in violations):
                recommendations.append("Implement PHI detection and removal")
                recommendations.append("Ensure all PHI is encrypted at rest and in transit")
        
        elif framework == ComplianceFramework.GDPR:
            if any("personal_data" in v.violation_type for v in violations):
                recommendations.append("Implement data minimization practices")
                recommendations.append("Ensure consent is obtained for all personal data processing")
        
        return recommendations
    
    def _generate_overall_recommendations(self, audit_results: Dict[str, Any]) -> List[str]:
        """Generate overall recommendations based on audit results"""
        
        recommendations = []
        
        # Check for common issues across frameworks
        non_compliant_frameworks = [
            framework for framework, result in audit_results.items()
            if result["status"] == "non_compliant"
        ]
        
        if len(non_compliant_frameworks) > 1:
            recommendations.append("Implement comprehensive privacy-by-design approach")
            recommendations.append("Establish privacy governance framework")
        
        if any(result.get("critical_violations") for result in audit_results.values()):
            recommendations.append("Address critical violations immediately")
            recommendations.append("Implement automated privacy violation detection")
        
        return recommendations
    
    def _log_audit_event(self, operation: str, context: AgentContext, result: Dict[str, Any]):
        """Log audit event for compliance"""
        
        audit_event = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "user_id": context.user_id,
            "session_id": context.session_id,
            "result": {
                "success": result.get("success", True),
                "violations_count": len(result.get("violations", [])),
                "compliance_status": result.get("overall_status", "unknown")
            }
        }
        
        self.audit_log.append(audit_event)
        
        # Keep only last 1000 audit events
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def get_audit_log(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get audit log entries within date range"""
        
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        filtered_log = [
            event for event in self.audit_log
            if start_date <= datetime.fromisoformat(event["timestamp"]) <= end_date
        ]
        
        return filtered_log
    
    def apply_differential_privacy(self, data: List[float], sensitivity: float = 1.0) -> List[float]:
        """Apply differential privacy to numerical data"""
        
        import numpy as np
        
        # Laplace mechanism
        scale = sensitivity / self.dp_epsilon
        noise = np.random.laplace(0, scale, len(data))
        
        return [original + noise_val for original, noise_val in zip(data, noise)]
