"""
JARVIS V10 Speaker Adapter

Provides asynchronous, session-aware, interruptible Kokoro TTS
playback for V10.

Important:
- Historical V1-V9 voice/speaker.py is NOT modified.
- V10 speaker.speak() returns immediately.
- Kokoro generation and WAV preparation run on a dedicated worker thread.
- Audio playback uses sounddevice callback streaming.
- stop() cancels generation and aborts active audio playback.
- Temporary WAV files are removed only after playback has ended.
"""

from __future__ import annotations

import os
import tempfile
import threading

import sounddevice as sd
import soundfile as sf
from kokoro_onnx import Kokoro


class V10Speaker:
    """Asynchronous, session-aware, interruptible Kokoro speaker."""

    def __init__(self):
        # ==========================================
        # JARVIS ROOT DIRECTORY
        # ==========================================

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        # ==========================================
        # KOKORO CONFIGURATION
        # ==========================================

        self.model_path = os.path.join(
            base_dir,
            "kokoro-v1.0.onnx",
        )

        self.voices_path = os.path.join(
            base_dir,
            "voices-v1.0.bin",
        )

        self.voice = "am_adam"
        self.language = "en-us"
        self.speed = 1.0

        # ==========================================
        # OUTPUT DIRECTORY
        # ==========================================

        self.data_dir = os.path.join(
            base_dir,
            "data",
        )

        os.makedirs(
            self.data_dir,
            exist_ok=True,
        )

        # Kept for compatibility/reference.
        self.output_file = os.path.join(
            self.data_dir,
            "jarvis_voice_v10.wav",
        )

        # ==========================================
        # STATE
        # ==========================================

        self._lock = threading.Lock()

        self._speaking = False
        self._speech_thread = None
        self._speech_stop_event = None

        # Active sounddevice stream.
        self._audio_stream = None

        # ==========================================
        # VERIFY MODEL FILES
        # ==========================================

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                "Kokoro model not found:\n"
                f"{self.model_path}"
            )

        if not os.path.exists(self.voices_path):
            raise FileNotFoundError(
                "Kokoro voice file not found:\n"
                f"{self.voices_path}"
            )

        # ==========================================
        # INITIALIZE KOKORO
        # ==========================================

        print("Initializing V10 JARVIS voice...")

        self.kokoro = Kokoro(
            self.model_path,
            self.voices_path,
        )

        print(
            "V10 JARVIS voice initialized: "
            "Kokoro / am_adam"
        )

    # ==========================================================
    # PREFETCH TTS AUDIO
    # ==========================================================

    def prepare(self, text, stop_event=None):
        """
        Generate Kokoro audio without starting playback.

        This is used by the streaming TTS prefetch pipeline so
        the next sentence can be synthesized while the current
        sentence is playing.
        """

        if not text:
            return None

        text = str(text).strip()

        if not text:
            return None

        samples, sample_rate = self.kokoro.create(
            text,
            voice=self.voice,
            speed=self.speed,
            lang=self.language,
        )

        if stop_event is not None and stop_event.is_set():
            return None

        audio = samples

        if audio.ndim == 1:
            audio = audio.reshape(-1, 1)

        return audio, sample_rate

    # ==========================================================
    # PLAY PREPARED AUDIO
    # ==========================================================

    def play_prepared(
        self,
        audio,
        sample_rate,
        stop_event=None,
    ):
        """
        Play already-generated Kokoro audio.

        Playback is interruptible through stop().
        """

        if audio is None:
            return

        if stop_event is None:
            stop_event = threading.Event()

        stream = None
        position = 0
        position_lock = threading.Lock()

        with self._lock:
            self._speech_stop_event = stop_event
            self._speaking = True

        def callback(
            outdata,
            frames,
            time_info,
            status,
        ):
            nonlocal position

            # Normal sounddevice callback status is intentionally
            # hidden from the user-facing JARVIS terminal UI.

            if stop_event.is_set():
                outdata.fill(0)
                raise sd.CallbackStop

            with position_lock:
                remaining = len(audio) - position

                if remaining <= 0:
                    outdata.fill(0)
                    raise sd.CallbackStop

                count = min(
                    frames,
                    remaining,
                )

                outdata[:count] = audio[
                    position:position + count
                ]

                if count < frames:
                    outdata[count:] = 0
                    position += count
                    raise sd.CallbackStop

                position += count

        try:
            # Voice engine details are intentionally hidden from
            # the user-facing JARVIS terminal UI.
            stream = sd.OutputStream(
                samplerate=sample_rate,
                channels=audio.shape[1],
                dtype="float32",
                callback=callback,
            )

            with self._lock:
                self._audio_stream = stream

            if stop_event.is_set():
                return

            # Playback start is intentionally hidden from the
            # user-facing JARVIS terminal UI.
            stream.start()

            while stream.active:
                if stop_event.wait(0.05):
                    try:
                        stream.abort()
                    except Exception:
                        pass
                    break

                if (
                    len(audio) - position
                    <= 0
                ):
                    break

            try:
                if stream.active:
                    stream.stop()
            except Exception:
                pass

        except Exception as exc:
            print(
                "V10 Kokoro prepared playback error:",
                exc,
            )

        finally:
            if stream is not None:
                try:
                    stream.close()
                except Exception:
                    pass

            with self._lock:
                if self._audio_stream is stream:
                    self._audio_stream = None

                if self._speech_stop_event is stop_event:
                    self._speaking = False
                    self._speech_thread = None
                    self._speech_stop_event = None

    # ==========================================================
    # START SPEECH
    # ==========================================================

    def speak(self, text):
        """
        Start a new speech request asynchronously.

        The caller returns immediately.

        Kokoro generation and audio playback happen inside
        the dedicated V10 TTS worker thread.
        """

        if not text:
            return

        text = str(text).strip()

        if not text:
            return

        # ------------------------------------------------------
        # Stop any previous speech request.
        # ------------------------------------------------------

        self.stop()

        # ------------------------------------------------------
        # Create cancellation event for this request.
        # ------------------------------------------------------

        stop_event = threading.Event()

        with self._lock:
            self._speech_stop_event = stop_event
            self._speaking = True

        print("JARVIS:", text)

        # ------------------------------------------------------
        # Start dedicated speech worker.
        # ------------------------------------------------------

        thread = threading.Thread(
            target=self._speak_worker,
            args=(text, stop_event),
            daemon=True,
            name="JARVIS-V10-TTS",
        )

        with self._lock:
            self._speech_thread = thread

        thread.start()

    # ==========================================================
    # SPEECH WORKER
    # ==========================================================

    def _speak_worker(self, text, stop_event):
        """
        Generate and play one isolated speech request.

        Audio playback uses sounddevice callback streaming so
        active playback can be interrupted with stream.abort().
        """

        output_file = None
        stream = None

        try:
            # ==============================================
            # KOKORO GENERATION
            # ==============================================

            samples, sample_rate = self.kokoro.create(
                text,
                voice=self.voice,
                speed=self.speed,
                lang=self.language,
            )

            # ==============================================
            # CANCELLATION CHECK
            # ==============================================

            if stop_event.is_set():
                return

            # ==============================================
            # CREATE UNIQUE TEMPORARY WAV
            # ==============================================

            fd, output_file = tempfile.mkstemp(
                prefix="jarvis_v10_",
                suffix=".wav",
                dir=self.data_dir,
            )

            os.close(fd)

            # ==============================================
            # WRITE COMPLETE WAV
            # ==============================================

            sf.write(
                output_file,
                samples,
                sample_rate,
            )

            # ==============================================
            # SECOND CANCELLATION CHECK
            # ==============================================

            if stop_event.is_set():
                return

            # ==============================================
            # VERIFY FILE
            # ==============================================

            if not os.path.exists(output_file):
                print(
                    "V10 Kokoro TTS error: "
                    "temporary WAV file disappeared before playback."
                )
                return

            # ==============================================
            # LOAD AUDIO
            # ==============================================

            audio, rate = sf.read(
                output_file,
                dtype="float32",
            )

            if audio.ndim == 1:
                audio = audio.reshape(-1, 1)

            if stop_event.is_set():
                return

            # ==============================================
            # PLAYBACK STATE
            # ==============================================

            position = 0
            position_lock = threading.Lock()

            # ==============================================
            # SOUNDDEVICE CALLBACK
            # ==============================================

            def callback(
                outdata,
                frames,
                time_info,
                status,
            ):
                nonlocal position

                # Normal sounddevice callback status is intentionally
                # hidden from the user-facing JARVIS terminal UI.

                # ------------------------------------------
                # Immediate cancellation check
                # ------------------------------------------

                if stop_event.is_set():
                    outdata.fill(0)
                    raise sd.CallbackStop

                # ------------------------------------------
                # Copy next audio block
                # ------------------------------------------

                with position_lock:
                    remaining = len(audio) - position

                    if remaining <= 0:
                        outdata.fill(0)
                        raise sd.CallbackStop

                    count = min(
                        frames,
                        remaining,
                    )

                    outdata[:count] = audio[
                        position:position + count
                    ]

                    if count < frames:
                        outdata[count:] = 0
                        position += count
                        raise sd.CallbackStop

                    position += count

            # ==============================================
            # START INTERRUPTIBLE PLAYBACK
            # ==============================================

            # Voice engine details are intentionally hidden from
            # the user-facing JARVIS terminal UI.
            stream = sd.OutputStream(
                samplerate=rate,
                channels=audio.shape[1],
                dtype="float32",
                callback=callback,
            )

            with self._lock:
                self._audio_stream = stream

            if stop_event.is_set():
                try:
                    stream.close()
                except Exception:
                    pass
                return

            # Playback start is intentionally hidden from the
            # user-facing JARVIS terminal UI.
            stream.start()

            # ==============================================
            # WAIT FOR PLAYBACK / CANCELLATION
            # ==============================================

            while stream.active:
                if stop_event.wait(0.05):
                    try:
                        stream.abort()
                    except Exception:
                        pass
                    break

                # Give callback-driven playback time to finish.
                time_remaining = (
                    len(audio) - position
                )

                if time_remaining <= 0:
                    break

            # ==============================================
            # FINAL STREAM STOP
            # ==============================================

            try:
                if stream.active:
                    stream.stop()
            except Exception:
                pass

        except Exception as exc:
            print(
                "V10 Kokoro TTS error:",
                exc,
            )

        finally:
            # ==============================================
            # CLOSE ACTIVE STREAM
            # ==============================================

            if stream is not None:
                try:
                    stream.close()
                except Exception:
                    pass

            with self._lock:
                if self._audio_stream is stream:
                    self._audio_stream = None

            # ==============================================
            # CLEAN TEMPORARY WAV
            # ==============================================

            if output_file is not None:
                try:
                    if os.path.exists(output_file):
                        os.remove(output_file)
                except OSError:
                    pass

            # ==============================================
            # CLEAR STATE SAFELY
            # ==============================================

            with self._lock:
                if self._speech_stop_event is stop_event:
                    self._speaking = False
                    self._speech_thread = None
                    self._speech_stop_event = None

    # ==========================================================
    # STOP SPEECH
    # ==========================================================

    def stop(self):
        """
        Cancel the current V10 speech request.

        If Kokoro is still generating audio:
            - cancellation event is set
            - generated audio will not start playback

        If sounddevice playback is active:
            - stream.abort() immediately interrupts playback.

        This method does not join the speech worker because
        Kokoro generation itself cannot be forcibly interrupted.
        """

        with self._lock:
            stop_event = self._speech_stop_event
            stream = self._audio_stream

            if stop_event is not None:
                stop_event.set()

            self._speaking = False

        # ------------------------------------------------------
        # Abort active sounddevice playback.
        #
        # Keep this outside the lock so the audio callback and
        # worker can safely finish their own cleanup.
        # ------------------------------------------------------

        if stream is not None:
            try:
                stream.abort()
            except Exception as exc:
                print(
                    "V10 speaker audio abort error:",
                    exc,
                )

    # ==========================================================
    # STATE
    # ==========================================================

    def is_speaking(self) -> bool:
        """
        Return True while the current V10 speech request is
        generating or actively playing.
        """

        with self._lock:
            return self._speaking
