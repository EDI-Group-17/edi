---
id: "6.1"
key: "6-1-sqlalchemy-audit-models"
epic_id: "EPIC-6"
title: "SQLAlchemy Async Audit Models & Non-Blocking Background Logger"
status: "review"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 6.1: SQLAlchemy Async Audit Models & Non-Blocking Background Logger

## Story Statement
**As a** Security Compliance Auditor,  
**I want to** persist every MCP request transaction payload metadata, risk decision, and proxy processing latency asynchronously in a relational database,  
**So that** AgentShield maintains an immutable, queryable audit trail for security compliance and post-incident investigation without degrading runtime proxy performance.

---

## Acceptance Criteria (BDD)

### Scenario 1: Immutable Transaction Recording on Request Approval [COMPLETED]
- **Given** an approved `LOW` or `MEDIUM` risk request processed successfully by the proxy
- **When** the response is delivered to the client
- **Then** a background task asynchronously writes an `AuditRecord` to the database
- **And** records: `request_id`, `agent_id`, `method`, `risk_level: LOW/MEDIUM`, `decision: APPROVED`, and `latency_ms`.

### Scenario 2: Immutable Transaction Recording on Security Blocks [COMPLETED]
- **Given** a blocked request (either due to `PROMPT_INJECTION`, `RATE_LIMITED`, or `LOOP_QUARANTINE`)
- **When** the proxy returns the JSON-RPC error frame
- **Then** a background task asynchronously logs the event with corresponding decision (`BLOCKED`, `RATE_LIMITED`, `QUARANTINED`) to the database.

### Scenario 3: Database Connection Resiliency & In-Memory Fallback [COMPLETED]
- **Given** an environment where the target PostgreSQL database is down or unconfigured
- **When** audit records are queued for write
- **Then** the background logging engine falls back to an in-memory dictionary log store gracefully
- **And** does not raise uncaught exceptions that block gateway proxy thread execution.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests for Audit Logger (`tests/unit/test_audit_logger.py`).
- [x] Task 2: Create integration tests for proxy logging integration (`tests/integration/test_audit_integration.py`).
- [x] Task 3: Implement `src/core/database.py` setting up the async SQLAlchemy engine.
- [x] Task 4: Implement `src/audit/models.py` containing schema columns for request logs.
- [x] Task 5: Implement `src/audit/logger.py` with non-blocking DB commit and fallback store.
- [x] Task 6: Wire background logging tasks into `src/gateway/router.py`.
- [x] Task 7: Run full PyTest test suite and confirm 100% pass rate (34/34 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 34 passed in 1.41s
- **Constitutional LOC Check:** All files in `src/` are $< 110$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/core/database.py`](file:///Users/harshm/Desktop/edi/src/core/database.py)
- [`src/audit/models.py`](file:///Users/harshm/Desktop/edi/src/audit/models.py)
- [`src/audit/logger.py`](file:///Users/harshm/Desktop/edi/src/audit/logger.py)
- [`src/gateway/router.py`](file:///Users/harshm/Desktop/edi/src/gateway/router.py)
- [`tests/unit/test_audit_logger.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_audit_logger.py)
- [`tests/integration/test_audit_integration.py`](file:///Users/harshm/Desktop/edi/tests/integration/test_audit_integration.py)
