"""
JARVIS V10 Session Runtime

Owns the V10 Windows-session lifecycle around the voice layer.

This module intentionally does not modify V1-V9 runtime code.
"""

from __future__ import annotations

import threading
from enum import Enum
from typing import Optional

from v10.runtime.session_coordinator import (
    SessionCoordinator,
    SessionState,
)
from v10.runtime.session_monitor import SessionMonitor
from v10.runtime.session_voice_bridge import SessionVoiceBridge
from v10.runtime.voice_listener import V10Listener
from v10.runtime.voice_speaker import V10Speaker


class RuntimeState(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    ACTIVE = "active"
    LOCKED = "locked"
    STOPPING = "stopping"


class V10SessionRuntime:
    """
    Coordinates the V10 voice layer with Windows session state.
    """

    def __init__(
        self,
        listener: Optional[V10Listener] = None,
        speaker: Optional[V10Speaker] = None,
    ):
        self.coordinator = SessionCoordinator()

        self.listener = listener or V10Listener(
            self.coordinator.get_interrupt_event()
        )

        self.speaker = speaker or V10Speaker()

        self.bridge = SessionVoiceBridge(
            self.coordinator,
            self.listener,
            self.speaker,
        )

        self.monitor = SessionMonitor(
            on_event=self._handle_session_event
        )

        self._lock = threading.Lock()
        self._state = RuntimeState.STOPPED

    def start(self) -> None:
        """Start the V10 session-aware runtime."""

        with self._lock:
            if self._state != RuntimeState.STOPPED:
                return

            self._state = RuntimeState.STARTING

        try:
            self.coordinator.set_active()

            self.bridge.start()
            self.monitor.start()

            with self._lock:
                self._state = RuntimeState.ACTIVE

        except Exception:
            try:
                self.monitor.stop()
            except Exception:
                pass

            try:
                self.bridge.stop()
            except Exception:
                pass

            with self._lock:
                self._state = RuntimeState.STOPPED

            raise

    def _handle_session_event(self, event: str) -> None:
        """
        Lightweight session callback.

        SessionVoiceBridge performs potentially blocking voice
        operations outside the Windows message thread.
        """

        self.bridge.handle_event(event)

        if event == "lock":
            with self._lock:
                self._state = RuntimeState.LOCKED

        elif event == "unlock":
            with self._lock:
                self._state = RuntimeState.ACTIVE

    def stop(self) -> None:
        """Stop the V10 session-aware runtime."""

        with self._lock:
            if self._state == RuntimeState.STOPPED:
                return

            self._state = RuntimeState.STOPPING

        try:
            self.monitor.stop()
        finally:
            try:
                self.bridge.stop()
            finally:
                with self._lock:
                    self._state = RuntimeState.STOPPED

    def get_state(self) -> RuntimeState:
        """Return the V10 runtime state."""

        with self._lock:
            return self._state

    def get_session_state(self) -> SessionState:
        """Return the coordinated Windows session state."""

        return self.coordinator.get_state()

    def is_running(self) -> bool:
        """Return whether the V10 runtime is active or locked."""

        with self._lock:
            return self._state in (
                RuntimeState.ACTIVE,
                RuntimeState.LOCKED,
            )
