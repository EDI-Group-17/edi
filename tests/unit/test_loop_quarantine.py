import pytest
import time
from src.ratelimit.loop_detector import LoopQuarantineDetector

def test_loop_quarantine_persistence_and_release():
    detector = LoopQuarantineDetector(max_repeat_calls=3, window_seconds=5.0, quarantine_seconds=60.0)
    agent_id = "agent-loop-test"

    # Trigger quarantine by making 4 identical calls
    for _ in range(3):
        detector.record_and_check_loop(agent_id, "fs.read", {"path": "/tmp/test"})

    # 4th call triggers quarantine
    is_loop = detector.record_and_check_loop(agent_id, "fs.read", {"path": "/tmp/test"})
    assert is_loop is True
    assert detector.is_quarantined(agent_id) is True

    # Inspect quarantined agents list
    quarantined = detector.get_quarantined_agents()
    assert agent_id in quarantined

    # Manually release quarantine
    released = detector.release_quarantine(agent_id)
    assert released is True
    assert detector.is_quarantined(agent_id) is False
