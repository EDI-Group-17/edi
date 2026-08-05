import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from src.core.database import async_session
from src.audit.models import AuditRecord

logger = logging.getLogger("agentshield.audit")

class AuditLogger:
    def __init__(self):
        self._fallback: List[Dict[str, Any]] = []

    async def log_transaction(
        self,
        request_id: str,
        agent_id: str,
        method: str,
        tool_name: Optional[str],
        payload_hash: str,
        risk_level: str,
        decision: str,
        latency_ms: float
    ):
        record_dict = {
            "request_id": request_id,
            "agent_id": agent_id,
            "method": method,
            "tool_name": tool_name,
            "payload_hash": payload_hash,
            "risk_level": risk_level,
            "decision": decision,
            "latency_ms": latency_ms,
            "timestamp": datetime.utcnow()
        }

        self._fallback.append(record_dict)
        if len(self._fallback) > 1000:
            self._fallback.pop(0)

        try:
            async with async_session() as session:
                async with session.begin():
                    db_record = AuditRecord(
                        request_id=request_id,
                        agent_id=agent_id,
                        method=method,
                        tool_name=tool_name,
                        payload_hash=payload_hash,
                        risk_level=risk_level,
                        decision=decision,
                        latency_ms=latency_ms,
                        timestamp=record_dict["timestamp"]
                    )
                    session.add(db_record)
                await session.commit()
        except Exception as exc:
            logger.warning(f"Database audit write failed; using fallback. Error: {str(exc)}")

    def get_fallback_records(self) -> List[Dict[str, Any]]:
        return self._fallback

    def clear_fallback_records(self):
        self._fallback.clear()

audit_logger = AuditLogger()
