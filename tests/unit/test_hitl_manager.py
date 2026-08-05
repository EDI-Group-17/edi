import pytest
import asyncio
from src.hitl.manager import hitl_manager

@pytest.mark.anyio
async def test_hitl_approve_workflow():
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "fs.write_file", "arguments": {"path": "/tmp/a.txt"}},
        "id": "hitl-test-1"
    }

    async def approve_later():
        await asyncio.sleep(0.05)
        success = await hitl_manager.approve_request("hitl-test-1", comment="Approved by test")
        assert success is True

    asyncio.create_task(approve_later())

    decision, comment = await hitl_manager.register_and_wait("hitl-test-1", payload, timeout_seconds=2)
    assert decision == "APPROVED"
    assert comment == "Approved by test"

@pytest.mark.anyio
async def test_hitl_deny_workflow():
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "fs.write_file", "arguments": {"path": "/etc/shadow"}},
        "id": "hitl-test-2"
    }

    async def deny_later():
        await asyncio.sleep(0.05)
        success = await hitl_manager.deny_request("hitl-test-2", comment="Access denied to system file")
        assert success is True

    asyncio.create_task(deny_later())

    decision, comment = await hitl_manager.register_and_wait("hitl-test-2", payload, timeout_seconds=2)
    assert decision == "DENIED"
    assert "Access denied" in comment

@pytest.mark.anyio
async def test_hitl_timeout_workflow():
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "fs.write_file"},
        "id": "hitl-test-timeout"
    }

    decision, comment = await hitl_manager.register_and_wait("hitl-test-timeout", payload, timeout_seconds=0.1)
    assert decision == "TIMED_OUT"
    assert "Expired" in comment
