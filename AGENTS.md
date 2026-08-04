# AGENTS.md — agentshield

Loader for AI agents. Constitution wins on conflict.

## Tracks
quick-flow | bmad-method | **platinum (Rock)** | enterprise

## Layered defense (every session)
1. Feed forward: constitution + relevant skill + story/spec + **graphify before broad read**
2. Real-time: Semgrep (.semgrep/), linters, Sentrux MCP/CLI if available
3. Feed backward: ai_session_gate.sh --changed; checkpoint; promote repeated mistakes

## Token economy (Article VI-B) — mandatory
1. ~90% retrieval from BMad artefacts + graphify; refresh graph on gap; narrow code read only when blocked
2. dontbmad-caveman (full) + dontbmad-compress-artifacts continuous baseline
3. bmad-cis-innovation-strategy token loop; seal wins to skills/rules/constitution

## Platinum
Invoke Rock (@bmad-agent-rock). SSOT: {epic-id}-platinum-runbook.md.
Sprint truth: _bmad-output/implementation-artifacts/sprint-status.yaml

## Gates before handoff
bash scripts/ai_session_gate.sh --changed [--cursor-strict]
