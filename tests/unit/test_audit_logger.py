import pytest
from sqlalchemy import select
from src.core.database import async_session, init_db
from src.audit.models import AuditRecord
from src.audit.logger import audit_logger

@pytest.mark.anyio
async def test_audit_logger_in_memory_fallback():
    audit_logger.clear_fallback_records()
    await audit_logger.log_transaction(
        request_id="test-audit-1",
        agent_id="agent-007",
        method="tools/call",
        tool_name="fs.read_file",
        payload_hash="abcd1234hash",
        risk_level="LOW",
        decision="APPROVED",
        latency_ms=12.5
    )

    records = audit_logger.get_fallback_records()
    assert len(records) > 0
    record = records[-1]
    assert record["request_id"] == "test-audit-1"
    assert record["agent_id"] == "agent-007"
    assert record["decision"] == "APPROVED"

@pytest.mark.anyio
async def test_audit_logger_database_write():
    # Initialize schema
    await init_db()

    # Log transaction
    await audit_logger.log_transaction(
        request_id="db-test-id",
        agent_id="agent-db-test",
        method="resources/read",
        tool_name=None,
        payload_hash="db_hash_999",
        risk_level="MEDIUM",
        decision="APPROVED",
        latency_ms=45.2
    )

    # Query DB to check if record is persisted
    async with async_session() as session:
        result = await session.execute(
            select(AuditRecord).where(AuditRecord.request_id == "db-test-id")
        )
        record = result.scalars().first()
        assert record is not None
        assert record.agent_id == "agent-db-test"
        assert record.risk_level == "MEDIUM"
        assert record.decision == "APPROVED"
        assert record.latency_ms == 45.2
