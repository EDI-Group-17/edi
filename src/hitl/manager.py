import asyncio
import time
from typing import Any, Dict, List, Optional, Tuple

import inspect

class PendingHITLRequest:
    def __init__(self, request_id: str, payload: Dict[str, Any]):
        self.request_id = request_id
        self.payload = payload
        self.event = asyncio.Event()
        self.status = "PENDING"
        self.decision: Optional[str] = None
        self.comment: Optional[str] = None
        self.timestamp = time.time()

class HITLManager:
    def __init__(self):
        self._pending: Dict[str, PendingHITLRequest] = {}
        self._timeout_callbacks = []

    def register_timeout_callback(self, callback):
        self._timeout_callbacks.append(callback)

    async def register_and_wait(
        self, request_id: str, payload: Dict[str, Any], timeout_seconds: float = 60.0
    ) -> Tuple[str, str]:
        item = PendingHITLRequest(request_id, payload)
        self._pending[request_id] = item

        try:
            await asyncio.wait_for(item.event.wait(), timeout=timeout_seconds)
            return item.decision or "DENIED", item.comment or ""
        except asyncio.TimeoutError:
            if item.event.is_set():
                return item.decision or "APPROVED", item.comment or ""
            item.status = "TIMED_OUT"
            item.decision = "TIMED_OUT"
            item.comment = "Security Timeout: HITL Approval Request Expired"
            
            # Fire registered callbacks (supporting both sync and async)
            for cb in self._timeout_callbacks:
                try:
                    if inspect.iscoroutinefunction(cb):
                        await cb(request_id, payload)
                    else:
                        cb(request_id, payload)
                except Exception:
                    pass
                    
            return "TIMED_OUT", item.comment
        finally:
            self._pending.pop(request_id, None)

    async def approve_request(self, request_id: str, comment: str = "Approved by Admin") -> bool:
        item = self._pending.get(request_id)
        if not item or item.event.is_set():
            return False
        item.status = "APPROVED"
        item.decision = "APPROVED"
        item.comment = comment
        item.event.set()
        return True

    async def deny_request(self, request_id: str, comment: str = "Denied by Admin") -> bool:
        item = self._pending.get(request_id)
        if not item or item.event.is_set():
            return False
        item.status = "DENIED"
        item.decision = "DENIED"
        item.comment = comment
        item.event.set()
        return True

    def get_pending_requests(self) -> List[Dict[str, Any]]:
        return [
            {
                "request_id": item.request_id,
                "payload": item.payload,
                "status": item.status,
                "timestamp": item.timestamp
            }
            for item in self._pending.values()
            if not item.event.is_set()
        ]

hitl_manager = HITLManager()
