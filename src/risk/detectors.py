import re
from typing import Any, Tuple
from src.core.config import settings

INJECTION_PATTERNS = [
    # Path & File System Traversal
    (r"\.\./|\.\.\\", "PATH_TRAVERSAL: Directory traversal pattern detected"),
    (r"/etc/passwd|/etc/shadow|/root/\.|~/\.", "PATH_TRAVERSAL: Attempt to read sensitive OS files"),
    
    # Command & Shell Injection
    (r"rm\s+-rf|;\s*cat\s+/etc|;\s*drop\s+table", "COMMAND_INJECTION: Harmful shell command pattern"),
    (r"\$\(.*?\)|`.*?`|&&\s*\w+|\|\s*sh|\|\s*bash", "COMMAND_INJECTION: Subshell execution or command chaining pattern"),
    (r">\s*/dev/null|wget\s+http|curl\s+http", "COMMAND_INJECTION: Reverse shell or remote download execution"),
    
    # Prompt Injection & Jailbreaks (Highly Generalized)
    (r"<system_override>|<instructions>|<system>|\[system\]", "PROMPT_INJECTION: System tag spoofing detected"),
    (r"ignore\s+(?:all\s+)?(?:previous\s+)?(?:instructions|rules|guidelines|directives)", "PROMPT_INJECTION: Rule suppression jailbreak detected"),
    (r"forget\s+(?:all\s+)?(?:previous\s+)?(?:instructions|rules|guidelines)", "PROMPT_INJECTION: Amnesia jailbreak detected"),
    (r"developer\s+mode|do\s+anything\s+now|DAN|unfiltered\s+AI", "PROMPT_INJECTION: DAN/Persona jailbreak detected"),
    (r"you\s+are\s+now\s+a\s+(?:bad|unrestricted|malicious|evil|hacker)\s+(?:bot|AI|assistant)", "PROMPT_INJECTION: Persona adoption jailbreak detected"),
    (r"bypass\s+safety|disable\s+security|turn\s+off\s+filters", "PROMPT_INJECTION: Security filter bypass request"),
    (r"print\s+your\s+(?:initial|core|system)\s+prompt", "PROMPT_INJECTION: System prompt extraction attempt"),
    
    # SQL Injection
    (r"'\s*UNION\s+SELECT|'\s*OR\s+'1'='1|;\s*SELECT\s+.*?\s+FROM|'\s*OR\s+1=1", "SQL_INJECTION: SQL injection signature detected"),
    (r";\s*DROP\s+TABLE|;\s*DELETE\s+FROM|;\s*TRUNCATE\s+TABLE", "SQL_INJECTION: Destructive SQL query injection"),
    
    # Exfiltration
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
