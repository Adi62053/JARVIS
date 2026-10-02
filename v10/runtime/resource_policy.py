from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from v10.runtime.resource_model import ResourceObservation


class ResourceState(Enum):
    """Policy classification of a resource observation."""

    NORMAL = "normal"
    PRESSURE = "pressure"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ResourcePolicyConfig:
    """Configurable single-observation resource policy boundaries."""

    pressure_memory_percent: float = 85.0
    critical_memory_percent: float = 92.0

    pressure_available_memory_bytes: int = 1_500_000_000
    critical_available_memory_bytes: int = 750_000_000

    pressure_process_cpu_percent: float = 200.0
    critical_process_cpu_percent: float = 400.0

    def __post_init__(self) -> None:
        if not 0 <= self.pressure_memory_percent <= 100:
            raise ValueError("pressure_memory_percent must be between 0 and 100")

        if not 0 <= self.critical_memory_percent <= 100:
            raise ValueError("critical_memory_percent must be between 0 and 100")

        if self.pressure_memory_percent >= self.critical_memory_percent:
            raise ValueError(
                "pressure_memory_percent must be below critical_memory_percent"
            )

        if self.pressure_available_memory_bytes <= 0:
            raise ValueError(
                "pressure_available_memory_bytes must be greater than zero"
            )

        if self.critical_available_memory_bytes <= 0:
            raise ValueError(
                "critical_available_memory_bytes must be greater than zero"
            )

        if (
            self.critical_available_memory_bytes
            >= self.pressure_available_memory_bytes
        ):
            raise ValueError(
                "critical_available_memory_bytes must be below "
                "pressure_available_memory_bytes"
            )

        if self.pressure_process_cpu_percent < 0:
            raise ValueError(
                "pressure_process_cpu_percent must be non-negative"
            )

        if self.critical_process_cpu_percent < 0:
            raise ValueError(
                "critical_process_cpu_percent must be non-negative"
            )

        if (
            self.pressure_process_cpu_percent
            >= self.critical_process_cpu_percent
        ):
            raise ValueError(
                "pressure_process_cpu_percent must be below "
                "critical_process_cpu_percent"
            )


@dataclass(frozen=True)
class ResourceDecision:
    """Immutable result of evaluating one resource observation."""

    state: ResourceState
    reasons: tuple[str, ...]
    observation: ResourceObservation

    def __post_init__(self) -> None:
        if not isinstance(self.state, ResourceState):
            raise TypeError("state must be a ResourceState")

        if not isinstance(self.reasons, tuple):
            raise TypeError("reasons must be a tuple")

        if not all(isinstance(reason, str) for reason in self.reasons):
            raise TypeError("reasons must contain only strings")

        if not isinstance(self.observation, ResourceObservation):
            raise TypeError(
                "observation must be a ResourceObservation"
            )


class ResourcePolicy:
    """Pure single-observation resource policy evaluator."""

    def __init__(
        self,
        config: ResourcePolicyConfig | None = None,
    ) -> None:
        self._config = config or ResourcePolicyConfig()

    @property
    def config(self) -> ResourcePolicyConfig:
        return self._config

    def evaluate(
        self,
        observation: ResourceObservation,
    ) -> ResourceDecision:
        if not isinstance(observation, ResourceObservation):
            raise TypeError(
                "observation must be a ResourceObservation"
            )

        snapshot = observation.snapshot
        reasons: list[str] = []
        critical = False
        pressure = False

        if (
            snapshot.memory_percent
            >= self._config.critical_memory_percent
        ):
            critical = True
            reasons.append("system_memory_critical")
        elif (
            snapshot.memory_percent
            >= self._config.pressure_memory_percent
        ):
            pressure = True
            reasons.append("system_memory_pressure")

        if (
            snapshot.memory_available_bytes
            <= self._config.critical_available_memory_bytes
        ):
            critical = True
            reasons.append("available_memory_critical")
        elif (
            snapshot.memory_available_bytes
            <= self._config.pressure_available_memory_bytes
        ):
            pressure = True
            reasons.append("available_memory_pressure")

        if (
            snapshot.process_cpu_percent
            >= self._config.critical_process_cpu_percent
        ):
            critical = True
            reasons.append("process_cpu_critical")
        elif (
            snapshot.process_cpu_percent
            >= self._config.pressure_process_cpu_percent
        ):
            pressure = True
            reasons.append("process_cpu_pressure")

        if critical:
            state = ResourceState.CRITICAL
        elif pressure:
            state = ResourceState.PRESSURE
        else:
            state = ResourceState.NORMAL

        if not reasons:
            reasons.append("resources_within_policy_limits")

        return ResourceDecision(
            state=state,
            reasons=tuple(reasons),
            observation=observation,
        )
