# `utils/` — Cross-Cutting Utilities

Shared infrastructure modules used by all agents and the orchestrator. None of these modules contain business logic — they are pure infrastructure.

## Files

### `tracing.py`
**Stateful JSONL event logger.** Appends every significant event to `audit_trace.jsonl` immediately, enabling full reconstruction of an audit even after a crash.

Logged events include:
- Agent start / completion
- Every LLM API call (prompt + response)
- Each `Finding` as it is discovered
- Budget checkpoints

### `budget.py`
**Real-time cost tracker.** Maintains a running tally of API spend across all agents. Exposes a `gate_check()` method that the meta-agent calls before each expensive operation to enforce the `$50` hard limit.

### `validators.py`
**Quality gates.** Validates agent outputs against expected schemas and business rules before they are passed to the next stage. Prevents malformed or empty results from propagating silently through the pipeline.

## Usage Pattern

```python
from lighthouse.utils.tracing import log_event
from lighthouse.utils.budget import BudgetTracker
from lighthouse.utils.validators import validate_findings
```
