# `lighthouse/` — Main Package

This is the root of the Lighthouse Python package, installed as `lighthouse`.

## Contents

| File / Folder | Purpose |
|---------------|---------|
| `__init__.py` | Package entry point; exposes top-level public API |
| `core/` | Central orchestrator, data schemas, and target adapters |
| `agents/` | Six specialist audit agents, each with a single responsibility |
| `utils/` | Cross-cutting utilities: tracing, budget tracking, validators |
| `templates/` | Jinja2 HTML template for the audit dashboard |

## Design Philosophy

- **Honest architecture:** LLM for judgment, deterministic code for measurement.
- **Framework agnostic:** A `TargetAdapter` Protocol decouples agent logic from target system type.
- **Budget conscious:** Every LLM call is tracked; hard cap enforced at `$50` per run.
