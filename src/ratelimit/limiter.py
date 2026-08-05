import time
from typing import Dict, List, Tuple

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Key: agent_id -> List of request timestamps
        self._timestamps: Dict[str, List[float]] = {}

    def set_limit(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def check_rate_limit(self, agent_id: str) -> Tuple[bool, str]:
        now = time.time()
        timestamps = self._timestamps.get(agent_id, [])
        
        # Clean timestamps outside window
        timestamps = [ts for ts in timestamps if now - ts <= self.window_seconds]

        if len(timestamps) >= self.max_requests:
            self._timestamps[agent_id] = timestamps
            return False, f"Rate Limit Exceeded: Max {self.max_requests} requests per {int(self.window_seconds)}s"

        timestamps.append(now)
        self._timestamps[agent_id] = timestamps
        return True, ""

    def reset(self):
        self._timestamps.clear()

rate_limiter = RateLimiter()
