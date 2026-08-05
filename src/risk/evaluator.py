from typing import Any, Tuple
from src.core.config import settings
from src.risk.detectors import detect_injection_vectors, detect_restricted_paths
from src.risk.heuristics import evaluate_argument_heuristics

def evaluate_mcp_risk(payload: dict[str, Any]) -> Tuple[str, str]:
    # 1. Check for injection vectors in payload
    detected, injection_reason = detect_injection_vectors(payload)
    if detected:
        return "HIGH", f"PROMPT_INJECTION_DETECTED: {injection_reason}"

    # 2. Check for restricted sensitive paths in parameters
    path_detected, path_reason = detect_restricted_paths(payload)
    if path_detected:
        return "HIGH", path_reason

    # 3. Check tool argument heuristics (dangerous commands & system folders)
    heuristic_detected, heuristic_reason = evaluate_argument_heuristics(payload)
    if heuristic_detected:
        return "HIGH", heuristic_reason

    method = payload.get("method") or ""
    params = payload.get("params") or {}
    if not isinstance(params, dict):
        params = {}

    # 4. Check read-only methods
    if method in {"resources/read", "prompts/get", "tools/list"}:
        return "LOW", "READ_ONLY_OPERATION"

    # 5. Check tool invocations
    if method == "tools/call":
        tool_name = params.get("name", "")
        if tool_name in settings.HIGH_RISK_TOOLS:
            if tool_name in {"fs.write_file", "fs.delete_file", "github.delete_repo", "db.execute_sql", "shell.execute", "exec"}:
                return "HIGH", f"SENSITIVE_TOOL_MUTATION: Tool '{tool_name}' requires HITL approval"
            return "HIGH", f"SENSITIVE_TOOL_CALL: Configured sensitive tool '{tool_name}'"
        return "MEDIUM", f"STANDARD_TOOL_EXECUTION: Tool '{tool_name}'"

    return "MEDIUM", "DEFAULT_FAIL_SAFE_MEDIUM_RISK"
