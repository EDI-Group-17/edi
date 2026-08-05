---
id: "6.2"
key: "6-2-background-audit-writer"
epic_id: "EPIC-6"
title: "Asynchronous Queue Batch Audit Writer"
status: "done"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 6.2: Asynchronous Queue Batch Audit Writer

## Story Statement
**As a** High-Concurrency Security Proxy Gateway,  
**I want to** queue transaction audit records in an in-memory `asyncio.Queue` and flush them to PostgreSQL in background batches,  
**So that** high request volumes do not create database lock contention or increase API endpoint response latency.

---

## Acceptance Criteria (BDD)

### Scenario 1: Non-blocking Queue Ingestion [COMPLETED]
- **Given** high-volume request traffic handled by `AuditLogger`
- **When** audit records are logged
- **Then** records are placed into an `asyncio.Queue` in sub-millisecond time ($< 0.1\text{ms}$)
- **And** the caller task returns immediately without awaiting DB write completion.

### Scenario 2: Background Batch Flush to Database [COMPLETED]
- **Given** items accumulated in the `asyncio.Queue`
- **When** the batch size threshold (e.g. 5 items) or periodic flush interval (e.g. 0.5s) is reached
- **Then** the background worker flushes the batch to the database in a single transaction session.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests for BatchAuditWriter (`tests/unit/test_audit_writer.py`).
- [x] Task 2: Implement `src/audit/writer.py` with `BatchAuditWriter` using `asyncio.Queue` and batch flushing.
- [x] Task 3: Route `AuditLogger` transactions to `batch_writer.enqueue`.
- [x] Task 4: Run full PyTest test suite and confirm 100% pass rate (47/47 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 47 passed in 0.88s
- **Constitutional LOC Check:** All files in `src/` are $< 110$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/audit/writer.py`](file:///Users/harshm/Desktop/edi/src/audit/writer.py)
- [`src/audit/logger.py`](file:///Users/harshm/Desktop/edi/src/audit/logger.py)
- [`tests/unit/test_audit_writer.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_audit_writer.py)
