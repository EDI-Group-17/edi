import pytest
from src.ratelimit.limiter import rate_limiter
from src.ratelimit.loop_detector import loop_detector
from src.core.database import engine

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
def reset_rate_limiters():
    rate_limiter.set_limit(max_requests=60, window_seconds=60)
    rate_limiter.reset()
    loop_detector._history.clear()
    loop_detector._quarantined.clear()
    yield
    rate_limiter.reset()
    loop_detector._history.clear()
    loop_detector._quarantined.clear()

@pytest.fixture(scope="session", autouse=True)
async def cleanup_database_engine():
    yield
    await engine.dispose()
