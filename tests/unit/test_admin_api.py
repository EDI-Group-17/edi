import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.hitl.manager import hitl_manager, PendingHITLRequest

@pytest.mark.anyio
async def test_admin_metrics_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/api/admin/metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert "pending_hitl_count" in data
        assert "quarantined_agents_count" in data

@pytest.mark.anyio
async def test_admin_hitl_approve_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        item_id = "test-admin-hitl-123"
        hitl_manager._pending[item_id] = PendingHITLRequest(item_id, {"method": "tools/call"})

        resp = await client.post("/api/admin/hitl/approve", json={"request_id": item_id, "comment": "Admin Approved"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "APPROVED"
