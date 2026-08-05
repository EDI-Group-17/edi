---
id: "7.2"
key: "7-2-websockets-traffic-dashboard"
epic_id: "EPIC-7"
title: "WebSockets Live Traffic Feed & React Dashboard UI"
status: "done"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 7.2: WebSockets Live Traffic Feed & React Dashboard UI

## Story Statement
**As a** Security Operations Admin,  
**I want a** real-time WebSocket traffic feed (`ws://.../ws/traffic`) and an interactive glassmorphism Admin Dashboard,  
**So that** I can observe MCP agent requests live, view risk scoring, and execute one-click HITL approvals directly from the browser.

---

## Acceptance Criteria (BDD)

### Scenario 1: Real-time WebSocket Transaction Broadcasting [COMPLETED]
- **Given** an active WebSocket connection to `/ws/traffic`
- **When** the proxy processes any low, medium, or high risk JSON-RPC request
- **Then** the transaction payload metadata is broadcast live to all connected WebSocket clients.

### Scenario 2: Interactive Real-Time Dashboard UI [COMPLETED]
- **Given** an administrator opening `/dashboard` in a browser
- **When** live transactions occur or HITL approval requests enter `PENDING` state
- **Then** the UI displays animated live traffic cards, active stats counters, and interactive Approve/Deny buttons.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create WebSocket router in `src/api/websocket.py` and broadcast logic in `src/gateway/router.py`.
- [x] Task 2: Build single-page glassmorphism Admin Dashboard UI in `static/index.html`.
- [x] Task 3: Serve `/dashboard` and `/` in `src/main.py`.
- [x] Task 4: Run full PyTest test suite and confirm 100% pass rate (55/55 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 55 passed in 0.87s
- **Constitutional LOC Check:** All files in `src/` are $< 100$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/api/websocket.py`](file:///Users/harshm/Desktop/edi/src/api/websocket.py)
- [`static/index.html`](file:///Users/harshm/Desktop/edi/static/index.html)
- [`src/main.py`](file:///Users/harshm/Desktop/edi/src/main.py)
- [`tests/unit/test_websocket.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_websocket.py)
