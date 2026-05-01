"""
validators.py
=============
Quality gates for inter-agent data validation.

Agents trust their inputs to be correct Pydantic models, but this module
adds a second layer of business-rule validation *after* schema parsing —
catching issues that Pydantic alone cannot (e.g., an empty `TopologyMap`,
a `TestPlan` with zero test cases, or a `Finding` with no evidence).

Why This Exists
---------------
Long-running LLM pipelines can silently degrade: a hallucinated empty list
passes `list[Finding]` type checking but breaks the downstream compliance
mapper. These guards catch that class of failure early and loudly.

Key Functions
-------------
validate_topology_map(map: TopologyMap) -> None
    Raises `ValidationError` if no agents were discovered.

validate_test_plan(plan: TestPlan) -> None
    Raises `ValidationError` if the plan has fewer than 3 test cases.

validate_findings(findings: list[Finding]) -> None
    Raises `ValidationError` if any finding has an empty evidence dict
    or a missing remediation string.

validate_report(report: AuditReport) -> None
    Final gate before the synthesizer runs. Ensures cost and status fields
    are coherent.
"""
