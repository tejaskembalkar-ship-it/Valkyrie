# Notices

## Upstream attribution

- Valkyrie is derived from Scrapling by D4Vinci.
  Source: https://github.com/D4Vinci/Scrapling

## Cross-repo dependency notice

- Valkyrie optionally depends on Daedalus Hermes integration through:
  - `agent-skill/hermes/adapter.py`
  - `scrapling/core/hermes_recovery.py`
- This dependency is feature-flagged via `HERMES_ENABLED`.
