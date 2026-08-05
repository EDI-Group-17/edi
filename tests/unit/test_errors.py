import pytest
from src.gateway.errors import (
    build_jsonrpc_error,
    build_hitl_pending_error,
    build_injection_blocked_error,
    build_rate_limit_error,
    build_loop_quarantine_error
)

def test_jsonrpc_error_compliance():
    err = build_jsonrpc_error("id-123", -32001, "Error Message", {"extra": "details"})
    assert err["jsonrpc"] == "2.0"
    assert err["id"] == "id-123"
    assert err["error"]["code"] == -32001
    assert err["error"]["message"] == "Error Message"
    assert err["error"]["data"] == {"extra": "details"}

def test_jsonrpc_error_null_id():
    err = build_jsonrpc_error(None, -32603, "Null ID Error")
    assert err["id"] is None
    assert err["jsonrpc"] == "2.0"

def test_predefined_error_builders():
    # Test HITL Pending Error
    hitl = build_hitl_pending_error("req-1", "Requires human review")
    assert hitl["error"]["code"] == -32001
    assert hitl["error"]["data"]["status"] == "PENDING_APPROVAL"

    # Test Injection Blocked Error
    inj = build_injection_blocked_error("req-2", "Shell Injection")
    assert inj["error"]["code"] == -32002
    assert inj["error"]["data"]["status"] == "BLOCKED"

    # Test Rate Limit Error
    rl = build_rate_limit_error("req-3", "Too fast")
    assert rl["error"]["code"] == -32003
    assert rl["error"]["data"]["status"] == "RATE_LIMITED"

    # Test Loop Quarantine Error
    loop = build_loop_quarantine_error("req-4", "Recursive loop")
    assert loop["error"]["code"] == -32004
    assert loop["error"]["data"]["status"] == "QUARANTINED"
