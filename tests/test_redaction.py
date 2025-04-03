import pytest
from backend.utils.redact import redact_sensitive_info

def test_redact_email():
    text = "My email is john.doe@example.com"
    result = redact_sensitive_info(text)
    assert "[REDACTED_EMAIL]" in result

def test_redact_phone():
    text = "Call me at 555-123-4567 or (555) 123-4567."
    result = redact_sensitive_info(text)
    assert result.count("[REDACTED_PHONE]") == 2

def test_redact_date():
    text = "My appointment is on 04/15/2023 and another on 2024-01-01"
    result = redact_sensitive_info(text)
    assert result.count("[REDACTED_DATE]") == 2

def test_redact_ssn():
    text = "My SSN is 123-45-6789"
    result = redact_sensitive_info(text)
    assert "[REDACTED_SSN]" in result

def test_redact_name():
    text = "I spoke to Sarah Connor about my concerns."
    result = redact_sensitive_info(text)
    assert "[REDACTED_NAME]" in result

def test_redact_keywords():
    text = "The patient visited the clinic and spoke to the provider at the hospital."
    result = redact_sensitive_info(text)
    for word in ["[REDACTED]"] * 3:
        assert word in result
