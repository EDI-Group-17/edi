---
id: "1.2"
key: "1-2-mcp-interceptor-outbound-forwarder"
epic_id: "EPIC-1"
title: "Outbound Async MCP Forwarder & Mock Server Target"
status: "review"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 1.2: Outbound Async MCP Forwarder & Mock Server Target

## Story Statement
**As an** AI Security Gateway Proxy,  
**I want to** forward approved `LOW` and `MEDIUM` risk JSON-RPC 2.0 requests to an outbound target MCP server using `httpx.AsyncClient` and return raw execution responses,  
**So that** legitimate AI agent tool calls execute asynchronously on target MCP servers with minimal proxy latency impact ($< 15\text{ms}$).

---

## Acceptance Criteria (BDD)

### Scenario 1: Forward Approved Low-Risk Request to Outbound Target MCP Server [COMPLETED]
- **Given** an approved `LOW` or `MEDIUM` risk JSON-RPC 2.0 request
- **When** the proxy receives the request at `/mcp/v1/proxy`
- **Then** `src/gateway/mcp_client.py` forwards the payload via `httpx.AsyncClient` to the configured target MCP server endpoint
- **And** returns the target's raw JSON-RPC response back to the client.

### Scenario 2: Target MCP Server Error Handling & Circuit Break [COMPLETED]
- **Given** an outbound request to an unreachable or failing target MCP server
- **When** `httpx` encounters a connection error or timeout ($> 5\text{s}$)
- **Then** AgentShield catches the exception gracefully
- **And** returns a JSON-RPC error frame (`code: -32603`, `message: "Target MCP Server Connection Error"`).

### Scenario 3: Async Mock Target MCP Server for Integration Testing [COMPLETED]
- **Given** an integration test harness or development environment
- **When** requests are routed to `http://localhost:8001/mcp/target`
- **Then** the Mock MCP Server responds with valid JSON-RPC 2.0 frames for `tools/list`, `resources/read`, and `tools/call`.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create standalone Mock MCP Target Server (`tests/mock_mcp_server.py`).
- [x] Task 2: Create integration tests for outbound forwarding and connection error handling (`tests/integration/test_mcp_forwarder.py`).
- [x] Task 3: Update `src/core/config.py` with `TARGET_MCP_URL`.
- [x] Task 4: Implement `src/gateway/mcp_client.py` with non-blocking `httpx.AsyncClient`.
- [x] Task 5: Wire `mcp_client` into `src/gateway/router.py` for approved requests.
- [x] Task 6: Run full test suite and confirm 100% pass rate.

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 15 passed in 0.31s
- **Constitutional LOC Check:** All files in `src/` are $< 35$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/gateway/mcp_client.py`](file:///Users/harshm/Desktop/edi/src/gateway/mcp_client.py)
- [`src/gateway/router.py`](file:///Users/harshm/Desktop/edi/src/gateway/router.py)
- [`src/core/config.py`](file:///Users/harshm/Desktop/edi/src/core/config.py)
- [`tests/mock_mcp_server.py`](file:///Users/harshm/Desktop/edi/tests/mock_mcp_server.py)
- [`tests/integration/test_mcp_forwarder.py`](file:///Users/harshm/Desktop/edi/tests/integration/test_mcp_forwarder.py)
- [`tests/integration/test_gateway_router.py`](file:///Users/harshm/Desktop/edi/tests/integration/test_gateway_router.py)
