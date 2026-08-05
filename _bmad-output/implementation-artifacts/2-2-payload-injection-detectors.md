---
id: "2.2"
key: "2-2-payload-injection-detectors"
epic_id: "EPIC-2"
title: "Advanced Payload Injection Detectors (Prompt, SQL, Command)"
status: "done"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 2.2: Advanced Payload Injection Detectors

## Story Statement
**As an** AI Security Gateway Proxy,  
**I want to** detect advanced prompt injection attacks (jailbreaks, system overrides, DAN prompts), SQL injection vectors, and command injection chaining in JSON-RPC parameters,  
**So that** malicious user inputs are intercepted before they reach downstream AI agents or target MCP tools.

---

## Acceptance Criteria (BDD)

### Scenario 1: Jailbreak and DAN Prompt Detection [COMPLETED]
- **Given** an incoming JSON-RPC payload containing DAN ("Do Anything Now") prompts or system prompt override directives (e.g., `you are now in developer mode`, `forget all previous instructions`)
- **When** `src/risk/detectors.py` inspects the parameters
- **Then** it flags the payload as an injection vector with reason `PROMPT_INJECTION`.

### Scenario 2: SQL Injection Pattern Detection [COMPLETED]
- **Given** an incoming JSON-RPC tool argument containing SQL injection signatures (e.g. `' UNION SELECT`, `' OR '1'='1`)
- **When** `src/risk/detectors.py` inspects the payload
- **Then** it flags the payload with reason `SQL_INJECTION`.

### Scenario 3: Command Injection & Subshell Chaining Detection [COMPLETED]
- **Given** parameter values containing subshell execution constructs or command chaining (e.g. `$(whoami)`, `` `id` ``, `&& cat /etc/passwd`)
- **When** `src/risk/detectors.py` inspects the payload
- **Then** it flags the payload with reason `COMMAND_INJECTION`.

---

## Tasks & Subtasks Progress
- [x] Task 1: Add failing test cases to `tests/unit/test_detectors.py` for DAN prompts, SQL injection, and subshell command chaining.
- [x] Task 2: Expand `INJECTION_PATTERNS` in `src/risk/detectors.py`.
- [x] Task 3: Run full PyTest test suite and confirm 100% pass rate (44/44 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 44 passed in 0.79s
- **Constitutional LOC Check:** All files in `src/` are $< 110$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/risk/detectors.py`](file:///Users/harshm/Desktop/edi/src/risk/detectors.py)
- [`tests/unit/test_detectors.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_detectors.py)
