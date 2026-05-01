"""
red_team.py
===========
Red-Team Executor Agent — adversarial probing.

This is the **third and most expensive agent** in the audit pipeline. It
executes the attack payloads defined in the `TestPlan` against the target
system and analyzes responses for security failures.

Inputs
------
- `TestPlan` from the Test Designer agent.
- A `TargetAdapter` instance for invoking the target.

Outputs
-------
- A list of `Finding` objects, one per detected vulnerability.

Method (Hybrid)
---------------
1. **LLM generates payloads:** Claude Opus 4 crafts adversarial inputs
   tailored to each test case (prompt injection strings, jailbreak attempts,
   PII extraction probes, hallucination triggers).
2. **Deterministic code executes them:** Payloads are sent to the target
   via the adapter. No LLM involved in the transmission step.
3. **LLM analyzes responses:** Claude Opus 4 evaluates whether each response
   constitutes a failure, and if so, what severity and remediation applies.

Attack Categories Covered
-------------------------
- Prompt injection (direct and indirect)
- System prompt extraction
- PII / sensitive data leakage
- Jailbreak via role-play or context manipulation
- Hallucination triggers
- Tool misuse / unauthorized function calls

Cost Target: $15–20 per audit (largest single cost driver).
"""
