
"""
JARVIS V10 Session Voice Bridge

Connects Windows session state to the V10 voice components.

This module intentionally does not modify:
- V1-V9 runtime code
- jarvis_unified.py
- jarvis_unified_runtime.py
- historical voice implementations

The SessionMonitor callback remains lightweight. Voice shutdown
operations are handled by a dedicated worker thread.
"""

from __future__ import annotations

import queue
import threading
from typing import Optional

from v10.runtime.session_coordinator import (
    SessionCoordinator,
    SessionState,
)
from v10.runtime.voice_listener import V10Listener
from v10.runtime.voice_speaker import V10Speaker


class VoiceAction:
    LOCK = "lock"
    UNLOCK = "unlock"
    STOP = "stop"


class SessionVoiceBridge:
    """
    Coordinates session state with V10 listener and speaker.

    Windows session events are received through handle_event().
    Potentially blocking voice operations are performed by a
    dedicated worker thread.
    """

    def __init__(
        self,
        coordinator: SessionCoordinator,
        listener: V10Listener,
        speaker: V10Speaker,
    ):
        self.coordinator = coordinator
        self.listener = listener
        self.speaker = speaker

        self._queue: queue.Queue[str] = queue.Queue()
        self._stop_event = threading.Event()
        self._worker: Optional[threading.Thread] = None

        self._lock = threading.Lock()
        self._started = False

    def start(self) -> None:
        """Start the voice-control worker."""

        with self._lock:
            if self._started:
                return

            self._stop_event.clear()

            self._worker = threading.Thread(
                target=self._run,
                daemon=True,
                name="JARVIS-V10-SessionVoiceBridge",
            )

            self._worker.start()
            self._started = True

    def handle_event(self, event: str) -> None:
        """
        Handle a Windows session event.

        This method remains lightweight because it may be called
        from the SessionMonitor's Windows message thread.
        """

        if event == "lock":
            print("V10 BRIDGE: LOCK EVENT RECEIVED")

            self.coordinator.set_locked()

            self._queue.put(VoiceAction.LOCK)

            print("V10 BRIDGE: LOCK ACTION QUEUED")

        elif event == "unlock":
            print("V10 BRIDGE: UNLOCK EVENT RECEIVED")

            self.coordinator.set_active()

            self._queue.put(VoiceAction.UNLOCK)

            print("V10 BRIDGE: UNLOCK ACTION QUEUED")

    def _run(self) -> None:
        """Process voice actions outside the Windows message thread."""

        while not self._stop_event.is_set():

            try:
                action = self._queue.get(timeout=0.1)

            except queue.Empty:
                continue

            try:
                if action == VoiceAction.LOCK:
                    print("V10 BRIDGE WORKER: LOCK ACTION START")

                    print(
                        "V10 BRIDGE WORKER: SPEAKER BEFORE STOP:",
                        self.speaker.is_speaking(),
                    )

                    # Critical ordering:
                    # stop speech FIRST so audio cannot continue while
                    # the listener shutdown is being processed.
                    self.speaker.stop()

                    print(
                        "V10 BRIDGE WORKER: SPEAKER AFTER STOP:",
                        self.speaker.is_speaking(),
                    )

                    # Stop microphone/listening after speech is stopped.
                    self.listener.stop()

                    print("V10 BRIDGE WORKER: LOCK ACTION COMPLETE")

                elif action == VoiceAction.UNLOCK:
                    # Session state is already ACTIVE.
                    # Voice components remain stopped until the
                    # V10 runtime explicitly starts them again.
                    pass

                elif action == VoiceAction.STOP:
                    # Use the same safe shutdown ordering.
                    self.speaker.stop()
                    self.listener.stop()

            except Exception as exc:
                print(
                    "V10 session voice bridge error:",
                    exc,
                )

            finally:
                self._queue.task_done()

    def stop(self, timeout: float = 5.0) -> None:
        """Stop the bridge worker and voice components."""

        with self._lock:
            if not self._started:
                return

            self._stop_event.set()

            worker = self._worker

            self._worker = None
            self._started = False

        self._queue.put(VoiceAction.STOP)

        if worker is not None:
            worker.join(timeout=timeout)

    def is_running(self) -> bool:
        """Return whether the bridge worker is running."""

        with self._lock:
            worker = self._worker

            return (
                self._started
                and worker is not None
                and worker.is_alive()
            )

    def get_state(self) -> SessionState:
        """Return the current coordinated Windows session state."""

        return self.coordinator.get_state()
