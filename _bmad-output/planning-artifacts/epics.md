---
title: "AgentShield: Epics & User Stories"
status: "draft"
version: "1.0.0"
created: "2026-08-05"
project: "agentshield"
---

# AgentShield — Epics & User Stories Specification

## Summary of Epics

| Epic ID | Title | Priority | Primary Target Modules |
| :--- | :--- | :--- | :--- |
| **EPIC-1** | Centralized JSON-RPC Security Gateway & Proxy | P0 (Core) | `src/gateway/` |
| **EPIC-2** | Dynamic Risk Assessment Engine & Injection Detectors | P0 (Core) | `src/risk/` |
| **EPIC-3** | Redis Rate Limiting & Loop Quarantine | P1 | `src/ratelimit/` |
| **EPIC-4** | Event-Driven HITL Approval Engine (Redis Pub/Sub) | P1 | `src/hitl/` |
| **EPIC-5** | Response-Side PII Sanitization & Data Redaction | P1 | `src/sanitizer/` |
| **EPIC-6** | PostgreSQL Asynchronous Audit Logger | P2 | `src/audit/` |
| **EPIC-7** | React Admin Web Dashboard & Real-time WebSockets | P2 | `src/dashboard/`, `frontend/` |

---

## EPIC-1: Centralized JSON-RPC Security Gateway & Reverse Proxy

### Story 1.1: Asynchronous Proxy Core Setup & FastAPI Router
- **As an:** AI Security Engineer
- **I want to:** Deploy a lightweight, async FastAPI proxy router that accepts JSON-RPC 2.0 requests from AI clients.
- **So that:** All MCP traffic flows through AgentShield without modifying client or server code.
- **Acceptance Criteria:**
  1. `src/gateway/router.py` defines `/mcp/v1/proxy` endpoint accepting HTTP POST JSON-RPC 2.0 payloads.
  2. File LOC strictly $\le$ 200 lines.
  3. `bmad-tea` PyTest suite validates valid JSON-RPC frames pass parsing checks.

### Story 1.2: MCP Interceptor & Outbound Forwarder
- **As a:** Gateway Proxy Component
- **I want to:** Forward approved JSON-RPC payloads to target enterprise MCP servers using `httpx.AsyncClient`.
- **So that:** Verified tool executions reach target infrastructure asynchronously.
- **Acceptance Criteria:**
  1. `src/gateway/mcp_client.py` handles connection pooling and async HTTP/WebSocket forwarding.
  2. Latency impact on low-risk requests $< 15\text{ms}$.
  3. File LOC $\le$ 200 lines.

### Story 1.3: Standardized JSON-RPC Security Error Generator
- **As an:** AI Client
- **I want to:** Receive standard JSON-RPC 2.0 error frames when a request is blocked by policy or risk evaluation.
- **So that:** LLM agents gracefully handle security rejections (`code: -32001`).
- **Acceptance Criteria:**
  1. `src/gateway/errors.py` formats JSON-RPC error responses with detailed security reason codes.
  2. Unit tests verify error payloads match MCP spec schema.

---

## EPIC-2: Dynamic Risk Assessment Engine & Injection Detectors

### Story 2.1: 3-Tier Risk Classifier Engine
- **As a:** Risk Engine
- **I want to:** Categorize every MCP request payload into `LOW`, `MEDIUM`, or `HIGH` risk tiers.
- **So that:** High-risk write/execute operations are intercepted before execution.
- **Acceptance Criteria:**
  1. `src/risk/evaluator.py` implements the primary `evaluate_risk(request: MCPRequest) -> RiskResult` method.
  2. Read-only queries default to `LOW`; state-mutating operations default to `MEDIUM`/`HIGH`.
  3. File LOC $\le$ 200 lines.

### Story 2.2: Payload Injection & Path Traversal Pattern Detectors
- **As a:** Security Detector
- **I want to:** Scan tool argument strings for shell injections, SQL injections, path traversals (`../`), and prompt overrides.
- **So that:** Adversarial payloads auto-escalate request risk to `HIGH`.
- **Acceptance Criteria:**
  1. `src/risk/detectors.py` contains compiled regex scanners for `../`, `rm -rf`, `; DROP TABLE`, and system prompt injection patterns.
  2. Automated tests verify detection of 20+ benchmark injection strings.

### Story 2.3: Tool Sensitivity & Parameter Mutability Heuristics
- **As a:** Security Administrator
- **I want to:** Map specific tool names (e.g., `fs.write_file`, `github.delete_repo`) to permanent `HIGH` risk rules.
- **So that:** Sensitive system tools always trigger human approval.
- **Acceptance Criteria:**
  1. `src/risk/heuristics.py` checks tool names against configurable high-risk tool registries.
  2. Tests confirm `fs.read_file` is `LOW` while `fs.write_file` is `HIGH`.

---

## EPIC-3: Redis Rate Limiting & Loop Quarantine

### Story 3.1: Redis Atomic Sliding-Window Rate Limiter
- **As a:** Gateway Component
- **I want to:** Track request frequencies per `AgentID` using Redis Lua scripts.
- **So that:** Overactive agents are rate-limited before exhausting backend resources.
- **Acceptance Criteria:**
  1. `src/ratelimit/limiter.py` executes atomic sliding-window checks in $< 2\text{ms}$.
  2. Exceeding limits returns HTTP 429 / JSON-RPC rate limit error.

### Story 3.2: Execution Loop Quarantine Engine
- **As a:** Security System
- **I want to:** Detect repetitive identical tool calls ($> 10$ calls in 5 seconds).
- **So that:** Recursive LLM hallucination loops are automatically quarantined for 60s.
- **Acceptance Criteria:**
  1. `src/ratelimit/loop_detector.py` computes rolling hashes of tool invocation payloads.
  2. Quarantine events trigger audit log entries and auto-block further calls.

---

## EPIC-4: Event-Driven HITL Approval Engine (Redis Pub/Sub)

### Story 4.1: Async Request Hold & Redis Pub/Sub Coordinator
- **As a:** Security Admin
- **I want:** `HIGH` risk requests to hold client connections asynchronously while pushing notifications to the Admin Dashboard.
- **So that:** Administrators can manually review and approve critical operations.
- **Acceptance Criteria:**
  1. `src/hitl/manager.py` uses `asyncio.Event` bound to Redis Pub/Sub channels.
  2. Admin `APPROVE` decision unlocks the event and allows forwarding.

### Story 4.2: Fail-Closed 60s Security Timeout Engine
- **As a:** System Guardian
- **I want:** Pending HITL requests to auto-deny if no admin action occurs within 60 seconds.
- **So that:** Unattended high-risk calls never execute by default.
- **Acceptance Criteria:**
  1. `src/hitl/timeout.py` enforces `asyncio.wait_for(timeout=60)`.
  2. Timeout auto-returns JSON-RPC `-32001 (Security Timeout)` response.

---

## EPIC-5: Response-Side PII Sanitization & Data Redaction

### Story 5.1: PII & Secret Regex Engine
- **As a:** Data Privacy Engine
- **I want to:** Identify API Keys, Credit Cards, Passwords, Aadhaar, and PAN numbers in MCP server text responses.
- **So that:** Sensitive data is sanitized before returning to AI context windows.
- **Acceptance Criteria:**
  1. `src/sanitizer/patterns.py` contains patterns for AWS keys, Bearer tokens, Aadhaar, PAN, and credit cards.

### Story 5.2: Response Payload Redaction Transformer
- **As a:** Sanitizer Component
- **I want to:** Replace sensitive strings with deterministic tokens (`[REDACTED: TYPE]`).
- **So that:** LLMs cannot ingest or leak private credentials.
- **Acceptance Criteria:**
  1. `src/sanitizer/pii_engine.py` recursively transforms JSON/text response bodies.
  2. Tests verify 100% redaction without breaking JSON frame structure.

---

## EPIC-6: PostgreSQL Asynchronous Audit Logger

### Story 6.1: SQLAlchemy Async Audit Models
- **As a:** Compliance Auditor
- **I want to:** Store full transaction records (Agent ID, Risk, Tool, Decision, Latency, Timestamp) in PostgreSQL.
- **So that:** The system maintains an immutable audit trail.
- **Acceptance Criteria:**
  1. `src/audit/models.py` defines `AuditRecord` model using SQLAlchemy Async.

### Story 6.2: Non-Blocking Background Audit Writer
- **As a:** Performance Engine
- **I want:** Audit writes to execute in async background tasks (`FastAPI BackgroundTasks`).
- **So that:** Database I/O never increases client proxy response latency.
- **Acceptance Criteria:**
  1. `src/audit/logger.py` queues audit records without blocking proxy responses.

---

## EPIC-7: React Admin Web Dashboard & Real-time WebSockets

### Story 7.1: Firebase Auth Security Middleware
- **As a:** Security Admin
- **I want to:** Authenticate via Firebase Auth before accessing admin dashboard endpoints.
- **So that:** Unauthorized users cannot modify security policies or view HITL queues.
- **Acceptance Criteria:**
  1. `src/core/security.py` validates Firebase JWT tokens on protected REST/WebSocket routes.

### Story 7.2: WebSockets Traffic Stream & Interactive HITL Queue
- **As an:** Admin User
- **I want to:** View live MCP traffic streams and click Approve/Deny on pending HITL requests in real time.
- **So that:** I can govern enterprise AI operations efficiently.
- **Acceptance Criteria:**
  1. `src/dashboard/ws_manager.py` pushes pending HITL requests and traffic metrics to React UI.
  2. React Dashboard displays action badges with responsive UI controls.
