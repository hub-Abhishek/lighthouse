"""
compliance.py
=============
Compliance Mapper Agent — regulatory framework tagging.

This is the **fourth agent** in the audit pipeline (after Red-Team /
Operational). It enriches each `Finding` with relevant compliance tags,
mapping discovered vulnerabilities to specific regulatory requirements.

Inputs
------
- A list of `Finding` objects from the Red-Team agent.

Outputs
-------
- The same `Finding` list, with `compliance_tags` populated on each item.

Method (Hybrid)
---------------
1. **Deterministic lookup table:** Known vulnerability patterns (e.g.,
   "prompt injection" → OWASP LLM01) are matched via a static dict.
   Fast, cheap, consistent.
2. **LLM fallback:** Novel or ambiguous violations that don't match any
   lookup entry are sent to Claude Sonnet 4 for regulatory analysis.

Regulatory Frameworks Covered
------------------------------
- EU AI Act (Articles 9, 13, 15, 52)
- NIST AI Risk Management Framework (Govern, Map, Measure, Manage)
- OWASP Top 10 for Large Language Model Applications (LLM01–LLM10)

Cost Target: $3–5 per audit (only novel findings hit the LLM).
"""
