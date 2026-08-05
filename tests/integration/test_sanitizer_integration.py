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
async def test_proxy_response_sanitization():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_user_info",
                "arguments": {"user_id": "123"}
            },
            "id": "sanitizer-1"
        }
        response = await client.post("/mcp/v1/proxy", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "sanitizer-1"
        assert "result" in data
        
        result = data["result"]
        assert result["user"] == "Harsh"
        assert result["aws_key"] == "[REDACTED: API_KEY]"
        assert result["aadhaar"] == "[REDACTED: AADHAAR_NUMBER]"
        assert result["pan"] == "[REDACTED: PAN_NUMBER]"
        assert "AKIAIOSFODNN7EXAMPLE" not in str(data)
        assert "3675 8392 0192" not in str(data)
        assert "ABCDE1234F" not in str(data)
