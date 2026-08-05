---
id: "5.1"
key: "5-1-pii-regex-engine"
epic_id: "EPIC-5"
title: "Response-Side PII Sanitization & Secret Redaction Engine"
status: "review"
created: "2026-08-05"
updated: "2026-08-05"
baseline_commit: "HEAD"
---

# Story 5.1: Response-Side PII Sanitization & Secret Redaction Engine

## Story Statement
**As an** AI Security Gateway Proxy,  
**I want to** inspect raw text and JSON response bodies returned by target MCP servers and redact sensitive PII and API credentials before delivering them to AI agents,  
**So that** LLM context windows never ingest raw API keys, passwords, Aadhaar numbers, PAN numbers, or credit card identifiers.

---

## Acceptance Criteria (BDD)

### Scenario 1: Redact API Keys & Access Tokens in Text & JSON Responses [COMPLETED]
- **Given** a raw MCP response body containing AWS keys (`AKIAIOSFODNN7EXAMPLE`), OpenAI keys (`sk-proj-...`), or GitHub PATs (`ghp_...`)
- **When** the payload passes through `src/sanitizer/pii_engine.py`
- **Then** all key strings are replaced with `[REDACTED: API_KEY]`
- **And** the surrounding JSON structure remains valid.

### Scenario 2: Redact Indian National Identifiers (Aadhaar & PAN Numbers) [COMPLETED]
- **Given** an MCP response payload containing a 12-digit Aadhaar number (`3675 8392 0192`) or a 10-character PAN string (`ABCDE1234F`)
- **When** the PII Engine scans the text/JSON body
- **Then** Aadhaar numbers are replaced with `[REDACTED: AADHAAR_NUMBER]`
- **And** PAN strings are replaced with `[REDACTED: PAN_NUMBER]`.

### Scenario 3: Redact Passwords & Credit Card Identifiers [COMPLETED]
- **Given** an MCP response containing password fields (`"password": "SuperSecret123!"`) or 16-digit credit card numbers
- **When** the PII Engine scans the payload
- **Then** credit card numbers are replaced with `[REDACTED: CREDIT_CARD]`
- **And** password values are replaced with `[REDACTED: SECRET]`.

---

## Tasks & Subtasks Progress
- [x] Task 1: Create unit tests for PII and Secret Redaction Engine (`tests/unit/test_pii_sanitizer.py`).
- [x] Task 2: Create integration tests for proxy response sanitization (`tests/integration/test_sanitizer_integration.py`).
- [x] Task 3: Implement `src/sanitizer/patterns.py` with compiled regex patterns for API Keys, Aadhaar, PAN, and Credit Cards.
- [x] Task 4: Implement `src/sanitizer/pii_engine.py` with recursive JSON/text transformer `sanitize_payload`.
- [x] Task 5: Wire `sanitize_payload` into `src/gateway/router.py` prior to returning proxy responses.
- [x] Task 6: Run full PyTest test suite and confirm 100% pass rate (27/27 tests passing).

---

## Dev Agent Record & Verification Log

### Verification Results
- **PyTest Results:** 27 passed in 0.64s
- **Constitutional LOC Check:** All files in `src/` are $< 70$ LOC (Constraint: $\le 200$ LOC per file).

### File List
- [`src/sanitizer/patterns.py`](file:///Users/harshm/Desktop/edi/src/sanitizer/patterns.py)
- [`src/sanitizer/pii_engine.py`](file:///Users/harshm/Desktop/edi/src/sanitizer/pii_engine.py)
- [`src/gateway/router.py`](file:///Users/harshm/Desktop/edi/src/gateway/router.py)
- [`tests/unit/test_pii_sanitizer.py`](file:///Users/harshm/Desktop/edi/tests/unit/test_pii_sanitizer.py)
- [`tests/integration/test_sanitizer_integration.py`](file:///Users/harshm/Desktop/edi/tests/integration/test_sanitizer_integration.py)
