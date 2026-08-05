import asyncio
import hashlib
import json
import time
from typing import Any, Dict
from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.risk.evaluator import evaluate_mcp_risk
from src.gateway.errors import (
    build_hitl_pending_error,
    build_injection_blocked_error,
    build_rate_limit_error,
    build_loop_quarantine_error,
    build_jsonrpc_error
)
from src.gateway.mcp_client import forward_mcp_request
from src.hitl.manager import hitl_manager
from src.sanitizer.pii_engine import sanitize_payload
from src.ratelimit.limiter import rate_limiter
from src.ratelimit.loop_detector import loop_detector
from src.audit.logger import audit_logger

from src.api.websocket import ws_manager

router = APIRouter(prefix="/mcp/v1", tags=["Gateway Proxy"])

@router.post("/proxy")
async def handle_mcp_proxy(payload: Dict[str, Any], request: Request):
    start_time = time.time()
    req_id = payload.get("id")
    agent_id = request.headers.get("X-Agent-ID", request.client.host if request.client else "default_agent")
    method = payload.get("method") or ""
    params = payload.get("params") or {}
    tool_name = params.get("name") if method == "tools/call" else None
    arguments = params.get("arguments") or {}

    # Compute payload hash
    args_str = json.dumps(arguments, sort_keys=True)
    payload_hash = hashlib.sha256(args_str.encode()).hexdigest()

    decision = "APPROVED"
    risk_level = "LOW"

    # Helper to send response and log transaction in background
    def build_response(status_code: int, content: Dict[str, Any], final_decision: str, final_risk: str) -> JSONResponse:
        latency = (time.time() - start_time) * 1000.0
        asyncio.create_task(
            audit_logger.log_transaction(
                request_id=str(req_id),
                agent_id=agent_id,
                method=method,
                tool_name=tool_name,
                payload_hash=payload_hash,
                risk_level=final_risk,
                decision=final_decision,
                latency_ms=latency
            )
        )
        # Broadcast live event to WebSocket dashboard subscribers
        asyncio.create_task(
            ws_manager.broadcast({
                "type": "TRANSACTION",
                "request_id": str(req_id),
                "agent_id": agent_id,
                "method": method,
                "tool_name": tool_name,
                "risk_level": final_risk,
                "decision": final_decision,
                "latency_ms": round(latency, 2),
                "timestamp": time.time()
            })
        )
        return JSONResponse(status_code=status_code, content=content)

    # 1. Check Rate Limiter
    allowed, rate_reason = rate_limiter.check_rate_limit(agent_id)
    if not allowed:
        return build_response(
            status.HTTP_200_OK,
            build_rate_limit_error(req_id, rate_reason),
            "RATE_LIMITED",
            "LOW"
        )

    # 2. Check Loop Quarantine
    if method == "tools/call":
        quarantined, loop_reason = loop_detector.check_loop(agent_id, tool_name or "", arguments)
        if quarantined:
            return build_response(
                status.HTTP_200_OK,
                build_loop_quarantine_error(req_id, loop_reason),
                "QUARANTINED",
                "LOW"
            )

    # 3. Dynamic Risk Evaluation
    risk_level, reason = evaluate_mcp_risk(payload)
    if risk_level == "HIGH":
        if "PROMPT_INJECTION" in reason:
            return build_response(
                status.HTTP_200_OK,
                build_injection_blocked_error(req_id, reason),
                "BLOCKED",
                risk_level
            )
        
        decision, comment = await hitl_manager.register_and_wait(
            str(req_id), payload, timeout_seconds=settings.HITL_TIMEOUT_SECONDS
        )
        if decision != "APPROVED":
            error_msg = f"Security Action Denied by HITL Admin: {comment}" if decision == "DENIED" else comment
            return build_response(
                status.HTTP_200_OK,
                build_jsonrpc_error(req_id, -32001, error_msg),
                decision,
                risk_level
            )

    # 4. Outbound Forwarding & Response Sanitization
    test_client = getattr(request.app.state, "mock_mcp_client", None)
    target_resp = await forward_mcp_request(payload, http_client=test_client)
    sanitized_resp = sanitize_payload(target_resp)
    
    return build_response(status.HTTP_200_OK, sanitized_resp, "APPROVED", risk_level)
