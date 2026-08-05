from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.hitl.manager import hitl_manager

router = APIRouter(prefix="/mcp/v1/hitl", tags=["HITL Admin Operations"])

class DecisionPayload(BaseModel):
    comment: Optional[str] = "Decision via Admin REST API"

@router.get("/pending")
async def get_pending_hitl_requests():
    return {"pending": hitl_manager.get_pending_requests()}

@router.post("/approve/{request_id}")
async def approve_hitl_request(request_id: str, payload: Optional[DecisionPayload] = None):
    comment = payload.comment if payload and payload.comment else "Approved via Admin REST API"
    success = await hitl_manager.approve_request(request_id, comment=comment)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="HITL request not found or resolved")
    return {"status": "success", "request_id": request_id, "action": "APPROVED"}

@router.post("/deny/{request_id}")
async def deny_hitl_request(request_id: str, payload: Optional[DecisionPayload] = None):
    comment = payload.comment if payload and payload.comment else "Denied via Admin REST API"
    success = await hitl_manager.deny_request(request_id, comment=comment)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="HITL request not found or resolved")
    return {"status": "success", "request_id": request_id, "action": "DENIED"}
