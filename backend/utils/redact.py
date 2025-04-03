import re

def redact_sensitive_info(text: str) -> str:
    """
    Redacts common forms of PII and PHI from user input using regex.
    """

    redacted = text

    # Email addresses
    redacted = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[REDACTED_EMAIL]', redacted)

    # Phone numbers (US-style)
    redacted = re.sub(r'\b(?:\+?1[-.\s]?)*?\d{3}?[-.\s]?\d{3}[-.\s]?\d{4}\b', '[REDACTED_PHONE]', redacted)

    # Dates (e.g., MM/DD/YYYY, YYYY-MM-DD)
    redacted = re.sub(r'\b(?:\d{1,2}[-/])?\d{1,2}[-/]\d{2,4}\b', '[REDACTED_DATE]', redacted)

    # Social Security Numbers
    redacted = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', redacted)

    # Names (very basic pattern — can be improved with NLP)
    redacted = re.sub(r'\b([A-Z][a-z]{2,}\s[A-Z][a-z]{2,})\b', '[REDACTED_NAME]', redacted)

    # Custom keyword redaction (e.g., patient, provider, location)
    keywords = ['hospital', 'clinic', 'address', 'insurance', 'dob', 'provider', 'patient']
    for word in keywords:
        redacted = re.sub(rf'\b{word}\b', '[REDACTED]', redacted, flags=re.IGNORECASE)

    return redacted
