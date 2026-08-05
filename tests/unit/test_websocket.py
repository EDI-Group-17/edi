import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.websocket import ws_manager

def test_websocket_traffic_connection():
    client = TestClient(app)
    with client.websocket_connect("/ws/traffic") as websocket:
        websocket.send_text("ping")
        data = websocket.receive_text()
        assert data == "pong"

@pytest.mark.anyio
async def test_websocket_broadcast():
    assert ws_manager is not None
