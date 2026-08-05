---
id: "4.1"
key: "4-1-hitl-manager-pubsub"
epic_id: "EPIC-4"
title: "Event-Driven HITL Approval Engine (Pub/Sub & Async Hold)"
status: "review"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 4.1: Event-Driven HITL Approval Engine (Pub/Sub & Async Hold)

## Story Statement
**As a** Security Gateway,  
**I want to** pause `HIGH` risk MCP requests asynchronously using `asyncio.Event` and publish pending approval events to an event bus,  
**So that** security administrators can review pending requests and approve or deny them in real time without blocking worker threads or dropping client connections.

---

## Acceptance Criteria (BDD)

### Scenario 1: High-Risk Request Enters Async Pending HITL Hold [COMPLETED]
- **Given** an incoming JSON-RPC request evaluated as `HIGH` risk
- **When** the proxy receives the request
- **Then** `src/hitl/manager.py` registers the request in the pending queue with status `PENDING`
- **And** holds the client connection open asynchronously waiting for an approval signal.

### Scenario 2: Admin Approval Signal Releases Connection & Forwards Payload [COMPLETED]
- **Given** a pending HITL request waiting in async hold
- **When** an admin emits an `APPROVE` decision for `request_id`
- **Then** the `asyncio.Event` is triggered
- **And** the gateway releases the hold and forwards the request to the target MCP server.

### Scenario 3: Admin Denial Signal Returns Security Block Frame [COMPLETED]
- **Given** a pending HITL request waiting in async hold
- **When** an admin emits a `DENY` decision with comment
- **Then** the gateway releases the hold and returns a JSON-RPC error frame (`code: -32001`, `message: "Security Action Denied by HITL Admin"`).

### Scenario 4: Fail-Closed 60s Timeout Auto-Denies Unattended Requests [COMPLETED]
- **Given** a pending HITL request waiting in async hold
- **When** 60 seconds elapse without an admin decision
- **Then** the request times out automatically
- **And** returns a JSON-RPC error frame (`code: -32001`, `message: "Security Timeout: HITL Approval Request Expired"`).

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests for HITL Manager (`tests/unit/test_hitl_manager.py`).
- [x] Task 2: Create end-to-end integration tests for HITL workflow (`tests/integration/test_hitl_workflow.py`).
- [x] Task 3: Implement `src/hitl/manager.py` with `asyncio.Event` async hold & pending request queue.
- [x] Task 4: Implement `src/hitl/router.py` with `/mcp/v1/hitl/pending`, `/approve/{id}`, and `/deny/{id}` endpoints.
- [x] Task 5: Integrate `hitl_manager` into `src/gateway/router.py` for `HIGH` risk requests.
- [x] Task 6: Run full PyTest test suite and confirm 100% pass rate (20/20 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 20 passed in 0.65s
- **Constitutional LOC Check:** All files in `src/` are $< 70$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/hitl/manager.py`](file:///Users/harshm/Desktop/edi/src/hitl/manager.py)
- [`src/hitl/router.py`](file:///Users/harshm/Desktop/edi/src/hitl/router.py)
- [`src/gateway/router.py`](file:///Users/harshm/Desktop/edi/src/gateway/router.py)
- [`src/main.py`](file:///Users/harshm/Desktop/edi/src/main.py)
- [`tests/unit/test_hitl_manager.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_hitl_manager.py)
- [`tests/integration/test_hitl_workflow.py`](file:///Users/harshm/Desktop/edi/tests/integration/test_hitl_workflow.py)
