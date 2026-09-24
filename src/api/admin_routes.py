from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from src.hitl.manager import hitl_manager
from src.ratelimit.loop_detector import loop_detector
from src.audit.logger import audit_logger

router = APIRouter(prefix="/api/admin", tags=["Admin"])

class HITLDecisionRequest(BaseModel):
    request_id: str
    comment: Optional[str] = "Admin Override"

class QuarantineReleaseRequest(BaseModel):
    agent_id: str

@router.get("/metrics")
async def get_admin_metrics() -> Dict[str, Any]:
    pending = hitl_manager.get_pending_requests()
    quarantined = loop_detector.get_quarantined_agents_detailed()
    fallback_logs = audit_logger.get_fallback_records()
    return {
        "pending_hitl_count": len(pending),
        "quarantined_agents_count": len(quarantined),
        "total_fallback_logs": len(fallback_logs),
        "quarantined_agents": quarantined
    }

@router.get("/hitl/pending")
async def list_pending_hitl() -> List[Dict[str, Any]]:
    return hitl_manager.get_pending_requests()

@router.post("/hitl/approve")
async def approve_hitl(req: HITLDecisionRequest):
    success = await hitl_manager.approve_request(req.request_id, req.comment or "Approved via Admin Dashboard")
    if not success:
        raise HTTPException(status_code=404, detail="Pending HITL request not found or expired")
    return {"status": "APPROVED", "request_id": req.request_id}

@router.post("/hitl/deny")
async def deny_hitl(req: HITLDecisionRequest):
    success = await hitl_manager.deny_request(req.request_id, req.comment or "Denied via Admin Dashboard")
    if not success:
        raise HTTPException(status_code=404, detail="Pending HITL request not found or expired")
    return {"status": "DENIED", "request_id": req.request_id}

@router.get("/quarantine")
async def get_quarantined():
    return {"quarantined_agents": loop_detector.get_quarantined_agents_detailed()}

@router.post("/quarantine/release")
async def release_quarantine_agent(req: QuarantineReleaseRequest):
    released = loop_detector.release_quarantine(req.agent_id)
    return {"agent_id": req.agent_id, "released": released}
