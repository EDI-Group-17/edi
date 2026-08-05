import pytest
import asyncio
import uuid
from src.audit.writer import BatchAuditWriter
from src.audit.models import AuditRecord
from src.core.database import init_db, async_session
from sqlalchemy import select

@pytest.mark.anyio
async def test_batch_audit_writer_enqueue_and_flush():
    await init_db()
    writer = BatchAuditWriter(batch_size=3, flush_interval_seconds=1.0)
    
    # Start background worker
    worker_task = asyncio.create_task(writer.start_worker())

    req1_id = f"batch-{uuid.uuid4().hex[:8]}"
    req2_id = f"batch-{uuid.uuid4().hex[:8]}"
    req3_id = f"batch-{uuid.uuid4().hex[:8]}"

    record_1 = {
        "request_id": req1_id,
        "agent_id": "agent-b1",
        "method": "tools/call",
        "tool_name": "fs.read",
        "payload_hash": "hash1",
        "risk_level": "LOW",
        "decision": "APPROVED",
        "latency_ms": 10.0
    }
    record_2 = {
        "request_id": req2_id,
        "agent_id": "agent-b2",
        "method": "tools/call",
        "tool_name": "fs.write",
        "payload_hash": "hash2",
        "risk_level": "HIGH",
        "decision": "DENIED",
        "latency_ms": 15.0
    }
    record_3 = {
        "request_id": req3_id,
        "agent_id": "agent-b3",
        "method": "resources/read",
        "tool_name": None,
        "payload_hash": "hash3",
        "risk_level": "LOW",
        "decision": "APPROVED",
        "latency_ms": 8.0
    }

    # Enqueue 3 items (triggers batch_size limit)
    await writer.enqueue(record_1)
    await writer.enqueue(record_2)
    await writer.enqueue(record_3)

    # Allow worker time to process flush
    await asyncio.sleep(0.1)

    # Stop worker cleanly
    await writer.stop_worker(worker_task)

    # Query DB to check if records were persisted in batch
    async with async_session() as session:
        result = await session.execute(
            select(AuditRecord).where(AuditRecord.request_id.in_([req1_id, req2_id, req3_id]))
        )
        records = result.scalars().all()
        assert len(records) == 3
