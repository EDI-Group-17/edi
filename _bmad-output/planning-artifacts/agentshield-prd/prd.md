---
title: "AgentShield: A Dynamic Risk-Aware Security Framework for Model Context Protocol"
status: "draft"
version: "1.0.0"
created: "2026-08-05"
authors:
  - "Harsh Manjramkar (Roll No. 70)"
  - "Vedant Gaidhani (Roll No. 74)"
  - "Vineet Wagh (Roll No. 75)"
  - "Arjun Joshi (Roll No. 76)"
guide: "Prof. Sanyukta Deshmukh"
institution: "Vishwakarma Institute of Technology, Department of Computer Engineering"
---

# AgentShield PRD — Product Requirements Document

## 1. Executive Summary & Problem Statement

### 1.1 Executive Summary
**AgentShield** is a dynamic, risk-aware security framework and runtime gateway for the **Model Context Protocol (MCP)**. Positioned between AI agents (OpenAI, Gemini, Claude, custom agents) and enterprise MCP servers (File System MCP, GitHub MCP, Database MCPs), AgentShield intercepts all incoming JSON-RPC requests and outgoing responses in real time. 

AgentShield enforces dynamic risk assessment, role-based access control (RBAC), Human-in-the-Loop (HITL) approval workflows for critical actions, Redis-backed rate limiting, response-side PII sanitization, and centralized PostgreSQL audit logging—all through an intuitive React Web Dashboard.

### 1.2 Problem Statement
The rapid enterprise adoption of LLMs and autonomous AI agents using MCP grants AI direct access to internal tools, databases, and APIs. However:
- **Hallucinations & Prompt Injection:** Autonomous agents can be tricked into executing unintended system commands or deleting database records.
- **Lack of Centralized Governance:** Existing MCP security is fragmented at individual server levels without global policy enforcement.
- **Absence of Real-time HITL Approvals:** High-risk actions (e.g., executing shell scripts, dropping database tables, transferring funds) run without human oversight.
- **Sensitive Data Leakage:** Responses returned to LLM context windows often contain raw API keys, passwords, Aadhaar numbers, PAN numbers, and personal identifiers.

AgentShield solves these problems by providing a zero-trust runtime interception gateway that enforces dynamic policy-driven security without requiring modifications to target MCP servers.

---

## 2. User Personas & System Roles

| Persona / Role | Description | Core Capabilities |
| :--- | :--- | :--- |
| **Security Administrator** | Enterprise Security Lead overseeing AI governance and compliance. | Manages security policies, reviews high-risk HITL approval queues, inspects audit logs, and monitors live traffic metrics. |
| **Developer / System Admin** | Engineers integrating AI agents with enterprise MCP tools. | Registers MCP servers, configures agent API credentials, sets rate limits, and monitors tool latency. |
| **AI Agent (Client)** | LLM orchestrators (OpenAI, Claude, Gemini, custom AutoGen/LangChain agents). | Emits JSON-RPC MCP requests (e.g., `tools/call`, `resources/read`) to AgentShield proxy. |
| **Target MCP Server** | Enterprise tools exposing capabilities via MCP protocol. | Executes authorized JSON-RPC requests forwarded by AgentShield and returns raw execution results. |

---

## 3. Functional Requirements (FRs)

### 3.1 Centralized Security Gateway (Gateway Interceptor)
- **FR-GW-01:** System SHALL act as a transparent JSON-RPC 2.0 reverse proxy between AI Clients and MCP Servers over HTTP/WebSockets/STDIO transport.
- **FR-GW-02:** System SHALL inspect every incoming MCP request (e.g., `tools/call`, `resources/read`, `prompts/get`) prior to forwarding to the target server.
- **FR-GW-03:** System SHALL preserve standard MCP JSON-RPC compliance without altering valid protocol structure for approved requests.
- **FR-GW-04:** System SHALL return standard JSON-RPC error frames (`code: -32000` to `-32099`) for requests blocked due to security violations, policy denial, or rate limits.

### 3.2 Dynamic Risk Assessment Engine
- **FR-RA-01:** System SHALL analyze every intercepted request payload against a multi-factor risk model and assign a Risk Category: `LOW`, `MEDIUM`, or `HIGH`.
- **FR-RA-02:** Risk scoring SHALL evaluate:
  - **Tool Sensitivity:** Write/Execute operations (e.g., `fs.write_file`, `github.delete_repo`, `db.execute_sql`) auto-escalate to `HIGH`.
  - **Parameter Payload Inspection:** Detect shell injection syntax, path traversal (`../`), SQL injection fragments, or prompt injection triggers.
  - **Contextual Anomaly:** Excessive tool invocation frequency or out-of-boundary parameters.
- **FR-RA-03:** `LOW` risk requests SHALL bypass HITL queues and proceed directly to authorization and rate limiting.
- **FR-RA-04:** `HIGH` risk requests SHALL automatically pause execution and be routed to the Human-in-the-Loop (HITL) approval queue.

### 3.3 Rule-Based & Role-Based Authorization Engine (RBAC)
- **FR-RB-01:** System SHALL enforce configurable access control policies mapping `AgentID`, `UserRole`, and `TargetTool`.
- **FR-RB-02:** System SHALL evaluate whether the requesting agent/user possesses the explicit permission to invoke the requested tool and parameters.
- **FR-RB-03:** System SHALL support dynamic policy updates via the React Admin Dashboard without requiring server restarts.

### 3.4 Human-in-the-Loop (HITL) Approval Module
- **FR-HI-01:** When a request is flagged as `HIGH` risk, the gateway SHALL hold the client HTTP/WebSocket connection open in a pending async state.
- **FR-HI-02:** System SHALL push the pending request to the Admin Dashboard in real time via WebSockets, displaying request details, agent identity, target tool, parameter payloads, and risk rationale.
- **FR-HI-03:** Security Admins SHALL have the capability to `APPROVE` or `DENY` requests with mandatory/optional audit comments.
- **FR-HI-04:** System SHALL support a configurable TTL timeout (default: 60 seconds). If an admin does not respond within the TTL, the request auto-fails with a `REQ_TIMEOUT_BLOCKED` status.

### 3.5 Redis-Based Rate Limiting & Loop Prevention
- **FR-RL-01:** System SHALL enforce sliding-window or token-bucket rate limits using Redis, configurable per Agent ID, IP address, or User Role.
- **FR-RL-02:** System SHALL detect rapid repetitive tool invocation loops (e.g., infinite agent recursion calling the same tool > 10 times in 5 seconds) and temporarily quarantine the agent.
- **FR-RL-03:** System SHALL return HTTP `429 Too Many Requests` or JSON-RPC Rate Limit Error when limits are exceeded.

### 3.6 Response Sanitization & Data Masking Engine
- **FR-RS-01:** System SHALL inspect raw execution responses returned by target MCP servers before delivering them to AI agents.
- **FR-RS-02:** System SHALL scan response text and JSON bodies for sensitive PII and credential patterns, including:
  - API Keys / Tokens (AWS, OpenAI, GitHub PATs)
  - Passwords & Secret hashes
  - Credit Card / Debit Card numbers (Luhn algorithm match)
  - Indian National Identifiers (Aadhaar number, PAN number)
  - Emails and Phone numbers (configurable per enterprise policy)
- **FR-RS-03:** System SHALL replace detected sensitive values with deterministic redaction tokens (e.g., `[REDACTED: AADHAAR_NUMBER]`, `[REDACTED: API_KEY]`).
- **FR-RS-04:** Sanitization activity SHALL be recorded in the audit trail indicating which fields were masked.

### 3.7 Centralized Audit Logging & Analytics
- **FR-AU-01:** System SHALL record every request/response transaction in PostgreSQL with timestamp, Agent ID, User Role, target MCP server, tool name, raw payload hash, risk level, policy decision, approval outcome, and processing latency.
- **FR-AU-02:** Audit records SHALL be immutable and queryable via administrative APIs.
- **FR-AU-03:** System SHALL generate aggregated security analytics (total traffic, blocked attempts, risk category breakdown, top targeted tools).

### 3.8 React Web Admin Dashboard
- **FR-UI-01:** Dashboard SHALL provide real-time visual monitoring of incoming MCP traffic, active agent sessions, and system health status.
- **FR-UI-02:** Dashboard SHALL feature an interactive **HITL Approval Queue** with notification badges and one-click Approve/Deny actions.
- **FR-UI-03:** Dashboard SHALL include a **Policy Management Suite** for creating, editing, and toggling RBAC rules and risk thresholds.
- **FR-UI-04:** Dashboard SHALL include a **Security Audit Log Explorer** with multi-parameter filtering (by date, agent, risk level, status).
- **FR-UI-05:** Dashboard SHALL implement **Firebase Authentication** for secure Admin login and session management.

---

## 4. System Architecture & Tech Stack

```
                                  AgentShield Security Gateway
                                 ┌─────────────────────────────┐
┌─────────────┐   JSON-RPC       │  1. Request Interceptor     │             ┌─────────────────┐
│  AI Agents  ├─────────────────►│  2. Dynamic Risk Assessment │────────────►│ Enterprise MCP  │
│ (OpenAI /   │   (Intercepted)  │  3. Rule Engine (RBAC)      │  (Approved) │ Servers (GitHub,│
│  Claude /   │                  │  4. Rate Limiter (Redis)    │             │ FileSystem, DB) │
│  Gemini)    │◄─────────────────┤  5. Response Sanitizer (PII)│◄────────────┤                 │
└─────────────┘   (Sanitized     └──────────────┬──────────────┘  Raw Response└─────────────────┘
                   Response)                    │ (High Risk)
                                                ▼
                                 ┌─────────────────────────────┐
                                 │ 6. HITL Approval Queue      │
                                 └──────────────┬──────────────┘
                                                │ Realtime WS
                                                ▼
                                 ┌─────────────────────────────┐
                                 │ 7. React Admin Dashboard    │
                                 │    (Firebase Auth / Audit)  │
                                 └─────────────────────────────┘
```

### Proposed Tech Stack

| Component | Technology Selected | Rationale |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI (Python 3.11+)** | High performance async I/O (`asyncio`), native OpenAPI schema generation, and seamless integration with PII regex engines. |
| **Frontend Framework** | **React (Vite + Tailwind CSS)** | Dynamic component re-rendering for live HITL queues, high responsiveness, and sleek UI. |
| **Authentication** | **Firebase Auth** | Industry-standard identity management for Security Admin dashboard access. |
| **Database** | **PostgreSQL (SQLAlchemy / Alembic)** | Relational integrity for immutable audit logs, policies, and agent role schemas. |
| **Cache & Rate Limiting**| **Redis (aioredis)** | In-memory atomic counters for sub-millisecond sliding-window rate limiting and async HITL event pub/sub. |
| **AI Clients & Test Tools**| **OpenAI / Claude / Gemini SDKs** | Target LLMs sending test MCP payloads. |
| **MCP Servers** | **Dummy MCP, FileSystem MCP, GitHub MCP** | Standard testbed for validating command interception and response PII masking. |

---

## 5. Non-Functional Requirements (NFRs) & Design Constraints

### 5.1 Architecture & Constitutional Constraints
- **LOC Gate Compliance:** In accordance with the `agentshield Constitution v1.0.0`, all backend Python modules and frontend React files MUST adhere to a strict limit of **$\le$ 200 Lines of Code (LOC)** per file.
- **TDD Requirement:** All features MUST be developed Test-First (`bmad-tea`), starting with failing PyTest unit/integration tests before writing implementation code.
- **Zero Modification to MCP Servers:** AgentShield MUST function as a clean proxy layer without requiring code changes or custom plugins installed on target MCP servers.

### 5.2 Performance & Latency
- **Proxy Latency Overhead:** Low/Medium-risk requests passing through interception, RBAC, rate-limiting, and response sanitization MUST introduce less than **30ms** total latency overhead.
- **Redis Rate Limiting:** Rate checks MUST complete in $< \mathbf{2ms}$.

### 5.3 Security & Compliance
- **Zero Credential Exposure:** API keys and credentials MUST never be stored in plain text or written to log files.
- **Session Protection:** Admin dashboard access MUST require valid Firebase JWT token authentication on all REST/WebSocket endpoints.

---

## 6. Success Metrics & Counter-Metrics

| Metric Category | Target Objective | Counter-Metric (To Prevent Negative Side Effects) |
| :--- | :--- | :--- |
| **Attack Interception Rate** | 100% of malicious path-traversal, shell injection, and unauthorized write calls intercepted. | Zero false-positive blocks on valid `LOW` risk read operations. |
| **Sensitive Data Redaction** | 100% masking of API keys, credit cards, Aadhaar, and PAN numbers in responses. | Zero corruption of valid structured JSON fields in MCP payloads. |
| **System Throughput** | Support $\ge 1,000$ concurrent MCP JSON-RPC requests/sec with Redis caching. | Maximum proxy CPU usage under 70% during peak load bursts. |
| **HITL Responsiveness** | Real-time WebSocket push to Admin Dashboard within $< 100\text{ms}$ of high-risk detection. | Client connection timeout auto-block executes reliably at 60s TTL. |

---

## 7. Approval & Sign-Off

- **Project Lead:** Harsh Manjramkar (VIT Computer Engineering)
- **Team Members:** Vedant Gaidhani, Vineet Wagh, Arjun Joshi
- **Faculty Guide:** Prof. Sanyukta Deshmukh
- **PRD Status:** Approved for Technical Architecture (`bmad-architecture`) & Implementation Plan.
