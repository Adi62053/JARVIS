from tools.base import Tool

from pycaw.pycaw import AudioUtilities
import ctypes


class SystemControl(Tool):
    """
    Controls basic Windows system functions.

    V3 currently supports:
    - Volume up
    - Volume down
    - Set exact volume
    - Mute
    - Unmute
    - Lock computer
    """

    @property
    def name(self):
        return "system_control"

    @property
    def description(self):
        return "Controls basic Windows system functions."

    # ==========================================
    # REQUIRED TOOL METHOD
    # ==========================================

    def execute(self, command):
        command = command.lower().strip()

        # Volume up
        if command in [
            "volume up",
            "volume increase",
            "increase volume",
            "increase the volume",
            "turn up volume",
            "turn up the volume",
            "make it louder",
            "louder"
        ]:
            return self.volume_up()

        # Volume down
        if command in [
            "volume down",
            "volume decrease",
            "decrease volume",
            "decrease the volume",
            "turn down volume",
            "turn down the volume",
            "make it quieter",
            "quieter"
        ]:
            return self.volume_down()

        # Mute
        if command in [
            "mute",
            "mute volume",
            "mute the volume"
        ]:
            return self.mute()

        # Unmute
        if command in [
            "unmute",
            "unmute volume",
            "unmute the volume"
        ]:
            return self.unmute()

        # Lock computer
        if command in [
            "lock",
            "lock computer",
            "lock my computer",
            "lock the computer",
            "lock pc",
            "lock my pc"
        ]:
            return self.lock_computer()

        return "I don't have a system control for that command yet."

    # ==========================================
    # GET WINDOWS AUDIO DEVICE
    # ==========================================

    def _get_volume(self):
        """
        Gets the Windows default audio endpoint.
        """

        devices = AudioUtilities.GetSpeakers()

        return devices.EndpointVolume

    # ==========================================
    # VOLUME UP
    # ==========================================

    def volume_up(self):
        try:
            volume = self._get_volume()

            current = volume.GetMasterVolumeLevelScalar()

            new_volume = min(
                current + 0.10,
                1.0
            )

            volume.SetMasterVolumeLevelScalar(
                new_volume,
                None
            )

            percentage = round(new_volume * 100)

            return f"Volume increased to {percentage} percent."

        except Exception as e:
            return f"Could not increase the volume: {e}"

    # ==========================================
    # VOLUME DOWN
    # ==========================================

    def volume_down(self):
        try:
            volume = self._get_volume()

            current = volume.GetMasterVolumeLevelScalar()

            new_volume = max(
                current - 0.10,
                0.0
            )

            volume.SetMasterVolumeLevelScalar(
                new_volume,
                None
            )

            percentage = round(new_volume * 100)

            return f"Volume decreased to {percentage} percent."

        except Exception as e:
            return f"Could not decrease the volume: {e}"

    # ==========================================
    # SET EXACT VOLUME
    # ==========================================

    def set_volume(self, percentage):
        try:
            volume = self._get_volume()

            percentage = max(
                0,
                min(100, int(percentage))
            )

            level = percentage / 100.0

            volume.SetMasterVolumeLevelScalar(
                level,
                None
            )

            return f"Volume is now at {percentage} percent."

        except Exception as e:
            return f"Could not set the volume: {e}"

    # ==========================================
    # MUTE
    # ==========================================

    def mute(self):
        try:
            volume = self._get_volume()

            volume.SetMute(1, None)

            return "Volume muted."

        except Exception as e:
            return f"Could not mute the volume: {e}"

    # ==========================================
    # UNMUTE
    # ==========================================

    def unmute(self):
        try:
            volume = self._get_volume()

            volume.SetMute(0, None)

            return "Volume unmuted."

        except Exception as e:
            return f"Could not unmute the volume: {e}"

    # ==========================================
    # LOCK COMPUTER
    # ==========================================

    def lock_computer(self):
        """
        Locks the current Windows session.
        """

        try:
            result = ctypes.windll.user32.LockWorkStation()

            if result:
                return "Locking the computer, sir."

            return "I could not lock the computer."

        except Exception as e:
            return f"Could not lock the computer: {e}"
