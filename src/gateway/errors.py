from typing import Any

def build_jsonrpc_error(req_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    error_frame = {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": code,
            "message": message
        }
    }
    if data is not None:
        error_frame["error"]["data"] = data
    return error_frame

def build_hitl_pending_error(req_id: Any, reason: str) -> dict[str, Any]:
    return build_jsonrpc_error(
        req_id=req_id,
        code=-32001,
        message="HITL Approval Required: Request paused for security review",
        data={"reason": reason, "status": "PENDING_APPROVAL"}
    )

def build_injection_blocked_error(req_id: Any, reason: str) -> dict[str, Any]:
    return build_jsonrpc_error(
        req_id=req_id,
        code=-32002,
        message="Injection Vector Intercepted: Request blocked by AgentShield",
        data={"reason": reason, "status": "BLOCKED"}
    )

def build_rate_limit_error(req_id: Any, reason: str) -> dict[str, Any]:
    return build_jsonrpc_error(
        req_id=req_id,
        code=-32003,
        message=f"Rate Limit Exceeded: {reason}",
        data={"status": "RATE_LIMITED"}
    )

def build_loop_quarantine_error(req_id: Any, reason: str) -> dict[str, Any]:
    return build_jsonrpc_error(
        req_id=req_id,
        code=-32004,
        message=f"Execution Loop Quarantine: {reason}",
        data={"status": "QUARANTINED"}
    )
