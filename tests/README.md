# `tests/` — Test Suite

Contains all automated tests and fixtures for validating the Lighthouse system itself.

## Structure

```
tests/
├── README.md           ← You are here
└── fixtures/           ← Sample target agents used as test inputs
```

## `fixtures/`

Three sample AI agents are provided to validate end-to-end behavior:

| Agent | Description | Expected Outcome |
|-------|-------------|-----------------|
| `benign_agent/` | Simple RAG chatbot with no known vulnerabilities | Passes most checks |
| `vulnerable_agent/` | Intentionally has prompt injection weaknesses | High/critical findings detected |
| `complex_agent/` | Multi-agent system (tests recon capabilities) | Full topology map produced |

## Success Criteria

- Lighthouse detects ≥ 8 of 11 standard test categories
- Audit completes in < 30 minutes
- Budget stays under $50 per run
- JSONL trace allows full audit reconstruction
