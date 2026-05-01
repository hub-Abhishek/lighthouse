# Lighthouse 🔦

**AI Agent Auditing System** — meta-agentic infrastructure that stress-tests and red-teams AI agents to produce enterprise-grade safety assurance reports.

## What This Is

Lighthouse audits opaque AI systems across 6 dimensions:

| Dimension | Agent | Cost Target |
|-----------|-------|-------------|
| Reconnaissance | `agents/reconnaissance.py` | $2–5 |
| Test Design | `agents/test_designer.py` | $1–3 |
| Red-Teaming | `agents/red_team.py` | $15–20 |
| Operational | `agents/operational.py` | $0 |
| Compliance | `agents/compliance.py` | $3–5 |
| Reporting | `agents/synthesizer.py` | $5–8 |

**Hard budget limit: $50 per audit run.**

## Project Layout

```
lighthouse/
├── README.md               ← You are here
├── claude.md               ← Project specification and instructions
├── pyproject.toml          ← Dependencies (Poetry / uv)
├── lighthouse/             ← Main Python package
│   ├── core/               ← Orchestrator, schemas, adapters
│   ├── agents/             ← Specialist audit agents
│   ├── utils/              ← Tracing, budget, validation utilities
│   └── templates/          ← HTML dashboard template
├── tests/
│   └── fixtures/           ← Sample target agents for testing
└── outputs/
    └── audits/             ← Generated audit reports (JSON + HTML)
```

## Quick Start

```bash
# Install dependencies
uv install   # or: poetry install

# Run an audit against a local agent repo
lighthouse audit ./my-agent --budget 50

# Run an audit against an API endpoint
lighthouse audit --api https://my-agent.example.com/invoke
```

## Tech Stack

- **Python** 3.11+
- **LLM:** Anthropic SDK — Claude Opus 4 (reasoning), Sonnet 4 (bulk tasks)
- **Validation:** Pydantic v2
- **Concurrency:** `asyncio.gather()`
- **Storage:** JSONL audit trails, JSON structured outputs
- **Frontend:** Static HTML/JS dashboard (no backend required)
