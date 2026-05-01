# `agents/` — Specialist Audit Agents

Each module is a **single-responsibility agent** in the audit pipeline. Agents are called sequentially by `core/meta_agent.py` and communicate through shared Pydantic schemas.

## Pipeline Order

```
reconnaissance  →  test_designer  →  red_team
                                         ↓
                              operational (parallel)
                                         ↓
                                    compliance
                                         ↓
                                    synthesizer
```

## Agent Summaries

| File | Responsibility | LLM? | Cost Target |
|------|---------------|------|-------------|
| `reconnaissance.py` | Discovers agents, tools, prompts, and data sources in the target system | ✅ Opus 4 | $2–5 |
| `test_designer.py` | Generates a tailored 11-check `TestPlan` based on the target's attack surface | ✅ Sonnet 4 | $1–3 |
| `red_team.py` | Generates adversarial payloads and analyzes target responses for failures | ✅ Opus 4 | $15–20 |
| `operational.py` | Measures latency, cost-per-call, and token usage — **no LLM needed** | ❌ Pure Python | $0 |
| `compliance.py` | Tags findings against EU AI Act, NIST AI RMF, and OWASP LLM Top 10 | ✅ Sonnet 4 (fallback) | $3–5 |
| `synthesizer.py` | Generates executive summary and renders the final HTML dashboard | ✅ Sonnet 4 | $5–8 |

## Input / Output Convention

Every agent follows this interface pattern:

```python
async def run(input: <AgentInput>, adapter: TargetAdapter, budget: BudgetTracker) -> <AgentOutput>:
    ...
```
