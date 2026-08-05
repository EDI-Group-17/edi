import pytest
import asyncio
from src.hitl.manager import HITLManager

@pytest.mark.anyio
async def test_hitl_timeout_callback_trigger():
    manager = HITLManager()
    called_with = []

    def on_timeout(req_id: str, payload: dict):
        called_with.append((req_id, payload))

    # Register callback
    manager.register_timeout_callback(on_timeout)

    # Register a request and wait with a short timeout
    payload = {"method": "tools/call", "params": {"name": "test_tool"}}
    
    # We expect register_and_wait to return TIMED_OUT
    decision, comment = await manager.register_and_wait("req-timeout-abc", payload, timeout_seconds=0.01)
    
    assert decision == "TIMED_OUT"
    assert len(called_with) == 1
    assert called_with[0][0] == "req-timeout-abc"
    assert called_with[0][1] == payload

@pytest.mark.anyio
async def test_hitl_async_timeout_callback():
    manager = HITLManager()
    called_with = []

    async def on_timeout_async(req_id: str, payload: dict):
        await asyncio.sleep(0.001)
        called_with.append((req_id, payload))

    manager.register_timeout_callback(on_timeout_async)
    payload = {"method": "tools/call", "params": {"name": "test_async_tool"}}
    decision, comment = await manager.register_and_wait("req-async-123", payload, timeout_seconds=0.01)
    
    assert decision == "TIMED_OUT"
    assert len(called_with) == 1
    assert called_with[0][0] == "req-async-123"

