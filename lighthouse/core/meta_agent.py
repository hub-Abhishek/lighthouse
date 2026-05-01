"""
meta_agent.py
=============
Central orchestrator for the Lighthouse audit system.

This is the top-level entry point for running an audit. It is responsible for:

1. Loading and validating an `AuditConfig`.
2. Selecting and instantiating the appropriate `TargetAdapter` (local repo,
   API endpoint, or LangGraph hook).
3. Calling each specialist agent in the correct sequence:
       Reconnaissance → Test Designer → Red-Team + Operational (parallel)
       → Compliance Mapper → Synthesizer
4. Enforcing budget gates before every expensive LLM call.
5. Aggregating all agent outputs into a final `AuditReport`.

Key Functions
-------------
plan_audit(config: AuditConfig) -> TestPlan
    Runs Reconnaissance and Test Designer. Returns a ready-to-execute plan.

execute_audit(plan: TestPlan) -> AuditReport
    Runs all remaining agents and produces the final report.

gate_check(current_cost: float, budget: float) -> bool
    Returns True if there is sufficient budget to continue. Called before
    every agent invocation.
"""
