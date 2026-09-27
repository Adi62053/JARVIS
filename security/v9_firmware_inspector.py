from __future__ import annotations

import json
import subprocess

from .v9_firmware_model import (
    BCDFirmwareInfo,
    BIOSInfo,
    FirmwareDeviceInfo,
    UEFIInfo,
)


class V9FirmwareInspector:
    """Read-only Windows firmware, BIOS, UEFI, and boot inspection."""

    @staticmethod
    def _run_powershell(command: str):
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"PowerShell command failed: {result.stderr.strip()}"
            )

        output = result.stdout.strip()

        if not output:
            return None

        try:
            return json.loads(output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "PowerShell returned invalid JSON"
            ) from exc

    def get_bios(self) -> BIOSInfo:
        data = self._run_powershell(
            """
            $bios = Get-CimInstance Win32_BIOS
            $bios |
                Select-Object Manufacturer,
                    SMBIOSBIOSVersion,
                    Version,
                    ReleaseDate,
                    SerialNumber |
                ConvertTo-Json -Compress
            """
        )

        if not isinstance(data, dict):
            raise RuntimeError("Invalid BIOS inspection result")

        return BIOSInfo(
            manufacturer=str(data.get("Manufacturer", "")),
            version=str(
                data.get("SMBIOSBIOSVersion")
                or data.get("Version")
                or ""
            ),
            release_date=str(data.get("ReleaseDate", "")),
            serial_number=str(data.get("SerialNumber", "")),
        )

    def get_uefi(self) -> UEFIInfo:
        firmware_type = self._run_powershell(
            """
            (Get-ComputerInfo -Property BiosFirmwareType).BiosFirmwareType |
                ConvertTo-Json -Compress
            """
        )

        secure_boot = self._run_powershell(
            """
            try {
                $secureBootState = Confirm-SecureBootUEFI
            }
            catch {
                $secureBootState = $false
            }

            $secureBootState | ConvertTo-Json -Compress
            """
        )

        return UEFIInfo(
            firmware_type=str(firmware_type or ""),
            secure_boot_enabled=bool(secure_boot),
        )

    def get_firmware_devices(self) -> list[FirmwareDeviceInfo]:
        data = self._run_powershell(
            """
            Get-PnpDevice |
                Where-Object {
                    $_.Class -eq 'Firmware' -or
                    $_.FriendlyName -match 'Firmware|UEFI|BIOS'
                } |
                Select-Object Status, Class, FriendlyName, InstanceId |
                ConvertTo-Json -Compress
            """
        )

        if data is None:
            return []

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            raise RuntimeError("Invalid firmware device result")

        devices = []

        for item in data:
            if not isinstance(item, dict):
                continue

            devices.append(
                FirmwareDeviceInfo(
                    name=str(item.get("FriendlyName", "")),
                    status=str(item.get("Status", "")),
                    instance_id=str(item.get("InstanceId", "")),
                )
            )

        return devices

    def get_system_firmware_devices(
        self,
    ) -> list[FirmwareDeviceInfo]:
        data = self._run_powershell(
            """
            Get-CimInstance Win32_PnPEntity |
                Where-Object {
                    $_.PNPClass -eq 'Firmware' -or
                    $_.Name -match 'Firmware|UEFI|BIOS'
                } |
                Select-Object Status, PNPClass, Name, DeviceID |
                ConvertTo-Json -Compress
            """
        )

        if data is None:
            return []

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            raise RuntimeError("Invalid system firmware device result")

        devices = []

        for item in data:
            if not isinstance(item, dict):
                continue

            devices.append(
                FirmwareDeviceInfo(
                    name=str(item.get("Name", "")),
                    status=str(item.get("Status", "")),
                    instance_id=str(item.get("DeviceID", "")),
                )
            )

        return devices

    def get_bcd_firmware(self) -> list[BCDFirmwareInfo]:
        result = subprocess.run(
            [
                "bcdedit.exe",
                "/enum",
                "firmware",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"bcdedit inspection failed: {result.stderr.strip()}"
            )

        entries = []
        current = {}

        for raw_line in result.stdout.splitlines():
            line = raw_line.strip()

            if not line:
                if current.get("identifier"):
                    entries.append(
                        BCDFirmwareInfo(
                            identifier=current.get("identifier", ""),
                            description=current.get("description", ""),
                            device=current.get("device", ""),
                            path=current.get("path", ""),
                        )
                    )
                    current = {}
                continue

            if line.endswith(":"):
                continue

            if " " not in line:
                continue

            key, value = line.split(None, 1)

            if key in {
                "identifier",
                "description",
                "device",
                "path",
            }:
                current[key] = value

        if current.get("identifier"):
            entries.append(
                BCDFirmwareInfo(
                    identifier=current.get("identifier", ""),
                    description=current.get("description", ""),
                    device=current.get("device", ""),
                    path=current.get("path", ""),
                )
            )

        return entries

    def get_summary(self) -> dict:
        bios = self.get_bios()
        uefi = self.get_uefi()
        firmware_devices = self.get_firmware_devices()
        system_devices = self.get_system_firmware_devices()
        bcd_entries = self.get_bcd_firmware()

        return {
            "bios": bios,
            "uefi": uefi,
            "firmware_device_count": len(firmware_devices),
            "system_firmware_device_count": len(system_devices),
            "bcd_firmware_entry_count": len(bcd_entries),
        }
