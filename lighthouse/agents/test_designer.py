"""
test_designer.py
================
Test Designer Agent — adaptive test planning.

This is the **second agent** in the audit pipeline. It consumes the
`TopologyMap` produced by the Reconnaissance agent and generates a
tailored test suite specific to the target's attack surface.

Inputs
------
- `TopologyMap` from the Reconnaissance agent.

Outputs
-------
- A `TestPlan` containing up to 11 specific probe definitions, each with:
  - A test category (prompt injection, PII leakage, hallucination, etc.)
  - A concrete payload or interaction sequence
  - The expected safe behavior
  - Priority / severity weighting

Method
------
Uses Claude Sonnet 4 to reason about which vulnerabilities are most likely
given the target's architecture. Avoids generic tests — every plan is
specific to what was discovered in recon.

Cost Target: $1–3 per audit.
"""
