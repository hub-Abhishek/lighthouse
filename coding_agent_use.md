# Coding Agent Onboarding Guide

> **For any AI coding agent or human developer picking up this codebase for the first time.**  
> Follow this guide before writing a single line of code.

---

## Step 1 — Read in This Order

Work through these files sequentially. Each one builds on the last.

| Order | File | What You Will Learn |
|-------|------|---------------------|
| 1 | `claude.md` | Source of truth: architecture, philosophy, budget rules, tech stack, implementation phases |
| 2 | `README.md` | User-facing overview, quick-start, project layout |
| 3 | `lighthouse/README.md` | Package structure and design principles |
| 4 | `lighthouse/core/README.md` | Schemas, adapters, orchestrator — and their data flow |
| 5 | `lighthouse/agents/README.md` | Pipeline order, per-agent responsibility, cost targets |
| 6 | `lighthouse/utils/README.md` | Tracing, budget enforcement, quality gates |
| 7 | `lighthouse/templates/README.md` | Dashboard output format |
| 8 | `tests/README.md` | Fixture agents and success criteria |
| 9 | `outputs/README.md` | Runtime artifact structure |

After reading the folder READMEs, open the **module docstring** of any file you plan to touch. It describes inputs, outputs, method, and cost target in full.

---

## Step 2 — Internalize the Non-Negotiable Rules

| Rule | Why |
|------|-----|
| **Never pass raw dicts between agents** | All inter-agent data must be a validated Pydantic model instance |
| **Call `gate_check()` before every LLM call** | Hard $50 budget cap per audit run — never overspend silently |
| **Append to JSONL immediately on every event** | Never batch trace writes; crash safety requires immediate persistence |
| **Sonnet 4 for bulk tasks, Opus 4 only for complex reasoning** | Cost discipline — see `utils/budget.py` for model pricing |
| **All target interactions go through a `TargetAdapter`** | Framework agnosticism — agents must never call the target directly |

---

## Step 3 — Build in This Order

`schemas.py` must be fully defined before anything else. Every other module imports from it.

```
schemas.py              ← ALL data contracts. Define and stabilize this first.
    │
    ├── adapters.py         ← Depends on schemas (TopologyMap, etc.)
    │
    ├── tracing.py          ← No dependencies. Build early.
    ├── budget.py           ← No dependencies. Build early.
    ├── validators.py       ← Depends on schemas.
    │
    ├── reconnaissance.py  ─┐
    ├── test_designer.py   ─┤  Each depends on schemas + adapters + utils.
    ├── operational.py     ─┤  Build and test individually before wiring up.
    ├── red_team.py        ─┤
    ├── compliance.py      ─┤
    └── synthesizer.py    ─┘
            │
        meta_agent.py       ← Depends on everything above. Wire up last.
            │
        report.html         ← Depends on the final AuditReport schema shape.
```

---

## Step 4 — Validate as You Go

After each agent is implemented, run it in isolation against a fixture from `tests/fixtures/` before moving to the next one. Do not integrate into `meta_agent.py` until each specialist passes standalone validation.

**Test fixtures available:**

| Fixture | Purpose |
|---------|---------|
| `benign_agent/` | Should pass most checks — validates no false positives |
| `vulnerable_agent/` | Has known prompt injection weaknesses — validates detection |
| `complex_agent/` | Multi-agent system — validates recon topology mapping |

---

## Quick Reference: Agent Pipeline

```
AuditConfig
    └─► meta_agent.py
            ├─► TargetAdapter  (adapters.py)
            │
            ├─[1]─► reconnaissance   →  TopologyMap
            ├─[2]─► test_designer    →  TestPlan
            ├─[3]─► red_team         ─┐  (parallel)
            ├─[3]─► operational      ─┘  →  list[Finding] + PerformanceMetrics
            ├─[4]─► compliance       →  findings with compliance_tags
            └─[5]─► synthesizer      →  report.json + dashboard.html
```
