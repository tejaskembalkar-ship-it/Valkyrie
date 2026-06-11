from __future__ import annotations

import os
from typing import Any, Callable, Dict, Optional


def _enabled() -> bool:
    return os.environ.get("HERMES_ENABLED", "false").strip().lower() in {"1", "true", "yes", "on"}


def recover_extraction_failure(
    *,
    operation_name: str,
    primary_error: Exception,
    retry_fn: Callable[[], Any],
    similarity_context: Optional[Dict[str, Any]] = None,
) -> Any:
    if not _enabled():
        raise primary_error

    from integrations.hermes_client import HermesClient  # type: ignore

    client = HermesClient()
    agent_id = "valkyrie"
    client.register_agent(agent_id, ["adaptive-extraction", "self-healing", "mcp-research"])

    memory = client.load_memory(agent_id)
    memory.setdefault("extraction_failures", [])
    memory["extraction_failures"].append(
        {
            "operation": operation_name,
            "error": str(primary_error),
            "similarity_context": similarity_context or {},
        }
    )
    client.save_memory(agent_id, memory)

    return client.self_heal(
        {
            "agent_id": agent_id,
            "operation": operation_name,
            "error": str(primary_error),
            "similarity_context": similarity_context or {},
        },
        retry_fn=retry_fn,
    )
