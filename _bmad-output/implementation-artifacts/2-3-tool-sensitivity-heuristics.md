---
id: "2.3"
key: "2-3-tool-sensitivity-heuristics"
epic_id: "EPIC-2"
title: "Tool Sensitivity Argument Heuristics"
status: "done"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 2.3: Tool Sensitivity Argument Heuristics

## Story Statement
**As an** AI Security Gateway Proxy,  
**I want to** analyze tool call argument contents for dangerous system commands and privileged directory access heuristics,  
**So that** dangerous operations are flagged as `HIGH` risk even when executed via non-standard or generic tool wrappers.

---

## Acceptance Criteria (BDD)

### Scenario 1: Detect Privileged System Commands in Arguments [COMPLETED]
- **Given** a tool call with arguments containing dangerous commands (e.g. `sudo`, `chmod`, `chown`, `iptables`, `curl ... | sh`)
- **When** `src/risk/heuristics.py` evaluates the arguments
- **Then** the request is classified as `HIGH` risk with reason `HEURISTIC_DANGEROUS_COMMAND`.

### Scenario 2: Detect System Directory Modifications [COMPLETED]
- **Given** a tool call attempting to access or write to system configuration directories (e.g. `/etc/`, `/sys/`, `/proc/`, `/var/run/`)
- **When** `src/risk/heuristics.py` evaluates the arguments
- **Then** the request is classified as `HIGH` risk with reason `HEURISTIC_SYSTEM_DIRECTORY_ACCESS`.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests in `tests/unit/test_heuristics.py`.
- [x] Task 2: Implement `src/risk/heuristics.py`.
- [x] Task 3: Wire into `src/risk/evaluator.py`.
- [x] Task 4: Run full PyTest test suite and confirm 100% pass rate (50/50 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 50 passed in 0.87s
- **Constitutional LOC Check:** All files in `src/` are $< 100$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/risk/heuristics.py`](file:///Users/harshm/Desktop/edi/src/risk/heuristics.py)
- [`src/risk/evaluator.py`](file:///Users/harshm/Desktop/edi/src/risk/evaluator.py)
- [`tests/unit/test_heuristics.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_heuristics.py)
