"""
JARVIS V10 Unified Runtime Integration Boundary

Provides a narrow integration layer between the existing unified
JARVIS runtime and the V10 session-aware voice components.

This module intentionally does not modify:
- jarvis_unified.py
- jarvis_unified_runtime.py
- V1-V9 voice implementations

The boundary preserves the synchronous behavior expected by the
existing unified runtime while using the V10 session-aware listener
and speaker underneath.
"""

from __future__ import annotations

import time
from typing import Optional

from v10.runtime.session_runtime import V10SessionRuntime
from v10.runtime.session_coordinator import SessionState
from v10.runtime.voice_listener import ListenerInterrupted
from v10.runtime.resource_manager import ResourceManager
from v10.runtime.resource_monitor import ResourceMonitor
from v10.runtime.resource_policy import ResourcePolicy


class V10UnifiedIntegration:
    """
    Integration boundary for the existing unified JARVIS runtime.

    The existing runtime can continue calling:

        integration.listen()
        integration.speak(text)

    without knowing about Windows session monitoring.
    """

    def __init__(
        self,
        session_runtime: Optional[V10SessionRuntime] = None,
    ):
        self.session_runtime = (
            session_runtime
            or V10SessionRuntime()
        )

        self.listener = self.session_runtime.listener
        self.speaker = self.session_runtime.speaker
        self.coordinator = self.session_runtime.coordinator

        self.resource_manager = ResourceManager()
        self.resource_policy = ResourcePolicy()
        self.resource_monitor = ResourceMonitor(
            self.resource_manager,
            self.resource_policy,
        )

        self._started = False

    def start(self) -> None:
        """Start the V10 session-aware runtime."""

        if self._started:
            return

        self.session_runtime.start()

        try:
            self.resource_monitor.start()
        except Exception:
            self.session_runtime.stop()
            raise

        self._started = True

    def wait_until_active(self) -> None:
        """
        Wait until the Windows session is active.

        This is intentionally small so the unified runtime does not
        need to understand Windows session APIs.
        """

        while self.coordinator.is_interrupted():
            time.sleep(0.05)

    def listen(self) -> str:
        """
        Listen using the V10 session-aware listener.

        ListenerInterrupted is allowed to propagate so the outer
        integration boundary can distinguish a Windows lock from
        an ordinary speech-recognition failure.
        """

        self.wait_until_active()

        try:
            return self.listener.listen()

        except ListenerInterrupted:
            raise

    def speak(self, text) -> None:
        """
        Preserve synchronous speaker semantics while making the
        production voice path explicitly session-aware.

        A Windows lock is treated as an immediate cancellation:
        the current TTS operation is stopped and this call returns
        without allowing the old runtime to continue waiting on it.
        """

        if not text:
            return

        self.wait_until_active()

        # Re-check immediately before starting TTS.
        if self.coordinator.is_interrupted():
            return

        self.speaker.speak(text)

        while self.speaker.is_speaking():
            if self.coordinator.is_interrupted():
                self.speaker.stop()
                return

            time.sleep(0.02)

        # Prevent a new voice operation from starting after a lock
        # that arrives at the end of playback.
        if self.coordinator.is_interrupted():
            self.speaker.stop()

    def is_locked(self) -> bool:
        """Return whether the Windows session is currently locked."""

        return (
            self.coordinator.get_state()
            == SessionState.LOCKED
        )

    def is_active(self) -> bool:
        """Return whether the Windows session is currently active."""

        return (
            self.coordinator.get_state()
            == SessionState.ACTIVE
        )

    def stop(self) -> None:
        """Stop the V10 session-aware runtime."""

        if not self._started:
            return

        try:
            self.resource_monitor.stop()
        finally:
            self.session_runtime.stop()

        self._started = False

    def is_running(self) -> bool:
        """Return whether the integration boundary is running."""

        return (
            self._started
            and self.session_runtime.is_running()
        )

    def get_resource_decision(self):
        """Return the latest V10.6 resource decision."""

        return self.resource_monitor.get_last_decision()

    def is_resource_monitor_running(self) -> bool:
        """Return whether the V10.6 resource monitor is running."""

        return self.resource_monitor.is_running()
