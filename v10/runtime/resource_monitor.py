from __future__ import annotations

import threading
import time
from typing import Callable, Optional

from v10.runtime.resource_manager import ResourceManager
from v10.runtime.resource_model import ResourceObservation
from v10.runtime.resource_policy import ResourceDecision, ResourcePolicy


class ResourceMonitor:
    """Periodic resource observation and policy evaluation for JARVIS V10.6."""

    def __init__(
        self,
        resource_manager: ResourceManager,
        resource_policy: ResourcePolicy,
        interval: float = 5.0,
        on_decision: Optional[Callable[[ResourceDecision], None]] = None,
    ) -> None:
        if not isinstance(resource_manager, ResourceManager):
            raise TypeError("resource_manager must be a ResourceManager")
        if not isinstance(resource_policy, ResourcePolicy):
            raise TypeError("resource_policy must be a ResourcePolicy")
        if interval <= 0:
            raise ValueError("interval must be greater than zero")

        self._resource_manager = resource_manager
        self._resource_policy = resource_policy
        self._interval = interval
        self._on_decision = on_decision

        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._last_decision: Optional[ResourceDecision] = None

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                snapshot = self._resource_manager.snapshot()
                observation = ResourceObservation.now(snapshot)
                decision = self._resource_policy.evaluate(observation)

                with self._lock:
                    self._last_decision = decision

                if self._on_decision is not None:
                    self._on_decision(decision)

            except Exception:
                # Monitoring must never terminate the host runtime.
                pass

            self._stop_event.wait(self._interval)

        with self._lock:
            self._running = False

    def start(self) -> None:
        with self._lock:
            if self._running:
                return

            self._stop_event.clear()
            self._running = True
            self._thread = threading.Thread(
                target=self._run,
                name="JARVIS-V10-ResourceMonitor",
                daemon=True,
            )
            self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        if timeout < 0:
            raise ValueError("timeout must be non-negative")

        with self._lock:
            thread = self._thread
            if thread is None:
                self._running = False
                return

            self._stop_event.set()

        if thread is not threading.current_thread():
            thread.join(timeout=timeout)

        with self._lock:
            if not thread.is_alive():
                self._running = False
                self._thread = None

    def is_running(self) -> bool:
        with self._lock:
            return self._running

    def get_last_decision(self) -> Optional[ResourceDecision]:
        with self._lock:
            return self._last_decision

    def get_interval(self) -> float:
        return self._interval
