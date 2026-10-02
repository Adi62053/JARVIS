from __future__ import annotations

import threading
from typing import Optional

import speech_recognition as sr


class ListenerInterrupted(Exception):
    """Raised when the V10 listener is interrupted by session state."""


class V10Listener:
    def __init__(self, interrupt_event: threading.Event):
        self._interrupt_event = interrupt_event
        self._recognizer = sr.Recognizer()

        # A fresh Microphone instance is created for every listening
        # session. This prevents a previous background listener's
        # context manager from colliding with a new one after
        # Windows LOCK -> UNLOCK.
        self._microphone: Optional[sr.Microphone] = None

        self._lock = threading.Lock()
        self._stopper = None
        self._running = False

        self._result_event = threading.Event()
        self._result_lock = threading.Lock()

        self._result: Optional[str] = None
        self._exception: Optional[BaseException] = None

    def start(self) -> None:
        with self._lock:
            if self._running:
                return

            # Reset result state before starting a new microphone
            # session.
            self._result_event.clear()

            with self._result_lock:
                self._result = None
                self._exception = None

            # IMPORTANT:
            # Create a completely new Microphone object for every
            # background listener session.
            microphone = sr.Microphone()

            # Keep this microphone instance alive for the entire
            # background-listener lifetime.
            self._microphone = microphone

            # Preserve the existing calibration behavior.
            with microphone as source:
                self._recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5,
                )

            stopper = self._recognizer.listen_in_background(
                microphone,
                self._callback,
                phrase_time_limit=None,
            )

            self._stopper = stopper
            self._running = True

    def _callback(self, recognizer, audio) -> None:
        try:
            # If Windows has locked the session, discard the captured
            # audio instead of sending it for recognition.
            if self._interrupt_event.is_set():
                return

            command = recognizer.recognize_google(audio)

            # The session could have become locked while Google STT
            # was processing the audio.
            if self._interrupt_event.is_set():
                return

            with self._result_lock:
                self._result = command

            self._result_event.set()

        except BaseException as exc:
            with self._result_lock:
                self._exception = exc

            self._result_event.set()

    def listen(self) -> str:
        self.start()

        while True:
            # Fast interruption response.
            if self._interrupt_event.is_set():
                raise ListenerInterrupted()

            if self._result_event.wait(0.1):
                with self._result_lock:
                    result = self._result
                    exception = self._exception

                    self._result = None
                    self._exception = None

                self._result_event.clear()

                # Never return a command after the session became
                # locked.
                if self._interrupt_event.is_set():
                    raise ListenerInterrupted()

                if exception is not None:
                    raise exception

                if result is None:
                    continue

                print("You:", result)

                return result

    def stop(self) -> None:
        with self._lock:
            stopper = self._stopper

            self._stopper = None
            self._running = False

            # Release our reference to the microphone only after the
            # background listener has been stopped below.
            microphone = self._microphone

        if stopper is not None:
            # SpeechRecognition's stopper waits for the background
            # listener thread to terminate.
            stopper(wait_for_stop=True)

        with self._lock:
            # Clear the microphone reference only after the listener
            # thread has finished using it.
            if self._microphone is microphone:
                self._microphone = None

            # Wake any waiting listen() call.
            self._result_event.set()

    def is_running(self) -> bool:
        with self._lock:
            return self._running