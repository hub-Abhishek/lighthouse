# `utils/` — Cross-Cutting Utilities

Shared infrastructure modules used by all agents and the orchestrator. None of these modules contain business logic — they are pure infrastructure.

## Files

### `tracing.py`
**Stateful JSONL event logger.** Appends every significant event to `audit_trace.jsonl` immediately, enabling full reconstruction of an audit even after a crash.

Logged events include:
- Agent start / completion
- Every LLM API call (prompt + response)
- Each `Finding` as it is discovered

### `validators.py`
**Quality gates.** Validates agent outputs against expected schemas and business rules before they are passed to the next stage. Prevents malformed or empty results from propagating silently through the pipeline.

## Usage Pattern

```python
from lighthouse.utils.tracing import log_event
from lighthouse.utils.validators import validate_findings
```
