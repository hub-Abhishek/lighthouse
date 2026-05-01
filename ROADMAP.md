# Lighthouse: Future Roadmap

This document captures ideas, features, and architectural improvements that are out of scope for the MVP but should be considered for future iterations.

## Advanced Sandboxing & Network Interception

To definitively prove whether a target agent is making unauthorized external LLM calls, leaking PII, or hallucinating data to third parties, Lighthouse should eventually move towards dynamic network interception.

Running the target software in an isolated environment (like a virtual environment or container) and capturing its outbound calls allows for highly reliable, deterministic auditing of its external dependencies.

### Proposed Implementation Approaches

#### 1. Python Monkey-Patching (Lightweight)
Because Lighthouse runs the agent via `LocalRepoAdapter` (importing and invoking Python code), we can monkey-patch common networking libraries (`requests`, `httpx`, `aiohttp`, `urllib3`) and SDKs (`openai`, `anthropic`) immediately before execution.
- **How:** Replace the `send` methods with a wrapper that logs the URL, headers, and payload to the `audit_trace.jsonl` before forwarding the request.
- **Pros:** No external tools required; pure Python solution.
- **Cons:** Can be bypassed if the agent uses obscure compiled extensions or spawns subprocesses (e.g., executing `curl` via `subprocess`).

#### 2. Transparent Proxy (Intermediate)
Run the target agent inside a virtual environment configured with `HTTP_PROXY` and `HTTPS_PROXY` variables pointing to a local Lighthouse-controlled proxy (e.g., using `mitmproxy`).
- **How:** Inject a custom CA certificate into the environment so the proxy can decrypt, inspect, and re-encrypt HTTPS traffic.
- **Pros:** Captures all HTTP(S) traffic regardless of the library used.
- **Cons:** Requires managing TLS certificates and running a background proxy server during the audit.

#### 3. Containerized Network Monitoring (Robust)
Execute the target agent inside an isolated Docker container with strict network monitoring attached.
- **How:** Use tools like `tcpdump` or eBPF probes on the container's virtual network interface to log all packets.
- **Pros:** Bulletproof. Captures everything, and allows Lighthouse to simulate network failures (e.g., testing agent behavior when the OpenAI API is down).
- **Cons:** Requires Docker privileges and a heavier setup.

### Integration into Lighthouse Pipeline

Once implemented, network interception would heavily enhance existing agents:
- **Reconnaissance:** Run a "dry run" through the proxy to automatically discover external dependencies and APIs without relying purely on static code analysis.
- **Red-Teaming:** Detect data exfiltration dynamically. (e.g., "We injected a fake SSN in the prompt, and the proxy caught the agent transmitting it to an unapproved API endpoint.")
- **Operational:** Accurately measure exact token consumption and latency for third-party API calls directly from the network layer.
