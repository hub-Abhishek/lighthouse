# `outputs/` — Generated Audit Artifacts

Runtime output directory. All files here are **generated** — never hand-edited.

## Structure

```
outputs/
└── audits/
    └── <target_id>/
        ├── report.json         ← Structured AuditReport (Pydantic serialized)
        ├── dashboard.html      ← Human-readable dashboard (rendered from template)
        └── audit_trace.jsonl   ← Full event log for reconstruction / debugging
```

## Notes

- Each audit run creates a subdirectory named by `target_id` and timestamp.
- `audit_trace.jsonl` is written incrementally during the run — safe to inspect mid-audit.
- `report.json` and `dashboard.html` are written only after the synthesizer completes.
- This directory is **gitignored** by default; only `.gitkeep` is committed.
