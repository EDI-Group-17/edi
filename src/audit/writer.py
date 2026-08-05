import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from src.core.database import async_session
from src.audit.models import AuditRecord

logger = logging.getLogger("agentshield.writer")

class BatchAuditWriter:
    def __init__(self, batch_size: int = 10, flush_interval_seconds: float = 1.0):
        self.batch_size = batch_size
        self.flush_interval_seconds = flush_interval_seconds
        self.queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._fallback: List[Dict[str, Any]] = []

    async def enqueue(self, record: Dict[str, Any]):
        self._fallback.append(record)
        await self.queue.put(record)

    async def start_worker(self):
        self._running = True
        while self._running:
            batch: List[Dict[str, Any]] = []
            try:
                # Wait for at least 1 item or timeout
                item = await asyncio.wait_for(self.queue.get(), timeout=self.flush_interval_seconds)
                batch.append(item)
                self.queue.task_done()

                # Drain remaining available items up to batch_size
                while len(batch) < self.batch_size and not self.queue.empty():
                    batch.append(self.queue.get_nowait())
                    self.queue.task_done()
            except asyncio.TimeoutError:
                pass

            if batch:
                await self._flush_batch(batch)

    async def _flush_batch(self, batch: List[Dict[str, Any]]):
        try:
            async with async_session() as session:
                async with session.begin():
                    db_records = [
                        AuditRecord(
                            request_id=rec["request_id"],
                            agent_id=rec["agent_id"],
                            method=rec["method"],
                            tool_name=rec.get("tool_name"),
                            payload_hash=rec["payload_hash"],
                            risk_level=rec["risk_level"],
                            decision=rec["decision"],
                            latency_ms=rec["latency_ms"],
                            timestamp=rec.get("timestamp") or datetime.utcnow()
                        )
                        for rec in batch
                    ]
                    session.add_all(db_records)
                await session.commit()
        except Exception as exc:
            logger.warning(f"Batch DB flush failed; using fallback. Error: {str(exc)}")

    async def stop_worker(self, worker_task: Optional[asyncio.Task] = None):
        self._running = False
        if worker_task:
            worker_task.cancel()
            try:
                await worker_task
            except asyncio.CancelledError:
                pass

        # Flush any remaining items in queue before shutting down
        remaining: List[Dict[str, Any]] = []
        while not self.queue.empty():
            remaining.append(self.queue.get_nowait())
            self.queue.task_done()
        if remaining:
            await self._flush_batch(remaining)

batch_writer = BatchAuditWriter()
