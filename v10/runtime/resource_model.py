from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from v10.runtime.resource_manager import ResourceSnapshot


@dataclass(frozen=True)
class ResourceObservation:
    """Immutable timestamped observation of runtime resource facts."""

    timestamp: datetime
    snapshot: ResourceSnapshot

    def __post_init__(self) -> None:
        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be a datetime")
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must be timezone-aware")
        if not isinstance(self.snapshot, ResourceSnapshot):
            raise TypeError("snapshot must be a ResourceSnapshot")

    @classmethod
    def now(cls, snapshot: ResourceSnapshot) -> "ResourceObservation":
        return cls(timestamp=datetime.now(timezone.utc), snapshot=snapshot)
