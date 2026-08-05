import pytest
import httpx
from src.main import app
from tests.mock_mcp_server import mock_mcp_app
from src.ratelimit.limiter import rate_limiter

@pytest.fixture(autouse=True)
async def setup_mock_target():
    transport = httpx.ASGITransport(app=mock_mcp_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        app.state.mock_mcp_client = client
        yield
        app.state.mock_mcp_client = None

@pytest.mark.anyio
async def test_proxy_rate_limit_exceeded():
    rate_limiter.set_limit(max_requests=2, window_seconds=10)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        headers = {"X-Agent-ID": "agent-rate-limit-test"}
        payload = {
            "jsonrpc": "2.0",
            "method": "resources/read",
            "params": {"uri": "file:///docs/readme.txt"},
            "id": "rate-1"
        }

        # First 2 succeed
        r1 = await client.post("/mcp/v1/proxy", json=payload, headers=headers)
        assert r1.status_code == 200
        assert "result" in r1.json()

        r2 = await client.post("/mcp/v1/proxy", json=payload, headers=headers)
        assert r2.status_code == 200
        assert "result" in r2.json()

        # 3rd fails with -32003
        r3 = await client.post("/mcp/v1/proxy", json=payload, headers=headers)
        assert r3.status_code == 200
        data = r3.json()
        assert data["error"]["code"] == -32003
        assert "Rate Limit Exceeded" in data["error"]["message"]
