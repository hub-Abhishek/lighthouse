"""
synthesizer.py
==============
Report Synthesizer Agent — final report generation.

This is the **last agent** in the audit pipeline. It consumes the completed
`AuditReport` (all findings + metrics) and produces the two user-facing
output artifacts.

Inputs
------
- A fully populated `AuditReport` object.

Outputs
-------
- `report.json` — The serialized `AuditReport` (Pydantic model dump).
  Machine-readable, suitable for downstream tooling or API responses.
- `dashboard.html` — A self-contained, static HTML file rendered from
  `templates/report.html` via Jinja2. No backend or CDN required.

Method
------
Uses Claude Sonnet 4 to write an executive summary aimed at C-suite
executives and compliance officers. Tone: professional, evidence-based,
no hype.

The LLM is instructed to:
1. State overall risk level (High / Medium / Low).
2. Highlight the top 3 critical findings with evidence.
3. Provide clear, actionable remediation steps.
4. Map key findings to specific regulatory articles.

Cost Target: $5–8 per audit.
"""
