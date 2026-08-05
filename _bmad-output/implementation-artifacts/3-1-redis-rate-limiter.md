---
id: "3.1"
key: "3-1-redis-rate-limiter"
epic_id: "EPIC-3"
title: "Redis Rate Limiting & Execution Loop Quarantine Engine"
status: "review"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 3.1: Redis Rate Limiting & Execution Loop Quarantine Engine

## Story Statement
**As an** AI Security Gateway Proxy,  
**I want to** enforce sliding-window rate limits per Agent ID and detect recursive tool execution loops,  
**So that** malicious or hallucinating AI agents cannot exhaust backend system resources or flood target MCP servers with infinite execution loops.

---

## Acceptance Criteria (BDD)

### Scenario 1: Sliding-Window Rate Limit Enforcement [COMPLETED]
- **Given** an AI agent emitting requests to `/mcp/v1/proxy`
- **When** the agent exceeds the configured rate limit (e.g. $> 60$ requests/minute)
- **Then** AgentShield blocks subsequent requests
- **And** returns a JSON-RPC 2.0 error frame (`code: -32003`, `message: "Rate Limit Exceeded: Too Many Requests"`).

### Scenario 2: Recursive Tool Invocation Loop Detection & Quarantine [COMPLETED]
- **Given** an AI agent calling the exact same tool with identical arguments $> 10$ times in a 5-second window
- **When** `src/ratelimit/loop_detector.py` evaluates the rolling payload hashes
- **Then** the agent is automatically placed in a 60-second quarantine (`LOOP_QUARANTINE`)
- **And** returns a JSON-RPC 2.0 error frame (`code: -32004`, `message: "Execution Loop Detected: Agent Quarantined"`).

### Scenario 3: Graceful In-Memory Fallback [COMPLETED]
- **Given** an environment without a running Redis server
- **When** the rate limiter operates
- **Then** it falls back to an in-memory sliding-window cache without raising uncaught exceptions.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests for Rate Limiter and Loop Detector (`tests/unit/test_rate_limiter.py`).
- [x] Task 2: Create integration tests for proxy rate limit enforcement (`tests/integration/test_ratelimit_integration.py`).
- [x] Task 3: Implement `src/ratelimit/loop_detector.py` with payload hash tracking & quarantine timers.
- [x] Task 4: Implement `src/ratelimit/limiter.py` with sliding window timestamp manager.
- [x] Task 5: Wire rate limiting and loop detection into `src/gateway/router.py`.
- [x] Task 6: Run full PyTest test suite and confirm 100% pass rate (31/31 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 31 passed in 0.65s
- **Constitutional LOC Check:** All files in `src/` are $< 70$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/ratelimit/limiter.py`](file:///Users/harshm/Desktop/edi/src/ratelimit/limiter.py)
- [`src/ratelimit/loop_detector.py`](file:///Users/harshm/Desktop/edi/src/ratelimit/loop_detector.py)
- [`src/gateway/errors.py`](file:///Users/harshm/Desktop/edi/src/gateway/errors.py)
- [`src/gateway/router.py`](file:///Users/harshm/Desktop/edi/src/gateway/router.py)
- [`tests/unit/test_rate_limiter.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_rate_limiter.py)
- [`tests/integration/test_ratelimit_integration.py`](file:///Users/harshm/Desktop/edi/tests/integration/test_ratelimit_integration.py)
