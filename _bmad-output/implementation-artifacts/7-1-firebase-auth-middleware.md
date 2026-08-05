---
id: "7.1"
key: "7-1-firebase-auth-middleware"
epic_id: "EPIC-7"
title: "Firebase Auth & Admin Dashboard API Routes"
status: "done"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 7.1: Firebase Auth & Admin Dashboard API Routes

## Story Statement
**As a** Security Admin,  
**I want** secure REST API routes for authentication, audit log retrieval, pending HITL approval management, and quarantine control,  
**So that** only authenticated administrative users can view security metrics and execute manual approval/denial overrides.

---

## Acceptance Criteria (BDD)

### Scenario 1: Admin Dashboard Metric API [COMPLETED]
- **Given** an administrative client requesting `/api/admin/metrics` or `/api/admin/audit-logs`
- **When** the REST endpoint is called
- **Then** it returns recent audit log records, pending HITL request items, and quarantined agent lists.

### Scenario 2: Administrative HITL Decision Override [COMPLETED]
- **Given** a pending HITL request ID
- **When** an admin posts to `/api/admin/hitl/approve` or `/api/admin/hitl/deny`
- **Then** the `hitl_manager` resolves the pending request immediately.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests in `tests/unit/test_admin_api.py`.
- [x] Task 2: Implement `src/api/admin_routes.py` with metrics, HITL override, and quarantine endpoints.
- [x] Task 3: Include `admin_router` in `src/main.py`.
- [x] Task 4: Run full PyTest test suite and confirm 100% pass rate (55/55 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 55 passed in 0.87s
- **Constitutional LOC Check:** All files in `src/` are $< 100$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/api/admin_routes.py`](file:///Users/harshm/Desktop/edi/src/api/admin_routes.py)
- [`src/main.py`](file:///Users/harshm/Desktop/edi/src/main.py)
- [`tests/unit/test_admin_api.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_admin_api.py)
