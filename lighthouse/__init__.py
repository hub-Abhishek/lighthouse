"""
lighthouse
==========
Lighthouse: AI Agent Auditing System.

This package exposes the public API for running audits programmatically.
For CLI usage, see the `lighthouse` console script defined in pyproject.toml.

Typical usage:
    from lighthouse.core.schemas import AuditConfig
    from lighthouse.core.meta_agent import run_audit

    config = AuditConfig(target_path="./my-agent", budget_usd=50.0)
    report = await run_audit(config)
"""
