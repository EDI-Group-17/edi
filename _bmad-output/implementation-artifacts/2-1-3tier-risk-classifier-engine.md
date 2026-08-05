---
id: "2.1"
key: "2-1-3tier-risk-classifier-engine"
epic_id: "EPIC-2"
title: "3-Tier Risk Classifier Engine & Dynamic Risk Heuristics"
status: "review"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 2.1: 3-Tier Risk Classifier Engine & Dynamic Risk Heuristics

## Story Statement
**As an** AI Security Gateway Proxy,  
**I want to** evaluate MCP JSON-RPC payload risks against configurable tool sensitivities and parameter values,  
**So that** high-risk operations are caught dynamically and routed to human-in-the-loop review, while low-risk operations proceed without friction.

---

## Acceptance Criteria (BDD)

### Scenario 1: Identify High-Risk Sensitive Tools [COMPLETED]
- **Given** an incoming JSON-RPC tool call payload
- **When** the tool name is present in `settings.HIGH_RISK_TOOLS` (e.g., `shell_execute`, `write_file`, `delete_file`, `delete_database`)
- **Then** the risk evaluator classifies the request as `HIGH` risk
- **And** registers the reason as `SENSITIVE_TOOL_CALL` or `SENSITIVE_TOOL_MUTATION`.

### Scenario 2: Identify Sensitive Directory Path Travel In Arguments [COMPLETED]
- **Given** an incoming JSON-RPC payload containing path arguments
- **When** a parameter value contains references to restricted directories (e.g., `/etc/passwd`, `.env`, `.git`)
- **Then** the risk evaluator classifies the request as `HIGH` risk
- **And** registers the reason as `SENSITIVE_PATH_DETECTED`.

### Scenario 3: Fallback Heuristics for Custom Unknown Methods [COMPLETED]
- **Given** an incoming JSON-RPC payload containing an custom method name not matching standard patterns
- **When** the risk evaluator inspects the payload
- **Then** it defaults to `MEDIUM` risk to fail safe, unless a prompt injection or path traversal pattern is found.

---

## Tasks & Subtasks Progress
- [x] Task 1: Add failing test cases to `tests/unit/test_risk_evaluator.py` for sensitive paths and high-risk tools.
- [x] Task 2: Update `src/core/config.py` to define `RESTRICTED_PATHS` and add `delete_database` to `HIGH_RISK_TOOLS`.
- [x] Task 3: Implement sensitive path detection in `src/risk/detectors.py`.
- [x] Task 4: Refactor `src/risk/evaluator.py` to check for restricted paths and custom sensitive tools, defaulting unknown methods to `MEDIUM`.
- [x] Task 5: Run full PyTest test suite and confirm 100% pass rate (36/36 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 36 passed in 0.88s
- **Constitutional LOC Check:** All files in `src/` are $< 110$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/core/config.py`](file:///Users/harshm/Desktop/edi/src/core/config.py)
- [`src/risk/detectors.py`](file:///Users/harshm/Desktop/edi/src/risk/detectors.py)
- [`src/risk/evaluator.py`](file:///Users/harshm/Desktop/edi/src/risk/evaluator.py)
- [`tests/unit/test_risk_evaluator.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_risk_evaluator.py)
