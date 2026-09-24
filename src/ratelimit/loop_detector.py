import hashlib
import json
import time
from typing import Any, Dict, List, Tuple

class LoopDetector:
    def __init__(self, max_repeat_calls: int = 10, window_seconds: float = 5.0, quarantine_seconds: float = 60.0):
        self.max_repeat_calls = max_repeat_calls
        self.window_seconds = window_seconds
        self.quarantine_seconds = quarantine_seconds
        # Key: agent_id -> List of (timestamp, payload_hash)
        self._history: Dict[str, List[Tuple[float, str]]] = {}
        # Key: agent_id -> quarantine_until_timestamp
        self._quarantined: Dict[str, float] = {}

    def check_loop(
        self, agent_id: str, tool_name: str, arguments: Dict[str, Any], max_repeat: int = None, window_seconds: float = None
    ) -> Tuple[bool, str]:
        max_rep = max_repeat or self.max_repeat_calls
        win_sec = window_seconds or self.window_seconds
        now = time.time()

        # Check existing quarantine status
        if self.is_quarantined(agent_id):
            remaining = int(self._quarantined[agent_id] - now)
            return True, f"Execution Loop Quarantine Active ({remaining}s remaining)"

        # Hash payload safely with fallback serialization
        try:
            payload_str = f"{tool_name}:{json.dumps(arguments, sort_keys=True, default=str)}"
        except Exception:
            payload_str = f"{tool_name}:{str(arguments)}"
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()

        # Clean old history
        history = self._history.get(agent_id, [])
        history = [(ts, h) for ts, h in history if now - ts <= win_sec]
        history.append((now, payload_hash))
        self._history[agent_id] = history

        # Count occurrences of identical hash in window
        identical_count = sum(1 for _, h in history if h == payload_hash)
        if identical_count >= max_rep:
            self._quarantined[agent_id] = now + self.quarantine_seconds
            return True, f"Execution Loop Quarantine Triggered: Tool '{tool_name}' invoked {identical_count} times in {win_sec}s"

        return False, ""

    def record_and_check_loop(self, agent_id: str, tool_name: str, arguments: Dict[str, Any]) -> bool:
        is_loop, _ = self.check_loop(agent_id, tool_name, arguments)
        return is_loop

    def is_quarantined(self, agent_id: str) -> bool:
        now = time.time()
        if agent_id in self._quarantined:
            if now < self._quarantined[agent_id]:
                return True
            else:
                self._quarantined.pop(agent_id, None)
        return False

    def get_quarantined_agents(self) -> List[str]:
        now = time.time()
        active = []
        for agent_id, until in list(self._quarantined.items()):
            if now < until:
                active.append(agent_id)
            else:
                self._quarantined.pop(agent_id, None)
        return active

    def get_quarantined_agents_detailed(self) -> List[Dict[str, Any]]:
        now = time.time()
        active = []
        for agent_id, until in list(self._quarantined.items()):
            if now < until:
                active.append({"agent_id": agent_id, "remaining_seconds": int(until - now)})
            else:
                self._quarantined.pop(agent_id, None)
        return active

    def release_quarantine(self, agent_id: str) -> bool:
        if agent_id in self._quarantined:
            self._quarantined.pop(agent_id, None)
            return True
        return False

LoopQuarantineDetector = LoopDetector
loop_detector = LoopDetector()
