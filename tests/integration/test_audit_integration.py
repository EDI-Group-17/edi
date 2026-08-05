import pytest
import httpx
import asyncio
from src.main import app
from tests.mock_mcp_server import mock_mcp_app
from src.audit.logger import audit_logger

@pytest.fixture(autouse=True)
async def setup_mock_target():
    transport = httpx.ASGITransport(app=mock_mcp_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        app.state.mock_mcp_client = client
        yield
        app.state.mock_mcp_client = None

@pytest.mark.anyio
async def test_gateway_logs_approved_transaction():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "jsonrpc": "2.0",
            "method": "resources/read",
            "params": {"uri": "file:///docs/help.txt"},
            "id": "audit-int-1"
        }
        
        # Clear fallback logs
        audit_logger.clear_fallback_records()

        response = await client.post("/mcp/v1/proxy", json=payload, headers={"X-Agent-ID": "agent-audit"})
        assert response.status_code == 200

        # Wait a small instant for background task completion
        await asyncio.sleep(0.05)

        records = audit_logger.get_fallback_records()
        assert len(records) > 0
        record = records[-1]
        assert record["request_id"] == "audit-int-1"
        assert record["agent_id"] == "agent-audit"
        assert record["risk_level"] == "LOW"
        assert record["decision"] == "APPROVED"
