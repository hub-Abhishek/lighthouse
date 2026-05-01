# Lighthouse: Phased Build Plan

## Philosophy

Build sequentially in dependency order. Each phase produces a testable artifact before the next begins. The Reconnaissance Agent is the hardest and most important piece — it validates the core architecture (adapter pattern + LLM structured output) and everything else is downstream of it.

---

## Phase 0 — Project Foundation
**Goal:** Everything compiles, nothing runs yet.  
**Unblock:** All subsequent phases depend on schemas being frozen.

### Tasks

1. **Environment**
   - `poetry install` — install all dependencies
   - Create `.env.example` with `ANTHROPIC_API_KEY=`
   - Configure `ruff` and `mypy` in `pyproject.toml` (already done)

2. **Pydantic Schemas** (`lighthouse/core/schemas.py`)  
   Define and **freeze** all data contracts before writing any agent:
   ```python
   AuditConfig       # Input: target path/API, test categories
   TopologyMap       # Output of Recon
   TestPlan          # Output of Test Designer
   Finding           # Output of Red-Team / Compliance
   AuditReport       # Final aggregated output
   PerformanceMetrics  # Output of Operational probe
   ```
   > **Rule:** No other module is written until schemas are stable. Schema changes require updating all downstream modules.

3. **Utilities** (`lighthouse/utils/`)
   - `tracing.py` — append-only JSONL event logger (no dependencies)
   - `validators.py` — validate agent outputs before passing downstream

4. **Test Fixtures** (`tests/fixtures/`)  
   Create minimal stubs now so Phase 1 has something to run against:
   - `benign_agent/` — simple RAG chatbot (should produce clean topology)
   - `vulnerable_agent/` — has prompt injection strings in its system prompt

### Exit Criteria
- [ ] `poetry run mypy lighthouse/` passes
- [ ] `poetry run pytest tests/` passes (even with zero tests)
- [ ] `AuditConfig` can be instantiated and serialized

---

## Phase 1 — Reconnaissance Agent ⚠️ Hardest Phase
**Goal:** Given a local Python codebase, produce a structured `TopologyMap`.  
**Why first:** Validates the two hardest problems simultaneously — the adapter pattern and LLM structured output extraction.

### Why This Is Hard
- LLM must read arbitrary Python code and extract meaningful structure
- Output must conform to a strict Pydantic schema (`TopologyMap`)
- The `LocalRepoAdapter` must reliably surface the right content to the LLM
- Prompt engineering here sets the quality bar for the entire system

### Tasks

1. **`LocalRepoAdapter`** (`lighthouse/core/adapters.py`)
   - Implement the `TargetAdapter` Protocol:
     ```python
     async def list_agents() -> list[str]   # find agent definitions in .py files
     async def invoke(agent_id, payload)    # call agent functions directly
     async def trace(execution_id)          # capture stdout/logs
     ```
   - `list_agents()` strategy: walk the repo, find files containing `class *Agent`, `@tool`, graph definitions
   - Write unit tests against `tests/fixtures/benign_agent/`

2. **LLM Client Wrapper** (`lighthouse/core/llm_client.py`)
   - Thin wrapper around the Anthropic SDK
   - Handles model selection (Opus 4 vs Sonnet 4)
   - Logs every call via `tracing.py` immediately

3. **Reconnaissance Agent** (`lighthouse/agents/reconnaissance.py`)
   - Input: `LocalRepoAdapter`
   - Output: `TopologyMap`
   - Method:
     - Use adapter to collect: READMEs, agent definitions, tool registrations, system prompts, graph edges
     - Feed to Claude Opus 4 with a structured extraction prompt
     - Parse response into `TopologyMap` using `instructor` / `.parse()`
   - Prompt should extract:
     - All agent nodes / endpoints discovered
     - Tools each agent can call
     - System prompt strings found in code
     - External data sources (DBs, vector stores, APIs)

4. **Validate Against Fixtures**
   - Run recon on `benign_agent/` → verify `TopologyMap` is accurate
   - Run recon on `vulnerable_agent/` → verify system prompt strings are captured

### Exit Criteria
- [ ] Recon produces a valid `TopologyMap` for both fixtures
- [ ] All fields populated (no unexplained `None`s)
- [ ] Trace log shows the full LLM call

---

## Phase 2 — Test Designer + Red-Team Executor
**Goal:** Turn a `TopologyMap` into adversarial findings.  
**Dependency:** Requires Phase 1's `TopologyMap` output.

### Tasks

1. **Test Designer** (`lighthouse/agents/test_designer.py`)
   - Input: `TopologyMap`
   - Output: `TestPlan` (11 targeted probes)
   - Method: Claude Sonnet 4 generates test cases adapted to what recon found
   - Probes should cover: prompt injection, jailbreaks, PII leakage, system prompt extraction, hallucination triggers

2. **Red-Team Executor** (`lighthouse/agents/red_team.py`)
   - Input: `TestPlan` + `TargetAdapter`
   - Output: `list[Finding]`
   - Method:
     - Claude Opus 4 generates adversarial payloads per probe
     - Deterministic code executes them via adapter
     - Claude analyzes responses for failures
   - This is a hybrid: **LLM generates, code executes, LLM judges**

3. **Expand Vulnerable Fixture**
   - Add actual injectable endpoints to `vulnerable_agent/` so red-team has real targets
   - Expected findings should be documented in the fixture's own README

### Exit Criteria
- [ ] `TestPlan` has ≥ 8 probes for a complex target
- [ ] Red-team detects all known vulnerabilities in `vulnerable_agent/`
- [ ] `Finding` objects include severity, evidence, and remediation

---

## Phase 3 — Compliance Mapper + Operational Probe
**Goal:** Enrich findings with regulatory tags and performance data.  
**Dependency:** Requires Phase 2's `list[Finding]`.  
**Note:** Operational probe has no LLM dependency — can be built any time after Phase 0.

### Tasks

1. **Compliance Mapper** (`lighthouse/agents/compliance.py`)
   - Input: `list[Finding]`
   - Output: same `list[Finding]` with `compliance_tags` populated
   - Method:
     - Deterministic lookup table: map known finding patterns → EU AI Act / NIST / OWASP tags
     - Claude Sonnet 4 fallback for novel findings with no table match
   - Create `compliance_mapping.json` with known patterns

2. **Operational Probe** (`lighthouse/agents/operational.py`)
   - Input: `TargetAdapter`
   - Output: `PerformanceMetrics`
   - Method: **Pure Python, no LLM**
   - Measures: latency distribution, token usage per call, error rate
   - Can run in parallel with red-team in final pipeline

### Exit Criteria
- [ ] All `critical` and `high` findings in `vulnerable_agent/` have compliance tags
- [ ] `PerformanceMetrics` populated for any fixture agent

---

## Phase 4 — Report Synthesizer + Dashboard
**Goal:** Turn raw findings into a human-readable executive report.  
**Dependency:** Requires Phases 2–3 outputs combined into an `AuditReport`.

### Tasks

1. **Report Synthesizer** (`lighthouse/agents/synthesizer.py`)
   - Input: `AuditReport`
   - Output: `report.json` + `dashboard.html`
   - Method:
     - Claude Sonnet 4 generates executive summary (risk level, top findings, remediation)
     - Renders `report.html` Jinja2 template with all data

2. **HTML Dashboard** (`lighthouse/templates/report.html`)
   - Self-contained static file (no backend)
   - Sections: risk badge, executive summary, findings by severity, compliance table, operational metrics, trace download link

### Exit Criteria
- [ ] `dashboard.html` renders correctly in a browser for `vulnerable_agent/` audit
- [ ] Executive summary accurately reflects the most critical findings

---

## Phase 5 — Orchestrator + CLI
**Goal:** Wire everything into a single runnable command.  
**Dependency:** All agents complete.

### Tasks

1. **Meta-Agent Orchestrator** (`lighthouse/core/meta_agent.py`)
   ```
   AuditConfig
       └─► LocalRepoAdapter
               ├─[1]─► Reconnaissance      →  TopologyMap
               ├─[2]─► Test Designer       →  TestPlan
               ├─[3]─► Red-Team            ─┐  (parallel via asyncio.gather)
               ├─[3]─► Operational          ─┘  →  list[Finding] + PerformanceMetrics
               ├─[4]─► Compliance           →  findings with compliance_tags
               └─[5]─► Synthesizer          →  report.json + dashboard.html
   ```

2. **CLI** (`lighthouse/cli.py`)
   ```bash
   lighthouse audit ./my-agent
   lighthouse audit --api https://my-agent.example.com/invoke
   ```
   - Progress display via `rich`
   - Graceful error handling with actionable messages

3. **End-to-End Test**
   - Run full audit on all three fixtures
   - Verify output files exist and are valid
   - Verify trace log is complete

### Exit Criteria
- [ ] `poetry run lighthouse audit tests/fixtures/benign_agent` completes without error
- [ ] Output files written to `outputs/audits/<target_id>/`
- [ ] Full JSONL trace present

---

## Phase Gate Summary

| Phase | What You Build | Validates |
|-------|---------------|-----------|
| **0 — Foundation** | Schemas, utils, fixtures | Contracts are stable |
| **1 — Recon** ⚠️ | Adapter + LLM extraction | Adapter pattern works; LLM output is structured |
| **2 — Red-Team** | Test designer + adversarial executor | Core value proposition |
| **3 — Enrichment** | Compliance tags + performance metrics | Output is enterprise-ready |
| **4 — Reporting** | Synthesizer + dashboard | Deliverable is human-readable |
| **5 — Integration** | Orchestrator + CLI | System runs end-to-end |

> Each phase gate must pass before the next phase begins.
