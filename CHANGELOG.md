# Changelog

## Unreleased

- Added optional Hermes recovery layer via `agent-skill/hermes/adapter.py` and `scrapling/core/hermes_recovery.py`.
- Preserved existing similarity-scoring adaptive recovery as first-line self-heal.
- Added Phase 1 social signal stub modules for Instagram, Facebook, and YouTube under `agent-skill/Scrapling-Skill/scrapers/`.
- Added MCP stub endpoint `discover_social_signals` in `scrapling/core/ai.py` for integration-path wiring.
