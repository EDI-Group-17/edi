---
id: "3.2"
key: "3-2-loop-quarantine-engine"
epic_id: "EPIC-3"
title: "Execution Loop Quarantine Engine & State Manager"
status: "done"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 3.2: Execution Loop Quarantine Engine & State Manager

## Story Statement
**As an** AI Security Gateway Proxy,  
**I want to** maintain active quarantine state for agents trapped in repetitive tool loops and expose management functions to inspect or release quarantined agents,  
**So that** infinite loops are blocked across requests for a configurable quarantine period without affecting healthy agents.

---

## Acceptance Criteria (BDD)

### Scenario 1: Persistent Loop Quarantine Lockout [COMPLETED]
- **Given** an agent that triggered a loop quarantine event ($>10$ identical tool calls within 5s window)
- **When** subsequent tool calls arrive from the same agent within the quarantine window (default: 60s)
- **Then** the proxy immediately rejects the calls with `LOOP_QUARANTINE_ACTIVE`.

### Scenario 2: Active Quarantine Inspection and Manual Release [COMPLETED]
- **Given** one or more quarantined agents
- **When** calling `get_quarantined_agents()` or `release_quarantine(agent_id)`
- **Then** active quarantined agents are listed or manually unblocked.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests in `tests/unit/test_loop_quarantine.py`.
- [x] Task 2: Expand `src/ratelimit/loop_detector.py` with `is_quarantined`, `get_quarantined_agents`, and `release_quarantine`.
- [x] Task 3: Run full PyTest test suite and confirm 100% pass rate (51/51 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 51 passed in 1.25s
- **Constitutional LOC Check:** All files in `src/` are $< 100$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/ratelimit/loop_detector.py`](file:///Users/harshm/Desktop/edi/src/ratelimit/loop_detector.py)
- [`tests/unit/test_loop_quarantine.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_loop_quarantine.py)
