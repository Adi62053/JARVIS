from __future__ import annotations

from enum import Enum
from threading import Event, Lock


class SessionState(Enum):
    UNKNOWN = "unknown"
    ACTIVE = "active"
    LOCKED = "locked"


class SessionCoordinator:
    def __init__(self):
        self._lock = Lock()
        self._state = SessionState.UNKNOWN
        self._interrupt_event = Event()
        self._response_generation = 0

    def set_active(self) -> None:
        with self._lock:
            self._state = SessionState.ACTIVE
            self._interrupt_event.clear()

    def set_locked(self) -> None:
        with self._lock:
            self._state = SessionState.LOCKED
            self._response_generation += 1
            self._interrupt_event.set()

    def handle_event(self, event: str) -> None:
        if event == "lock":
            self.set_locked()
        elif event == "unlock":
            self.set_active()

    def get_state(self) -> SessionState:
        with self._lock:
            return self._state

    def is_active(self) -> bool:
        return self.get_state() == SessionState.ACTIVE

    def is_locked(self) -> bool:
        return self.get_state() == SessionState.LOCKED

    def is_interrupted(self) -> bool:
        return self._interrupt_event.is_set()

    def get_interrupt_event(self) -> Event:
        return self._interrupt_event

    def get_response_generation(self) -> int:
        with self._lock:
            return self._response_generation
