import json
import subprocess
from typing import Any

from .v9_hardware_capability_model import (
    BIOSInfo,
    BatteryInfo,
    CPUInfo,
    GPUInfo,
    MemoryInfo,
    MotherboardInfo,
    StorageInfo,
    USBDeviceInfo,
)


class V9HardwareInspector:
    """Read-only Windows hardware inspection layer."""

    def _run_powershell(self, command: str) -> list[dict[str, Any]]:
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
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"PowerShell command failed: {result.stderr.strip()}"
            )

        output = result.stdout.strip()

        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid JSON returned by PowerShell: {output[:500]}"
            ) from exc

        if isinstance(data, dict):
            return [data]

        if isinstance(data, list):
            return data

        raise RuntimeError("Unexpected PowerShell JSON result type.")

    def get_cpu(self) -> CPUInfo:
        rows = self._run_powershell(
            "Get-CimInstance Win32_Processor | "
            "Select-Object Name,NumberOfCores,"
            "NumberOfLogicalProcessors,MaxClockSpeed | "
            "ConvertTo-Json -Compress"
        )

        row = rows[0]

        return CPUInfo(
            name=str(row.get("Name") or ""),
            cores=int(row.get("NumberOfCores") or 0),
            logical_processors=int(
                row.get("NumberOfLogicalProcessors") or 0
            ),
            max_clock_speed_mhz=int(row.get("MaxClockSpeed") or 0),
        )

    def get_memory(self) -> MemoryInfo:
        rows = self._run_powershell(
            "Get-CimInstance Win32_ComputerSystem | "
            "Select-Object TotalPhysicalMemory | "
            "ConvertTo-Json -Compress"
        )

        row = rows[0]

        return MemoryInfo(
            total_physical_bytes=int(
                row.get("TotalPhysicalMemory") or 0
            )
        )

    def get_gpus(self) -> list[GPUInfo]:
        rows = self._run_powershell(
            "Get-CimInstance Win32_VideoController | "
            "Select-Object Name,AdapterRAM,DriverVersion,Status | "
            "ConvertTo-Json -Compress"
        )

        return [
            GPUInfo(
                name=str(row.get("Name") or ""),
                adapter_ram_bytes=(
                    int(row["AdapterRAM"])
                    if row.get("AdapterRAM") is not None
                    else None
                ),
                driver_version=(
                    str(row["DriverVersion"])
                    if row.get("DriverVersion") is not None
                    else None
                ),
                status=str(row.get("Status") or ""),
            )
            for row in rows
        ]

    def get_storage(self) -> list[StorageInfo]:
        rows = self._run_powershell(
            "Get-CimInstance Win32_DiskDrive | "
            "Select-Object Model,InterfaceType,MediaType,Size,Status | "
            "ConvertTo-Json -Compress"
        )

        return [
            StorageInfo(
                model=str(row.get("Model") or ""),
                interface_type=(
                    str(row["InterfaceType"])
                    if row.get("InterfaceType") is not None
                    else None
                ),
                media_type=(
                    str(row["MediaType"])
                    if row.get("MediaType") is not None
                    else None
                ),
                size_bytes=(
                    int(row["Size"])
                    if row.get("Size") is not None
                    else None
                ),
                status=str(row.get("Status") or ""),
            )
            for row in rows
        ]

    def get_motherboard(self) -> MotherboardInfo:
        rows = self._run_powershell(
            "Get-CimInstance Win32_BaseBoard | "
            "Select-Object Manufacturer,Product,SerialNumber | "
            "ConvertTo-Json -Compress"
        )

        row = rows[0]

        return MotherboardInfo(
            manufacturer=str(row.get("Manufacturer") or ""),
            product=(
                str(row["Product"])
                if row.get("Product") is not None
                else None
            ),
            serial_number=(
                str(row["SerialNumber"])
                if row.get("SerialNumber") is not None
                else None
            ),
        )

    def get_bios(self) -> BIOSInfo:
        rows = self._run_powershell(
            "Get-CimInstance Win32_BIOS | "
            "Select-Object Manufacturer,SMBIOSBIOSVersion,ReleaseDate | "
            "ConvertTo-Json -Compress"
        )

        row = rows[0]

        return BIOSInfo(
            manufacturer=str(row.get("Manufacturer") or ""),
            version=str(row.get("SMBIOSBIOSVersion") or ""),
            release_date=(
                str(row["ReleaseDate"])
                if row.get("ReleaseDate") is not None
                else None
            ),
        )

    def get_batteries(self) -> list[BatteryInfo]:
        rows = self._run_powershell(
            "Get-CimInstance Win32_Battery | "
            "Select-Object Name,BatteryStatus,"
            "EstimatedChargeRemaining | "
            "ConvertTo-Json -Compress"
        )

        return [
            BatteryInfo(
                name=str(row.get("Name") or ""),
                status_code=(
                    int(row["BatteryStatus"])
                    if row.get("BatteryStatus") is not None
                    else None
                ),
                charge_percent=(
                    int(row["EstimatedChargeRemaining"])
                    if row.get("EstimatedChargeRemaining") is not None
                    else None
                ),
            )
            for row in rows
        ]

    def get_usb_devices(self) -> list[USBDeviceInfo]:
        rows = self._run_powershell(
            "Get-PnpDevice -Class USB | "
            "Select-Object FriendlyName,Status,InstanceId | "
            "ConvertTo-Json -Compress"
        )

        return [
            USBDeviceInfo(
                name=str(row.get("FriendlyName") or ""),
                status=str(row.get("Status") or ""),
                instance_id=str(row.get("InstanceId") or ""),
            )
            for row in rows
        ]

    def get_summary(self) -> dict[str, int]:
        return {
            "gpu_count": len(self.get_gpus()),
            "storage_count": len(self.get_storage()),
            "battery_count": len(self.get_batteries()),
            "usb_device_count": len(self.get_usb_devices()),
        }
