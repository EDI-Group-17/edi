import pytest
import asyncio
import httpx
from src.main import app
from tests.mock_mcp_server import mock_mcp_app

@pytest.fixture(autouse=True)
async def setup_mock_target():
    transport = httpx.ASGITransport(app=mock_mcp_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        app.state.mock_mcp_client = client
        yield
        app.state.mock_mcp_client = None

@pytest.mark.anyio
async def test_hitl_end_to_end_approval():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        high_risk_payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "fs.write_file",
                "arguments": {"path": "/docs/test.txt", "content": "approved data"}
            },
            "id": "e2e-hitl-1"
        }

        async def admin_approve_job():
            await asyncio.sleep(0.05)
            pending_resp = await client.get("/mcp/v1/hitl/pending")
            assert pending_resp.status_code == 200
            pending_items = pending_resp.json().get("pending", [])
            assert any(item["request_id"] == "e2e-hitl-1" for item in pending_items)

            approve_resp = await client.post("/mcp/v1/hitl/approve/e2e-hitl-1", json={"comment": "LGTM"})
            assert approve_resp.status_code == 200

        asyncio.create_task(admin_approve_job())

        response = await client.post("/mcp/v1/proxy", json=high_risk_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == "e2e-hitl-1"
        assert "result" in data
        assert "content" in data["result"]

@pytest.mark.anyio
async def test_hitl_end_to_end_denial():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        high_risk_payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "fs.write_file",
                "arguments": {"path": "/etc/passwd", "content": "bad"}
            },
            "id": "e2e-hitl-2"
        }

        async def admin_deny_job():
            await asyncio.sleep(0.05)
            deny_resp = await client.post("/mcp/v1/hitl/deny/e2e-hitl-2", json={"comment": "Forbidden target file"})
            assert deny_resp.status_code == 200

        asyncio.create_task(admin_deny_job())

        response = await client.post("/mcp/v1/proxy", json=high_risk_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["error"]["code"] == -32001
        assert "Security Action Denied by HITL Admin" in data["error"]["message"]
