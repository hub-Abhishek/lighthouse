"""
tracing.py
==========
Stateful JSONL event logger for audit runs.

All significant events during an audit are appended to `audit_trace.jsonl`
immediately as they occur — not batched at the end. This means the trace
file is safe to inspect mid-audit, and a crashed run leaves a recoverable
log behind.

What Gets Logged
----------------
- Agent lifecycle: start, completion, duration
- Every LLM API call: model used, full prompt, full response, token counts
- Every `Finding` at the moment it is discovered
- Budget checkpoints: cost so far vs. remaining budget

Log Format (one JSON object per line)
--------------------------------------
{
    "timestamp": "2026-05-01T14:00:00.000Z",
    "type": "agent_start" | "llm_call" | "finding" | "budget_checkpoint" | ...,
    "agent": "reconnaissance" | "red_team" | ...,
    "data": { ... event-specific payload ... }
}

Key Functions
-------------
log_event(event_type, agent, data)
    Appends a single event to the trace file. Thread-safe via file append.

get_trace(run_id) -> list[dict]
    Reads and parses all events for a given audit run.
"""
