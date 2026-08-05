import re
from typing import Any, Tuple
from src.core.config import settings

INJECTION_PATTERNS = [
    (r"\.\./|\.\.\\", "PATH_TRAVERSAL: Directory traversal pattern detected"),
    (r"rm\s+-rf|;\s*cat\s+/etc|;\s*drop\s+table", "COMMAND_INJECTION: Harmful shell command pattern"),
    (r"\$\(.*?\)|`.*?`|&&\s*\w+", "COMMAND_INJECTION: Subshell execution or command chaining pattern"),
    (r"<system_override>|ignore\s+(?:all\s+)?previous\s+instructions|developer\s+mode|do\s+anything\s+now", "PROMPT_INJECTION: System override / DAN jailbreak tag detected"),
    (r"'\s*UNION\s+SELECT|'\s*OR\s+'1'='1|;\s*SELECT\s+.*?\s+FROM", "SQL_INJECTION: SQL injection signature detected"),
    (r"!\[.*?\]\(https?://[^\s]+\)", "DATA_EXFILTRATION: Markdown image exfiltration pattern detected")
]

COMPILED_PATTERNS = [(re.compile(pat, re.IGNORECASE), msg) for pat, msg in INJECTION_PATTERNS]

def _inspect_obj(obj: Any) -> Tuple[bool, str]:
    if isinstance(obj, str):
        for pattern, msg in COMPILED_PATTERNS:
            if pattern.search(obj):
                return True, msg
    elif isinstance(obj, dict):
        for val in obj.values():
            detected, msg = _inspect_obj(val)
            if detected:
                return True, msg
    elif isinstance(obj, list):
        for item in obj:
            detected, msg = _inspect_obj(item)
            if detected:
                return True, msg
    return False, ""

def detect_injection_vectors(payload: Any) -> Tuple[bool, str]:
    return _inspect_obj(payload)

def detect_restricted_paths(obj: Any) -> Tuple[bool, str]:
    if isinstance(obj, str):
        for path in settings.RESTRICTED_PATHS:
            if path in obj:
                return True, f"SENSITIVE_PATH_DETECTED: Match found for restricted path '{path}'"
    elif isinstance(obj, dict):
        for val in obj.values():
            detected, msg = detect_restricted_paths(val)
            if detected:
                return True, msg
    elif isinstance(obj, list):
        for item in obj:
            detected, msg = detect_restricted_paths(item)
            if detected:
                return True, msg
    return False, ""
