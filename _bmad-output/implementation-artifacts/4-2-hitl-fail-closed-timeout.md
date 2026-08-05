---
id: "4.2"
key: "4-2-hitl-fail-closed-timeout"
epic_id: "EPIC-4"
title: "HITL Fail-Closed Timeout Notification"
status: "done"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 4.2: HITL Fail-Closed Timeout Notification

## Story Statement
**As a** Security Operations Admin,  
**I want to** be notified via logs and registerable callbacks when a Human-in-the-Loop approval request times out and fails closed,  
**So that** I can track expired tickets and identify potential system delays or unresponsive admins.

---

## Acceptance Criteria (BDD)

### Scenario 1: HITL Request Expiration Callback Trigger [COMPLETED]
- **Given** a pending HITL request waiting for approval
- **When** the timeout expires (e.g. 60 seconds) without admin input
- **Then** the request is marked `TIMED_OUT` (failing closed)
- **And** any registered timeout callback is executed with the request details.

### Scenario 2: Admin Logging Warning on Expiration [COMPLETED]
- **Given** a pending HITL request
- **When** the request transitions to `TIMED_OUT`
- **Then** a warning log entry `Security Timeout: HITL Approval Request Expired` is emitted.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests for HITL timeout callback trigger (`tests/unit/test_hitl_timeout.py`).
- [x] Task 2: Refactor `src/hitl/manager.py` implementing `register_timeout_callback` and executing callbacks on timeout.
- [x] Task 3: Run full PyTest test suite and confirm 100% pass rate (40/40 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 40 passed in 0.76s
- **Constitutional LOC Check:** All files in `src/` are $< 110$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/hitl/manager.py`](file:///Users/harshm/Desktop/edi/src/hitl/manager.py)
- [`tests/unit/test_hitl_timeout.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_hitl_timeout.py)
