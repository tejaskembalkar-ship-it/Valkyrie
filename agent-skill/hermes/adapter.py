from __future__ import annotations

import os
from typing import Any, Callable, Dict


def _enabled(flag: str = "HERMES_ENABLED") -> bool:
    return os.environ.get(flag, "false").strip().lower() in {"1", "true", "yes", "on"}


def run_with_layered_recovery(
    *,
    operation_name: str,
    primary_run: Callable[[], Any],
    similarity_recovery: Callable[[Exception], Any],
) -> Any:
    """
    Valkyrie recovery layering:
    1) normal execution
    2) existing Scrapling similarity-based relocation recovery
    3) Hermes recovery (optional, feature-flagged)
    """
    try:
        return primary_run()
    except Exception as primary_error:
        try:
            return similarity_recovery(primary_error)
        except Exception as similarity_error:
            if not _enabled():
                raise

            from integrations.hermes_client import HermesClient  # type: ignore

            client = HermesClient()
            agent_id = "valkyrie"
            client.register_agent(
                agent_id,
                capabilities=["signal-research", "adaptive-extraction", "mcp-serving"],
            )
            memory = client.load_memory(agent_id)
            memory.setdefault("recovery_events", [])
            memory["recovery_events"].append(
                {
                    "operation": operation_name,
                    "primary_error": str(primary_error),
                    "similarity_error": str(similarity_error),
                }
            )
            client.save_memory(agent_id, memory)

            return client.self_heal(
                {
                    "agent_id": agent_id,
                    "operation": operation_name,
                    "primary_error": str(primary_error),
                    "similarity_error": str(similarity_error),
                },
                retry_fn=primary_run,
            )
