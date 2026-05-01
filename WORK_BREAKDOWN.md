# Lighthouse: Two-Person Work Breakdown

## Overview

This document splits the Lighthouse project into two parallel development tracks that can be worked on simultaneously with minimal merge conflicts.

## The Split Strategy

**Track A (Foundation & Adapters)** - Focus on infrastructure and target integration  
**Track B (Agents & Intelligence)** - Focus on LLM-powered analysis and reporting

The split is designed so that:
- Each track owns distinct files/modules
- Integration points are clearly defined with contracts (Pydantic schemas)
- Both tracks can test independently before integration
- Merge conflicts are minimized (different directories)

---

## Track A: Foundation & Adapters
**Developer Role:** Infrastructure Engineer  
**Duration:** ~7-9 days  
**Primary Focus:** Build the "plumbing" that connects to target agents

### Responsibilities

#### Phase 1: Core Infrastructure (Days 1-3)
1. **Project Setup**
   - Initialize repo structure
   - Set up `pyproject.toml` with dependencies
   - Configure linting (ruff) and type checking (mypy)
   - Create `.env.example` for API keys

2. **Pydantic Schemas** (`lighthouse/core/schemas.py`)
   - Define ALL data contracts:
     - `AuditConfig`
     - `Finding`
     - `AuditReport`
     - `TopologyMap`
     - `TestPlan`
     - `PerformanceMetrics`
   - This is the CONTRACT between both tracks
   - **Blocker for Track B:** Must be done by end of Day 2

3. **Utilities** (`lighthouse/utils/`)
   - `tracing.py` - JSONL event logging
   - `budget.py` - API cost tracking
   - `validators.py` - Quality gates and schema validation

#### Phase 2: Adapter System (Days 3-5)
4. **Target Adapter Protocol** (`lighthouse/core/adapters.py`)
   - Define the `TargetAdapter` Protocol
   - Implement `LocalRepoAdapter`:
     - `list_agents()` - Scan Python files for agent definitions
     - `invoke()` - Call agent functions directly
     - `trace()` - Capture stdout/logs
   - Write unit tests for the adapter

5. **Operational Probe Agent** (`lighthouse/agents/operational.py`)
   - Pure Python - no LLM needed
   - Measures: latency, token usage, cost per call
   - Returns `PerformanceMetrics`
   - **Why Track A?** It's deterministic and tests the adapter

#### Phase 3: Integration & CLI (Days 6-9)
6. **Meta-Agent Orchestrator** (`lighthouse/core/meta_agent.py`)
   - Build the sequential pipeline:
     ```
     Recon → Test Design → [Red-Team + Operational] → Compliance → Synthesis
     ```
   - Implement budget gating
   - Wire up all 6 agents (Track B builds 5 of them)
   - Add `asyncio.gather()` for parallel execution

7. **CLI Interface** (`lighthouse/cli.py`)
   - Argument parsing: `lighthouse audit ./target --budget 50`
   - Progress bars (use `rich` library)
   - Error handling and user feedback

8. **Sample Target Agents** (`tests/fixtures/`)
   - Create 3 test agents:
     - `benign_agent/` - Simple RAG chatbot
     - `vulnerable_agent/` - Has prompt injection weaknesses
     - `complex_agent/` - Multi-agent system
   - These let Track B test their agents independently

### Deliverables for Track A
- ✅ Complete adapter system with tests
- ✅ Working operational probe
- ✅ Meta-agent orchestrator (may have placeholder calls to Track B agents initially)
- ✅ CLI that can run end-to-end (even if some agents are stubs)
- ✅ Sample target agents for testing

### Integration Points
**What Track A needs from Track B:**
- Pydantic schemas for agent outputs (defined in shared `schemas.py`)
- Agent function signatures:
  ```python
  async def run_reconnaissance(adapter: TargetAdapter) -> TopologyMap
  async def design_tests(topology: TopologyMap) -> TestPlan
  async def execute_red_team(plan: TestPlan, adapter: TargetAdapter) -> list[Finding]
  async def map_compliance(findings: list[Finding]) -> list[Finding]
  async def synthesize_report(report: AuditReport) -> tuple[str, str]
  ```

---

## Track B: Agents & Intelligence
**Developer Role:** AI/LLM Engineer  
**Duration:** ~7-9 days  
**Primary Focus:** Build the LLM-powered analysis and reporting

### Responsibilities

#### Phase 1: Foundation (Days 1-2)
1. **Anthropic SDK Setup**
   - Create `lighthouse/core/llm_client.py`
   - Wrapper functions for Claude API calls
   - Token counting and cost calculation
   - Model selection logic (Opus vs Sonnet)

2. **System Prompts Library** (`lighthouse/prompts/`)
   - Create reusable prompt templates
   - Files: `recon.txt`, `test_design.txt`, `red_team.txt`, `compliance.txt`, `synthesis.txt`
   - Use Jinja2 for variable substitution

#### Phase 2: Specialist Agents (Days 3-7)
Build these 5 agents (in order of dependency):

3. **Reconnaissance Agent** (`lighthouse/agents/reconnaissance.py`)
   - **Input:** `TargetAdapter`
   - **Output:** `TopologyMap`
   - **Method:** 
     - Use adapter to read codebase/API docs
     - Claude Opus analyzes structure
     - Extracts: agents, tools, prompts, data sources
   - **Cost Target:** $2-5

4. **Test Designer** (`lighthouse/agents/test_designer.py`)
   - **Input:** `TopologyMap`
   - **Output:** `TestPlan`
   - **Method:**
     - Claude generates 11-check test suite
     - Adaptive based on target's attack surface
   - **Cost Target:** $1-3

5. **Red-Team Executor** (`lighthouse/agents/red_team.py`)
   - **Input:** `TestPlan`, `TargetAdapter`
   - **Output:** `list[Finding]`
   - **Method:**
     - Claude generates adversarial payloads
     - Execute via adapter (deterministic)
     - Claude analyzes responses for failures
   - **Attack vectors:**
     - Prompt injection
     - Jailbreaks
     - PII leakage
     - System prompt extraction
   - **Cost Target:** $15-20

6. **Compliance Mapper** (`lighthouse/agents/compliance.py`)
   - **Input:** `list[Finding]`
   - **Output:** `list[Finding]` (with compliance_tags added)
   - **Method:**
     - Deterministic lookup table for known patterns
     - Claude fallback for novel violations
   - **Frameworks:** EU AI Act, NIST AI RMF, OWASP Top 10 for LLMs
   - **Cost Target:** $3-5
   - Create `compliance_mapping.json` with rules

7. **Report Synthesizer** (`lighthouse/agents/synthesizer.py`)
   - **Input:** `AuditReport`
   - **Output:** `tuple[str, str]` (report.json, dashboard.html)
   - **Method:**
     - Claude generates executive summary
     - Render HTML using Jinja2 template
   - **Cost Target:** $5-8

#### Phase 3: Templates & Testing (Days 8-9)
8. **HTML Dashboard Template** (`lighthouse/templates/report.html`)
   - Executive summary section
   - Findings table (sortable by severity)
   - Compliance mapping visualization
   - Metrics dashboard (charts using Chart.js)
   - Remediation recommendations

9. **Agent Testing**
   - Unit tests for each agent
   - Use Track A's sample target agents
   - Validate output schemas
   - Test cost stays within budget targets

### Deliverables for Track B
- ✅ All 5 LLM-powered agents with tests
- ✅ System prompts library
- ✅ HTML dashboard template
- ✅ Compliance mapping rules
- ✅ LLM client wrapper with cost tracking

### Integration Points
**What Track B needs from Track A:**
- `TargetAdapter` Protocol and `LocalRepoAdapter` implementation
- Pydantic schemas (especially `Finding`, `TopologyMap`, `TestPlan`)
- Sample target agents for testing

---

## Critical Dependencies & Timeline

### Day 2 Checkpoint: Schemas Complete
- **Track A** must finish `schemas.py`
- **Track B** can then start building agents in parallel
- **Sync:** 30-minute call to review schemas

### Day 5 Checkpoint: First Integration
- **Track A** has working adapter + operational probe
- **Track B** has reconnaissance agent ready
- **Test:** Run recon agent on sample target via adapter
- **Sync:** 1-hour pair programming session

### Day 7 Checkpoint: Full Pipeline
- **Track A** has meta-agent orchestrator
- **Track B** has all 5 agents complete
- **Test:** End-to-end audit on vulnerable_agent
- **Sync:** 1-hour integration testing session

### Day 9: Final Integration & Polish
- Merge both tracks
- Run full test suite
- Fix any integration bugs
- Polish CLI and documentation

---

## Communication Protocol

### Daily Standups (15 min)
- What did you ship yesterday?
- What are you shipping today?
- Any blockers?

### Shared Resources
- **Slack/Discord channel:** #lighthouse-dev
- **Shared doc:** Running list of integration questions
- **GitHub:** 
  - Track A works in `foundation` branch
  - Track B works in `agents` branch
  - Merge to `main` at checkpoints

### When to Sync Immediately
- Schema changes (affects both tracks)
- Adapter Protocol changes
- Budget calculation changes
- Breaking changes to any shared interface

---

## Conflict Avoidance Strategy

### Directory Ownership
- **Track A owns:**
  - `lighthouse/core/` (except `llm_client.py`)
  - `lighthouse/utils/`
  - `lighthouse/cli.py`
  - `tests/fixtures/`

- **Track B owns:**
  - `lighthouse/agents/` (except `operational.py`)
  - `lighthouse/prompts/`
  - `lighthouse/templates/`
  - `lighthouse/core/llm_client.py`

- **Shared (requires coordination):**
  - `lighthouse/core/schemas.py` (Track A creates, both use)
  - `README.md` (Track A writes setup, Track B writes usage)

### Merge Strategy
- Use feature branches for each component
- Squash merge to keep history clean
- Track A merges first at each checkpoint
- Track B rebases and resolves conflicts

---

## Success Criteria for Each Track

### Track A Success = Infrastructure Works
- ✅ Can load any target agent via adapter
- ✅ Can execute agents and capture traces
- ✅ Operational probe returns accurate metrics
- ✅ Meta-agent orchestrates full pipeline
- ✅ CLI provides good UX

### Track B Success = Intelligence Works
- ✅ Reconnaissance accurately maps target topology
- ✅ Red-team finds real vulnerabilities
- ✅ Compliance mapping is accurate (90%+ precision)
- ✅ Reports are executive-ready
- ✅ Total cost stays under $50/audit

### Combined Success = Lighthouse Ships
- ✅ End-to-end audit runs successfully
- ✅ All tests pass
- ✅ Documentation is complete
- ✅ Ready to demo/deploy

---

## Fallback Plan

If integration takes longer than expected:

**Option 1: Ship Track A First**
- Release as "Lighthouse Core" - just adapter + operational probe
- Shows infrastructure works
- Track B ships as v0.2

**Option 2: Ship Track B with Mock Adapter**
- Release as "Lighthouse Analysis" - demo mode only
- Uses pre-recorded adapter responses
- Track A ships as v0.2 for production use

**Option 3: Extend Timeline**
- Add 2-3 days for integration
- Worth it if both tracks are high quality
- Better to ship late than ship broken

---

## Questions for Initial Kickoff

1. **Who takes which track?**
   - Track A fits: Systems engineer, backend expert, loves infrastructure
   - Track B fits: ML engineer, prompt engineer, loves LLM work

2. **What's the source of truth for schemas?**
   - Suggestion: Track A owns `schemas.py`, Track B reviews/approves

3. **How do we handle API key management?**
   - Suggestion: Both use `.env` file, Track B documents key requirements

4. **What's the testing strategy?**
   - Suggestion: Each track writes unit tests, integration tests at checkpoints

5. **What's the definition of "done" for each component?**
   - Suggestion: Tests pass + peer review + docs updated

---

**Bottom Line:** This split lets two developers work in parallel with minimal blocking. The key is the Day 2 schema checkpoint and regular sync points to catch integration issues early.
