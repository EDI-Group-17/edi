import re
from typing import Any, Tuple

DANGEROUS_COMMAND_REGEX = re.compile(
    r"\b(?:sudo|chmod|chown|iptables|mkfs|dd)\b|(?:curl|wget)\s+.*?\|\s*(?:sh|bash|zsh|python|perl)",
    re.IGNORECASE
)

SYSTEM_DIRECTORY_REGEX = re.compile(
    r"(?:^|[\s\"'/])(?:/etc/|/sys/|/proc/|/var/run/|/boot/|/dev/)",
    re.IGNORECASE
)

def evaluate_argument_heuristics(obj: Any) -> Tuple[bool, str]:
    if isinstance(obj, str):
        if DANGEROUS_COMMAND_REGEX.search(obj):
            return True, "HEURISTIC_DANGEROUS_COMMAND: Privileged/system command signature detected in arguments"
        if SYSTEM_DIRECTORY_REGEX.search(obj):
            return True, "HEURISTIC_SYSTEM_DIRECTORY_ACCESS: Privileged system directory access detected in arguments"
    elif isinstance(obj, dict):
        for val in obj.values():
            detected, reason = evaluate_argument_heuristics(val)
            if detected:
                return True, reason
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            detected, reason = evaluate_argument_heuristics(item)
            if detected:
                return True, reason
    return False, ""
