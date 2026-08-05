import pytest
import time
from src.ratelimit.limiter import rate_limiter
from src.ratelimit.loop_detector import loop_detector

@pytest.mark.anyio
async def test_sliding_window_rate_limiter():
    agent_id = "test-agent-rate-1"
    # Allow 5 requests per window for testing
    rate_limiter.set_limit(max_requests=5, window_seconds=10)

    for i in range(5):
        allowed, reason = rate_limiter.check_rate_limit(agent_id)
        assert allowed is True

    # 6th request should fail
    allowed, reason = rate_limiter.check_rate_limit(agent_id)
    assert allowed is False
    assert "Rate Limit Exceeded" in reason

@pytest.mark.anyio
async def test_loop_quarantine_detector():
    agent_id = "test-agent-loop-2"
    tool_name = "fs.read_file"
    args = {"path": "/tmp/same.txt"}

    # Execute 9 identical calls -> Allowed
    for _ in range(9):
        quarantined, reason = loop_detector.check_loop(agent_id, tool_name, args, max_repeat=10, window_seconds=5)
        assert quarantined is False

    # 10th identical call within 5s window -> Triggers Quarantine
    quarantined, reason = loop_detector.check_loop(agent_id, tool_name, args, max_repeat=10, window_seconds=5)
    assert quarantined is True
    assert "Execution Loop Quarantine" in reason
