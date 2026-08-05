from typing import Any
from src.sanitizer.patterns import PII_PATTERNS, SENSITIVE_KEYS

def _sanitize_string(text: str) -> str:
    sanitized = text
    for pattern, replacement in PII_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized

def sanitize_payload(payload: Any) -> Any:
    if isinstance(payload, str):
        return _sanitize_string(payload)
    elif isinstance(payload, dict):
        sanitized_dict = {}
        for key, val in payload.items():
            sanitized_key = _sanitize_string(str(key))
            if str(key).lower() in SENSITIVE_KEYS:
                sanitized_dict[sanitized_key] = "[REDACTED: SECRET]"
            else:
                sanitized_dict[sanitized_key] = sanitize_payload(val)
        return sanitized_dict
    elif isinstance(payload, tuple):
        return tuple(sanitize_payload(item) for item in payload)
    elif isinstance(payload, set):
        return {sanitize_payload(item) for item in payload}
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    return payload
