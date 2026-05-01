"""
budget.py
=========
Real-time API cost tracker with hard budget enforcement.

Every LLM call in the system passes through this module before execution.
The `BudgetTracker` maintains a running tally of spend and exposes a gate
that the meta-agent uses to abort before a call that would exceed the cap.

Design
------
- Budget is set once at audit start from `AuditConfig.budget_usd`.
- Cost is calculated from token counts × model pricing after each LLM call.
- `gate_check()` is called *before* expensive operations — not after — so
  the system never silently overspends.

Key Classes / Functions
-----------------------
BudgetTracker
    Stateful tracker instantiated once per audit run.
    - `.record(model, prompt_tokens, completion_tokens)` — logs a completed call.
    - `.gate_check(estimated_cost)` — returns True if safe to proceed.
    - `.remaining` — property returning dollars left in the budget.
    - `.summary()` — returns a dict with total spent, per-agent breakdown.

MODEL_PRICING
    Dict mapping model names to (input_price_per_1k, output_price_per_1k).
    Must be kept in sync with Anthropic's published pricing.
"""
