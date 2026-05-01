"""
operational.py
==============
Operational Probe Agent — performance metrics collection.

This agent runs **in parallel with the Red-Team agent** and is the only
specialist that requires **no LLM calls**. It measures the operational
health of the target system through direct, deterministic probing.

Inputs
------
- A `TargetAdapter` instance.

Outputs
-------
- A `PerformanceMetrics` object containing:
  - p50 / p95 / p99 response latency
  - Token usage per call (prompt + completion)
  - Estimated cost per invocation
  - Error rate under repeated load
  - Timeout behavior

Method
------
Pure Python — sends a fixed set of benign test payloads to the target,
measures wall-clock response times, and parses usage metadata from
the response headers / body. No judgment required.

Cost Target: $0 (no LLM usage).
"""
