"""
JARVIS V9 - Audit Logger

Provides persistent security audit logging for V9.

This module:
- records structured security events
- creates the V9 audit log directory when needed
- writes one event per line
- avoids logging secret values by design

This module does not:
- execute operations
- request elevation
- authorize operations
- modify Windows permissions
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json


class V9AuditLogger:
    """Write structured V9 security audit events."""

    def __init__(self, log_path: str | Path | None = None) -> None:
        if log_path is None:
            log_path = Path("logs") / "v9_security_audit.jsonl"

        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        *,
        operation_id: str,
        capability: str,
        resource: str,
        risk_level: str,
        required_privilege: str,
        current_privilege: str,
        authorization_state: str,
        decision: str,
        result: str,
    ) -> dict[str, str]:
        """Record one security event and return the event dictionary."""

        values = {
            "operation_id": operation_id,
            "capability": capability,
            "resource": resource,
            "risk_level": risk_level,
            "required_privilege": required_privilege,
            "current_privilege": current_privilege,
            "authorization_state": authorization_state,
            "decision": decision,
            "result": result,
        }

        for name, value in values.items():
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")

            if not value.strip():
                raise ValueError(f"{name} cannot be empty")

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **values,
        }

        with self.log_path.open(
            "a",
            encoding="utf-8",
        ) as handle:
            handle.write(
                json.dumps(
                    event,
                    ensure_ascii=False,
                )
                + "\n"
            )

        return event
