# `core/` — System Core

Contains the three foundational modules that define **what** the system audits, **how** it connects to targets, and **who** coordinates the work.

## Files

### `schemas.py`
Pydantic v2 data contracts shared across the entire system.  
Key models: `AuditConfig`, `Finding`, `AuditReport`, `TopologyMap`, `TestPlan`.

### `adapters.py`
The `TargetAdapter` Protocol and its concrete implementations.  
Decouples all agent logic from the specifics of the target system:
- `LocalRepoAdapter` — scans a local Python codebase
- `APIAdapter` — probes REST/GraphQL endpoints
- `LangGraphAdapter` — hooks into LangGraph execution traces

### `meta_agent.py`
The central orchestrator. Loads an `AuditConfig`, picks the right adapter, calls all specialist agents in sequence, enforces budget gates, and produces the final `AuditReport`.

## Data Flow

```
AuditConfig
    └─► meta_agent.py
            ├─► TargetAdapter (adapters.py)
            └─► agents/* (using schemas from schemas.py)
                    └─► AuditReport
```
