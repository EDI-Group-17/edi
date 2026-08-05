import re

PII_PATTERNS = [
    # AWS, OpenAI, GitHub API Keys
    (re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE), "[REDACTED: API_KEY]"),
    (re.compile(r"sk-(?:proj-)?[a-zA-Z0-9\-_]{16,}", re.IGNORECASE), "[REDACTED: API_KEY]"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}", re.IGNORECASE), "[REDACTED: API_KEY]"),
    
    # Credit Card Numbers (13 to 16 digits formatted with spaces/dashes)
    (re.compile(r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b"), "[REDACTED: CREDIT_CARD]"),
    
    # Indian National Identifiers (Aadhaar & PAN)
    (re.compile(r"\b[2-9]\d{3}[\s\-]?\d{4}[\s\-]?\d{4}\b"), "[REDACTED: AADHAAR_NUMBER]"),
    (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "[REDACTED: PAN_NUMBER]"),
]

SENSITIVE_KEYS = {"password", "passwd", "secret", "private_key", "secret_key", "api_key"}
