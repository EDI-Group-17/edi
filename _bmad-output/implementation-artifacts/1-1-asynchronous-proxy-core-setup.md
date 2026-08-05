---
id: "1.1"
key: "1-1-asynchronous-proxy-core-setup"
epic_id: "EPIC-1"
title: "Asynchronous Proxy Core Setup & FastAPI MCP Router"
status: "review"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 1.1: Asynchronous Proxy Core Setup & FastAPI MCP Router

## Story Statement
**As an** AI Security Engineer,  
**I want to** deploy a lightweight, asynchronous FastAPI proxy router (`/mcp/v1/proxy`) that intercepts JSON-RPC 2.0 requests between AI clients and MCP servers and performs initial 3-tier risk evaluation (`LOW`, `MEDIUM`, `HIGH`),  
**So that** all MCP traffic passes through AgentShield's zero-trust security gateway without requiring modifications to client or server code.

---

## Acceptance Criteria (BDD)

### Scenario 1: Intercept Valid Low-Risk JSON-RPC Request [COMPLETED]
- **Given** an AI client (OpenAI, Gemini, Claude) sending a JSON-RPC 2.0 request to `/mcp/v1/proxy`
- **When** the method is `resources/read` or a read-only `tools/call` (e.g. `get_weather`)
- **Then** AgentShield evaluates the risk as `LOW`
- **And** returns a JSON-RPC response with `200 OK` preserving original request ID.

### Scenario 2: Intercept High-Risk System Mutation Request [COMPLETED]
- **Given** an AI client sending a `tools/call` for a sensitive tool (e.g., `fs.write_file`, `github.delete_repo`, `db.execute_sql`)
- **When** the request payload reaches `/mcp/v1/proxy`
- **Then** AgentShield evaluates the risk as `HIGH`
- **And** returns a JSON-RPC 2.0 Security Hold error response (`code: -32001`, `message: "Security Action Intercepted - Pending HITL Approval"`).

### Scenario 3: Intercept Adversarial Indirect Prompt Injection & Traversal Payload [COMPLETED]
- **Given** an incoming JSON-RPC payload containing path traversal (`../etc/shadow`), command injection (`rm -rf /`), or prompt override tags (`<system_override>...`)
- **When** the payload is inspected by the risk evaluator
- **Then** AgentShield flags the payload as `HIGH` risk with `REASON_PROMPT_INJECTION_DETECTED`
- **And** blocks execution with JSON-RPC error frame (`code: -32002`, `message: "Security Violation: Injection Vector Intercepted"`).

---

## Tasks & Subtasks Progress
- [x] Task 1: Create failing PyTest suite for injection detection and JSON-RPC router (`tests/unit/test_detectors.py`, `tests/unit/test_risk_evaluator.py`, `tests/integration/test_gateway_router.py`).
- [x] Task 2: Implement core settings in `src/core/config.py`.
- [x] Task 3: Implement regex detectors in `src/risk/detectors.py`.
- [x] Task 4: Implement 3-tier risk evaluator in `src/risk/evaluator.py`.
- [x] Task 5: Implement JSON-RPC error frame generator in `src/gateway/errors.py`.
- [x] Task 6: Implement FastAPI proxy router in `src/gateway/router.py` and mount in `src/main.py`.
- [x] Task 7: Execute full test suite and confirm 100% pass rate.

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 11 passed in 0.24s
- **Constitutional LOC Check:** All files in `src/` are $< 35$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/main.py`](file:///Users/harshm/Desktop/edi/src/main.py)
- [`src/core/config.py`](file:///Users/harshm/Desktop/edi/src/core/config.py)
- [`src/risk/detectors.py`](file:///Users/harshm/Desktop/edi/src/risk/detectors.py)
- [`src/risk/evaluator.py`](file:///Users/harshm/Desktop/edi/src/risk/evaluator.py)
- [`src/gateway/errors.py`](file:///Users/harshm/Desktop/edi/src/gateway/errors.py)
- [`src/gateway/router.py`](file:///Users/harshm/Desktop/edi/src/gateway/router.py)
- [`tests/unit/test_detectors.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_detectors.py)
- [`tests/unit/test_risk_evaluator.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_risk_evaluator.py)
- [`tests/integration/test_gateway_router.py`](file:///Users/harshm/Desktop/edi/tests/integration/test_gateway_router.py)
