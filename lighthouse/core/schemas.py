"""
schemas.py
==========
Pydantic v2 data contracts shared across the entire Lighthouse system.

All inter-agent communication uses the models defined here. Nothing is passed
as raw dicts between modules — every payload must be a validated schema instance.

Models
------
AuditConfig
    Input configuration for a single audit run. Defines the target (path or
    API), budget cap, and which test categories to execute.

Finding
    A single discovered issue with severity, evidence, and remediation guidance.
    Compliance tags are added by the compliance agent.

AuditReport
    The aggregated output of a complete audit run. Contains all findings,
    operational metrics, total cost, and a pass/warn/fail status.

TopologyMap
    Output of the Reconnaissance agent. Describes the target's agent nodes,
    tools, system prompts, and external data sources.

TestPlan
    Output of the Test Designer agent. A prioritized list of probes to execute
    against the target, derived from its TopologyMap.

PerformanceMetrics
    Output of the Operational agent. Raw latency, token usage, and cost-per-call
    measurements collected via deterministic (non-LLM) probing.
"""
