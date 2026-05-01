# `templates/` — Report Templates

Contains Jinja2 HTML templates used by `agents/synthesizer.py` to render the final human-readable audit dashboard.

## Files

### `report.html`
The primary audit dashboard template. Rendered by the `synthesizer` agent into a **self-contained static HTML file** (no backend required) that includes:

- Overall risk score and status badge (`passed` / `warning` / `failed`)
- Executive summary (LLM-generated)
- Finding cards grouped by severity (`critical`, `high`, `medium`, `low`, `info`)
- Compliance mapping table (EU AI Act, NIST AI RMF, OWASP LLM Top 10)
- Operational metrics charts (latency, token usage)
- Full JSONL trace download link

## Output Location

Rendered files are written to `outputs/audits/<target_id>/dashboard.html`.
