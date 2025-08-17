import re
import hashlib
import base64
import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass
from enum import Enum

from config.settings import settings

logger = logging.getLogger(__name__)

class DataType(Enum):
    """Types of data that can be anonymized."""
    TEXT = "text"
    EMAIL = "email"
    PHONE = "phone"
    NAME = "name"
    ADDRESS = "address"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    IP_ADDRESS = "ip_address"
    USER_ID = "user_id"
    TIMESTAMP = "timestamp"
    NUMERIC = "numeric"

class AnonymizationMethod(Enum):
    """Methods for anonymizing data."""
    HASH = "hash"
    MASK = "mask"
    GENERALIZE = "generalize"
    PERTURB = "perturb"
    SUPPRESS = "suppress"
    ENCRYPT = "encrypt"

@dataclass
class PIIPattern:
    """Pattern for detecting PII."""
    name: str
    pattern: str
    data_type: DataType
    confidence: float
    description: str

@dataclass
class AnonymizationRule:
    """Rule for anonymizing data."""
    field_name: str
    data_type: DataType
    method: AnonymizationMethod
    parameters: Dict[str, Any]
    required: bool = True

class DataAnonymizer:
    """Data anonymization and privacy protection."""
    
    def __init__(self):
        self.pii_patterns = self._load_pii_patterns()
        self.anonymization_rules = self._load_anonymization_rules()
        self.hash_salt = settings.security.hash_salt
        
        # Differential privacy parameters
        self.epsilon = 1.0  # Privacy budget
        self.delta = 1e-5   # Privacy parameter
    
    def _load_pii_patterns(self) -> List[PIIPattern]:
        """Load PII detection patterns."""
        return [
            # Email patterns
            PIIPattern(
                name="email",
                pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                data_type=DataType.EMAIL,
                confidence=0.95,
                description="Email address"
            ),
            
            # Phone number patterns
            PIIPattern(
                name="phone_us",
                pattern=r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
                data_type=DataType.PHONE,
                confidence=0.90,
                description="US phone number"
            ),
            
            # Name patterns
            PIIPattern(
                name="full_name",
                pattern=r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',
                data_type=DataType.NAME,
                confidence=0.80,
                description="Full name"
            ),
            
            # SSN patterns
            PIIPattern(
                name="ssn",
                pattern=r'\b\d{3}-\d{2}-\d{4}\b',
                data_type=DataType.SSN,
                confidence=0.95,
                description="Social Security Number"
            ),
            
            # Credit card patterns
            PIIPattern(
                name="credit_card",
                pattern=r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
                data_type=DataType.CREDIT_CARD,
                confidence=0.85,
                description="Credit card number"
            ),
            
            # IP address patterns
            PIIPattern(
                name="ip_address",
                pattern=r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
                data_type=DataType.IP_ADDRESS,
                confidence=0.90,
                description="IP address"
            ),
            
            # Address patterns
            PIIPattern(
                name="street_address",
                pattern=r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b',
                data_type=DataType.ADDRESS,
                confidence=0.75,
                description="Street address"
            )
        ]
    
    def _load_anonymization_rules(self) -> List[AnonymizationRule]:
        """Load anonymization rules."""
        return [
            # User identification
            AnonymizationRule(
                field_name="user_id",
                data_type=DataType.USER_ID,
                method=AnonymizationMethod.HASH,
                parameters={"algorithm": "sha256", "salt": self.hash_salt}
            ),
            
            AnonymizationRule(
                field_name="email",
                data_type=DataType.EMAIL,
                method=AnonymizationMethod.MASK,
                parameters={"mask_char": "*", "preserve_domain": True}
            ),
            
            AnonymizationRule(
                field_name="phone",
                data_type=DataType.PHONE,
                method=AnonymizationMethod.MASK,
                parameters={"mask_char": "*", "preserve_last_4": True}
            ),
            
            AnonymizationRule(
                field_name="name",
                data_type=DataType.NAME,
                method=AnonymizationMethod.GENERALIZE,
                parameters={"level": "first_initial"}
            ),
            
            AnonymizationRule(
                field_name="address",
                data_type=DataType.ADDRESS,
                method=AnonymizationMethod.SUPPRESS,
                parameters={}
            ),
            
            AnonymizationRule(
                field_name="ssn",
                data_type=DataType.SSN,
                method=AnonymizationMethod.MASK,
                parameters={"mask_char": "*", "preserve_last_4": True}
            ),
            
            AnonymizationRule(
                field_name="credit_card",
                data_type=DataType.CREDIT_CARD,
                method=AnonymizationMethod.MASK,
                parameters={"mask_char": "*", "preserve_last_4": True}
            ),
            
            AnonymizationRule(
                field_name="ip_address",
                data_type=DataType.IP_ADDRESS,
                method=AnonymizationMethod.GENERALIZE,
                parameters={"level": "subnet"}
            ),
            
            AnonymizationRule(
                field_name="timestamp",
                data_type=DataType.TIMESTAMP,
                method=AnonymizationMethod.GENERALIZE,
                parameters={"level": "hour"}
            ),
            
            AnonymizationRule(
                field_name="salary",
                data_type=DataType.NUMERIC,
                method=AnonymizationMethod.PERTURB,
                parameters={"noise_scale": 0.1}
            )
        ]
    
    def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        """Detect PII in text."""
        detected_pii = []
        
        for pattern in self.pii_patterns:
            matches = re.finditer(pattern.pattern, text, re.IGNORECASE)
            for match in matches:
                detected_pii.append({
                    "type": pattern.data_type.value,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": pattern.confidence,
                    "description": pattern.description
                })
        
        return detected_pii
    
    def anonymize_text(self, text: str, preserve_context: bool = True) -> str:
        """Anonymize text while preserving context."""
        if not text:
            return text
        
        # Detect PII
        detected_pii = self.detect_pii(text)
        
        # Sort by start position (reverse order to avoid index shifting)
        detected_pii.sort(key=lambda x: x["start"], reverse=True)
        
        # Replace PII with anonymized versions
        anonymized_text = text
        for pii in detected_pii:
            anonymized_value = self._anonymize_value(
                pii["value"], 
                pii["type"], 
                preserve_context
            )
            anonymized_text = (
                anonymized_text[:pii["start"]] + 
                anonymized_value + 
                anonymized_text[pii["end"]:]
            )
        
        return anonymized_text
    
    def _anonymize_value(self, value: str, data_type: str, preserve_context: bool) -> str:
        """Anonymize a single value."""
        if data_type == DataType.EMAIL.value:
            return self._anonymize_email(value, preserve_context)
        elif data_type == DataType.PHONE.value:
            return self._anonymize_phone(value, preserve_context)
        elif data_type == DataType.NAME.value:
            return self._anonymize_name(value, preserve_context)
        elif data_type == DataType.SSN.value:
            return self._anonymize_ssn(value)
        elif data_type == DataType.CREDIT_CARD.value:
            return self._anonymize_credit_card(value)
        elif data_type == DataType.IP_ADDRESS.value:
            return self._anonymize_ip_address(value)
        elif data_type == DataType.ADDRESS.value:
            return "[ADDRESS REDACTED]"
        else:
            return self._hash_value(value)
    
    def _anonymize_email(self, email: str, preserve_context: bool) -> str:
        """Anonymize email address."""
        if "@" not in email:
            return self._hash_value(email)
        
        local_part, domain = email.split("@", 1)
        
        if preserve_context:
            # Keep first and last character of local part
            if len(local_part) <= 2:
                anonymized_local = "*"
            else:
                anonymized_local = local_part[0] + "*" * (len(local_part) - 2) + local_part[-1]
            
            return f"{anonymized_local}@{domain}"
        else:
            return f"***@{domain}"
    
    def _anonymize_phone(self, phone: str, preserve_context: bool) -> str:
        """Anonymize phone number."""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) >= 4:
            if preserve_context:
                # Keep last 4 digits
                return "*" * (len(digits) - 4) + digits[-4:]
            else:
                return "*" * len(digits)
        else:
            return "*" * len(digits)
    
    def _anonymize_name(self, name: str, preserve_context: bool) -> str:
        """Anonymize name."""
        parts = name.split()
        
        if preserve_context:
            # Keep first letter of each part
            anonymized_parts = []
            for part in parts:
                if len(part) > 1:
                    anonymized_parts.append(part[0] + "*" * (len(part) - 1))
                else:
                    anonymized_parts.append(part)
            return " ".join(anonymized_parts)
        else:
            return "[NAME REDACTED]"
    
    def _anonymize_ssn(self, ssn: str) -> str:
        """Anonymize SSN."""
        # Remove non-digits
        digits = re.sub(r'\D', '', ssn)
        
        if len(digits) == 9:
            return f"***-**-{digits[-4:]}"
        else:
            return "*" * len(digits)
    
    def _anonymize_credit_card(self, card: str) -> str:
        """Anonymize credit card number."""
        # Remove non-digits
        digits = re.sub(r'\D', '', card)
        
        if len(digits) >= 4:
            return "*" * (len(digits) - 4) + digits[-4:]
        else:
            return "*" * len(digits)
    
    def _anonymize_ip_address(self, ip: str) -> str:
        """Anonymize IP address."""
        parts = ip.split(".")
        
        if len(parts) == 4:
            # Keep first two octets, mask last two
            return f"{parts[0]}.{parts[1]}.*.*"
        else:
            return "*.*.*.*"
    
    def _hash_value(self, value: str) -> str:
        """Hash a value."""
        salted_value = value + self.hash_salt
        return hashlib.sha256(salted_value.encode()).hexdigest()[:16]
    
    def anonymize_data(self, data: Union[Dict, List], rules: Optional[List[AnonymizationRule]] = None) -> Union[Dict, List]:
        """Anonymize structured data."""
        if rules is None:
            rules = self.anonymization_rules
        
        if isinstance(data, list):
            return [self.anonymize_data(item, rules) for item in data]
        elif isinstance(data, dict):
            anonymized_data = {}
            
            for key, value in data.items():
                # Find matching rule
                rule = next((r for r in rules if r.field_name == key), None)
                
                if rule:
                    anonymized_data[key] = self._apply_anonymization_rule(value, rule)
                else:
                    # Check if value contains PII
                    if isinstance(value, str):
                        anonymized_data[key] = self.anonymize_text(value)
                    else:
                        anonymized_data[key] = value
            
            return anonymized_data
        else:
            return data
    
    def _apply_anonymization_rule(self, value: Any, rule: AnonymizationRule) -> Any:
        """Apply an anonymization rule to a value."""
        if value is None:
            return None
        
        if rule.method == AnonymizationMethod.HASH:
            return self._hash_value(str(value))
        
        elif rule.method == AnonymizationMethod.MASK:
            return self._mask_value(str(value), rule.parameters)
        
        elif rule.method == AnonymizationMethod.GENERALIZE:
            return self._generalize_value(value, rule.parameters)
        
        elif rule.method == AnonymizationMethod.PERTURB:
            return self._perturb_value(value, rule.parameters)
        
        elif rule.method == AnonymizationMethod.SUPPRESS:
            return None
        
        elif rule.method == AnonymizationMethod.ENCRYPT:
            return self._encrypt_value(str(value))
        
        else:
            return value
    
    def _mask_value(self, value: str, parameters: Dict[str, Any]) -> str:
        """Mask a value."""
        mask_char = parameters.get("mask_char", "*")
        preserve_domain = parameters.get("preserve_domain", False)
        preserve_last_4 = parameters.get("preserve_last_4", False)
        
        if preserve_domain and "@" in value:
            # Email masking
            local_part, domain = value.split("@", 1)
            if len(local_part) > 2:
                masked_local = local_part[0] + mask_char * (len(local_part) - 2) + local_part[-1]
            else:
                masked_local = mask_char * len(local_part)
            return f"{masked_local}@{domain}"
        
        elif preserve_last_4 and len(value) >= 4:
            # Keep last 4 characters
            return mask_char * (len(value) - 4) + value[-4:]
        
        else:
            # Full masking
            return mask_char * len(value)
    
    def _generalize_value(self, value: Any, parameters: Dict[str, Any]) -> Any:
        """Generalize a value."""
        level = parameters.get("level", "default")
        
        if isinstance(value, datetime):
            if level == "hour":
                return value.replace(minute=0, second=0, microsecond=0)
            elif level == "day":
                return value.replace(hour=0, minute=0, second=0, microsecond=0)
            elif level == "month":
                return value.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif level == "year":
                return value.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        elif isinstance(value, str):
            if level == "first_initial" and " " in value:
                # Keep first initial of each word
                parts = value.split()
                return " ".join(part[0] + "." for part in parts)
        
        return value
    
    def _perturb_value(self, value: Any, parameters: Dict[str, Any]) -> Any:
        """Perturb a numeric value with noise."""
        if not isinstance(value, (int, float)):
            return value
        
        noise_scale = parameters.get("noise_scale", 0.1)
        
        # Add Laplace noise for differential privacy
        noise = np.random.laplace(0, noise_scale * abs(value))
        perturbed_value = value + noise
        
        # Round to appropriate precision
        if isinstance(value, int):
            return int(round(perturbed_value))
        else:
            return round(perturbed_value, 2)
    
    def _encrypt_value(self, value: str) -> str:
        """Encrypt a value (placeholder for actual encryption)."""
        # In production, use proper encryption
        return f"ENCRYPTED_{self._hash_value(value)}"
    
    def apply_differential_privacy(self, data: List[float], sensitivity: float = 1.0) -> List[float]:
        """Apply differential privacy to a list of numeric values."""
        if not data:
            return data
        
        # Calculate noise scale based on privacy parameters
        noise_scale = sensitivity / self.epsilon
        
        # Add Laplace noise
        noise = np.random.laplace(0, noise_scale, len(data))
        perturbed_data = [d + n for d, n in zip(data, noise)]
        
        return perturbed_data
    
    def aggregate_with_privacy(self, data: List[Dict[str, Any]], aggregation_field: str, 
                             group_by: Optional[str] = None) -> Dict[str, Any]:
        """Aggregate data with differential privacy."""
        if not data:
            return {}
        
        if group_by:
            # Group by specified field
            groups = {}
            for item in data:
                group_key = item.get(group_by, "unknown")
                if group_key not in groups:
                    groups[group_key] = []
                groups[group_key].append(item.get(aggregation_field, 0))
            
            # Aggregate each group with privacy
            result = {}
            for group_key, values in groups.items():
                if values:
                    # Calculate statistics with noise
                    mean_val = np.mean(values)
                    count_val = len(values)
                    
                    # Add noise to statistics
                    noisy_mean = mean_val + np.random.laplace(0, 1.0 / self.epsilon)
                    noisy_count = count_val + np.random.laplace(0, 1.0 / self.epsilon)
                    
                    result[group_key] = {
                        "count": max(0, int(round(noisy_count))),
                        "mean": round(noisy_mean, 2),
                        "privacy_level": "differential"
                    }
            
            return result
        else:
            # Simple aggregation
            values = [item.get(aggregation_field, 0) for item in data]
            
            if values:
                mean_val = np.mean(values)
                count_val = len(values)
                
                # Add noise
                noisy_mean = mean_val + np.random.laplace(0, 1.0 / self.epsilon)
                noisy_count = count_val + np.random.laplace(0, 1.0 / self.epsilon)
                
                return {
                    "count": max(0, int(round(noisy_count))),
                    "mean": round(noisy_mean, 2),
                    "privacy_level": "differential"
                }
        
        return {}
    
    def create_anonymous_id(self, original_id: str, context: str = "") -> str:
        """Create an anonymous ID from an original ID."""
        salted_value = f"{original_id}:{context}:{self.hash_salt}"
        return hashlib.sha256(salted_value.encode()).hexdigest()[:16]
    
    def validate_privacy_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate privacy compliance of data."""
        compliance_report = {
            "compliant": True,
            "issues": [],
            "recommendations": []
        }
        
        # Check for PII in text fields
        for key, value in data.items():
            if isinstance(value, str):
                detected_pii = self.detect_pii(value)
                if detected_pii:
                    compliance_report["compliant"] = False
                    compliance_report["issues"].append({
                        "field": key,
                        "issue": "PII detected",
                        "pii_types": [pii["type"] for pii in detected_pii]
                    })
                    compliance_report["recommendations"].append(
                        f"Anonymize field '{key}' to remove PII"
                    )
        
        # Check for required anonymization
        for rule in self.anonymization_rules:
            if rule.required and rule.field_name in data:
                if not self._is_properly_anonymized(data[rule.field_name], rule):
                    compliance_report["compliant"] = False
                    compliance_report["issues"].append({
                        "field": rule.field_name,
                        "issue": "Not properly anonymized",
                        "required_method": rule.method.value
                    })
                    compliance_report["recommendations"].append(
                        f"Apply {rule.method.value} anonymization to field '{rule.field_name}'"
                    )
        
        return compliance_report
    
    def _is_properly_anonymized(self, value: Any, rule: AnonymizationRule) -> bool:
        """Check if a value is properly anonymized according to the rule."""
        if value is None:
            return rule.method == AnonymizationMethod.SUPPRESS
        
        if rule.method == AnonymizationMethod.HASH:
            # Check if it looks like a hash
            return isinstance(value, str) and len(value) >= 16 and all(c in '0123456789abcdef' for c in value.lower())
        
        elif rule.method == AnonymizationMethod.MASK:
            # Check if it contains mask characters
            return isinstance(value, str) and "*" in value
        
        elif rule.method == AnonymizationMethod.SUPPRESS:
            return value is None
        
        # For other methods, assume it's properly anonymized if it's not the original
        return True

# Global anonymizer instance
data_anonymizer = DataAnonymizer()

# Export commonly used functions and classes
__all__ = [
    'DataType',
    'AnonymizationMethod',
    'PIIPattern',
    'AnonymizationRule',
    'DataAnonymizer',
    'data_anonymizer'
]
