"""
adapters.py
===========
Target system adapters that implement the `TargetAdapter` Protocol.

The adapter layer decouples all audit agents from the specifics of *how* a
target system is accessed. Any module that needs to interact with the target
receives a `TargetAdapter` instance — it never talks to the target directly.

Protocol
--------
TargetAdapter
    Defines the three operations every concrete adapter must support:
    - list_agents()  → discover agent nodes / endpoints
    - invoke()       → send a single probe payload and get a response
    - trace()        → retrieve execution logs for a given run

Concrete Implementations
------------------------
LocalRepoAdapter
    Mode A — Scans a local Python project directory. Parses source files to
    discover agent definitions, tool registrations, and system prompts.
    No network calls required.

APIAdapter
    Mode B — Probes a live REST or GraphQL endpoint. Sends HTTP requests
    constructed from the `TestPlan` and captures raw responses.

LangGraphAdapter
    Mode C — Hooks into a running LangGraph application via its tracing
    callbacks. Observes real execution without modifying the target.
"""
