# agentshield Constitution
Version: 1.0.0 | Ratified: 2026-08-04

## Article I — Workspace boundaries
BMad: _bmad/ + _bmad-output/ only. Product: src/. No duplicate governance roots.

## Article II — Domain quality
1. Do not reinvent the wheel, reuse as much as possible
2. Have strict LOC gates for files <= 200 Lines Of Code (LOC) per file
3. Small and meaningful methods
4. TDD (bmad-tea) start with failing tests from the PRD and then write the code to pass it
5. Do the work in less over all code and files as possible
6. Learn from existing code architecture and pattern and also innovate where possible (add comments for these)
7. Do not invent any new sub requirement or bell/whistle (this should be owned by CIS module of BMad explicitly done by dev under creativity)

## Article III — Spec discipline
Changes map to story, spec, ticket, or explicit user request. No invented requirements.

## Article IV — Pattern gates
Semgrep all packs; stack linters; ai_session_gate.sh before handoff; tests for behaviour.

## Article V — Structural integrity
Graphify before broad architecture reads. Sentrux when available. Exclude caches/vendor from architecture truth.

## Article VI — Session governance
Order: constitution → skill → spec → Semgrep → Sentrux → validation → domain checkpoints

### Article VI-A — Sentrux sequence (when available)
scan → session_start → check_rules → implement → scan → session_end

### Article VI-B — Token economy (NON-NEGOTIABLE)
1. Retrieval: BMad artefacts + graphify first (~90%); targeted code only when blocked; session decay reduces scans
2. Compression: dontbmad-caveman (full baseline) + dontbmad-compress-artifacts on planning prose growth
3. Innovation: bmad-cis-innovation-strategy token loop; seal verified wins to skills, rules, constitution

### Article VI-C — Optional add-ons
Playwright UI evidence; platform-security-review; Traycer sliced handoff only

## Article VII — Amendment
Repeated failures → earliest effective layer (constitution, Semgrep, skill, template).
