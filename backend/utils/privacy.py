"""
Privacy Manager - Data privacy controls and anonymization
"""

import hashlib
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class PrivacyManager:
    """
    Manages data privacy controls and anonymization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.anonymization_enabled = True
        self.data_retention_days = 365
    
    def apply_privacy_controls(self, data: Any, user_id: str) -> Any:
        """
        Apply privacy controls to data
        """
        try:
            if isinstance(data, dict):
                return self._anonymize_dict(data, user_id)
            elif isinstance(data, list):
                return [self._anonymize_dict(item, user_id) if isinstance(item, dict) else item for item in data]
            else:
                return data
        except Exception as e:
            self.logger.error(f"Failed to apply privacy controls: {e}")
            return data
    
    def _anonymize_dict(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Anonymize sensitive data in a dictionary
        """
        if not self.anonymization_enabled:
            return data
        
        anonymized = {}
        for key, value in data.items():
            if self._is_sensitive_field(key):
                anonymized[key] = self._anonymize_value(value, user_id)
            elif isinstance(value, dict):
                anonymized[key] = self._anonymize_dict(value, user_id)
            elif isinstance(value, list):
                anonymized[key] = [self._anonymize_dict(item, user_id) if isinstance(item, dict) else item for item in value]
            else:
                anonymized[key] = value
        
        return anonymized
    
    def _is_sensitive_field(self, field_name: str) -> bool:
        """
        Check if a field contains sensitive data
        """
        sensitive_patterns = [
            'email', 'phone', 'address', 'ssn', 'password', 'token',
            'credit_card', 'bank_account', 'ip_address', 'user_agent',
            'first_name', 'last_name', 'name', 'description'
        ]
        
        field_lower = field_name.lower()
        return any(pattern in field_lower for pattern in sensitive_patterns)
    
    def _anonymize_value(self, value: Any, user_id: str) -> str:
        """
        Anonymize a sensitive value
        """
        if not value:
            return value
        
        # Create a hash based on user_id and value
        hash_input = f"{user_id}:{str(value)}"
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
        
        if isinstance(value, str):
            if '@' in value:  # Email
                parts = value.split('@')
                return f"{hash_value}@{parts[1]}" if len(parts) > 1 else f"{hash_value}@example.com"
            elif re.match(r'^\d{10,}$', value):  # Phone number
                return f"+1-{hash_value[:3]}-{hash_value[3:6]}-{hash_value[6:8]}"
            else:
                return f"[ANONYMIZED_{hash_value}]"
        else:
            return f"[ANONYMIZED_{hash_value}]"
    
    def filter_entries(self, entries: List[Dict[str, Any]], user_id: str) -> List[Dict[str, Any]]:
        """
        Filter entries based on privacy settings
        """
        try:
            filtered_entries = []
            cutoff_date = datetime.utcnow() - timedelta(days=self.data_retention_days)
            
            for entry in entries:
                # Check data retention
                if 'created_at' in entry:
                    entry_date = datetime.fromisoformat(entry['created_at'].replace('Z', '+00:00'))
                    if entry_date < cutoff_date:
                        continue
                
                # Apply privacy controls
                filtered_entry = self.apply_privacy_controls(entry, user_id)
                filtered_entries.append(filtered_entry)
            
            return filtered_entries
        except Exception as e:
            self.logger.error(f"Failed to filter entries: {e}")
            return entries
    
    def filter_conversations(self, conversations: List[Dict[str, Any]], user_id: str) -> List[Dict[str, Any]]:
        """
        Filter conversations based on privacy settings
        """
        try:
            filtered_conversations = []
            cutoff_date = datetime.utcnow() - timedelta(days=self.data_retention_days)
            
            for conv in conversations:
                # Check data retention
                if 'created_at' in conv:
                    conv_date = datetime.fromisoformat(conv['created_at'].replace('Z', '+00:00'))
                    if conv_date < cutoff_date:
                        continue
                
                # Apply privacy controls
                filtered_conv = self.apply_privacy_controls(conv, user_id)
                filtered_conversations.append(filtered_conv)
            
            return filtered_conversations
        except Exception as e:
            self.logger.error(f"Failed to filter conversations: {e}")
            return conversations
    
    def mask_personal_data(self, text: str) -> str:
        """
        Mask personal data in text
        """
        if not text:
            return text
        
        # Mask email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Mask phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        
        # Mask credit card numbers
        text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', text)
        
        # Mask SSN
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        
        return text
    
    def get_data_retention_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get data retention information for a user
        """
        return {
            "retention_days": self.data_retention_days,
            "cutoff_date": (datetime.utcnow() - timedelta(days=self.data_retention_days)).isoformat(),
            "anonymization_enabled": self.anonymization_enabled
        }
    
    def validate_privacy_consent(self, user_id: str, consent_data: Dict[str, Any]) -> bool:
        """
        Validate privacy consent
        """
        try:
            required_fields = ['consent_given', 'consent_version', 'timestamp']
            
            for field in required_fields:
                if field not in consent_data:
                    self.logger.warning(f"Missing required consent field: {field}")
                    return False
            
            if not consent_data['consent_given']:
                return False
            
            # Check if consent is recent (within last year)
            consent_date = datetime.fromisoformat(consent_data['timestamp'].replace('Z', '+00:00'))
            if consent_date < datetime.utcnow() - timedelta(days=365):
                self.logger.warning(f"Consent is too old for user {user_id}")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to validate privacy consent: {e}")
            return False
    
    def log_privacy_event(self, user_id: str, event_type: str, details: Dict[str, Any]) -> None:
        """
        Log privacy-related events
        """
        try:
            log_entry = {
                "user_id": user_id,
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "details": details
            }
            
            self.logger.info(f"Privacy event: {log_entry}")
        except Exception as e:
            self.logger.error(f"Failed to log privacy event: {e}")
