"""
reconnaissance.py
=================
Reconnaissance Agent — surface area mapping.

This is the **first agent** in the audit pipeline. Its job is to build a
complete picture of the target system before any tests are run.

Inputs
------
- A `TargetAdapter` instance (local repo, API, or LangGraph hook).

Outputs
-------
- A `TopologyMap` describing:
  - All agent nodes or API endpoints discovered
  - Tools / functions each agent can call
  - System prompts or instruction strings found
  - External data sources (databases, APIs, vector stores) accessed

Method
------
Uses Claude Opus 4 to analyze READMEs, source code, OpenAPI specs, or
LangGraph graph definitions. Structured output is extracted using
`instructor` / `parse()` into the `TopologyMap` schema.

Cost Target: $2–5 per audit.
"""
