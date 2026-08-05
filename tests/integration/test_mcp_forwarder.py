import pytest
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
async def test_forward_low_risk_to_target_mcp():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "jsonrpc": "2.0",
            "method": "resources/read",
            "params": {"uri": "file:///docs/readme.txt"},
            "id": "fwd-1"
        }
        response = await client.post("/mcp/v1/proxy", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == "fwd-1"
        assert "result" in data
        assert "contents" in data["result"]
        assert data["result"]["contents"][0]["text"] == "Mock target server content"

@pytest.mark.anyio
async def test_forward_tool_call_to_target_mcp():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_weather",
                "arguments": {"city": "Pune"}
            },
            "id": "fwd-2"
        }
        response = await client.post("/mcp/v1/proxy", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "fwd-2"
        assert "result" in data
        assert "content" in data["result"]
        assert "Executed mock tool get_weather" in data["result"]["content"][0]["text"]

@pytest.mark.anyio
async def test_target_mcp_connection_error():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        async with httpx.AsyncClient(base_url="http://invalid-non-existent-host:9999") as bad_client:
            app.state.mock_mcp_client = bad_client
            payload = {
                "jsonrpc": "2.0",
                "method": "resources/read",
                "params": {"uri": "file:///test.txt"},
                "id": "fwd-err"
            }
            response = await client.post("/mcp/v1/proxy", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["error"]["code"] == -32603
            assert "Target MCP Server Connection Error" in data["error"]["message"]
