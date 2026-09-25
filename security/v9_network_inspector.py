"""
JARVIS V9.16 - Network & Device Inspection Layer

Read-only Windows network and Plug-and-Play device inspection.

This module performs no network or device modifications.
"""

from __future__ import annotations

import json
import subprocess
from typing import Any

from security.v9_network_device_model import (
    DeviceInfo,
    NetworkAdapterInfo,
)


class V9NetworkInspector:
    """Read-only Windows network inspection."""

    @staticmethod
    def _run_powershell(command: str) -> list[dict[str, Any]]:
        """Run a read-only PowerShell query and return JSON records."""

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
            message = result.stderr.strip() or "PowerShell query failed"
            raise RuntimeError(message)

        output = result.stdout.strip()

        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "PowerShell returned invalid JSON"
            ) from exc

        if isinstance(data, dict):
            return [data]

        if isinstance(data, list):
            return data

        return []

    def list_adapters(self) -> list[NetworkAdapterInfo]:
        """Return all network adapters without modifying them."""

        command = (
            "Get-NetAdapter | "
            "Select-Object Name,Status,InterfaceDescription,"
            "MacAddress,LinkSpeed | "
            "ConvertTo-Json -Depth 3 -Compress"
        )

        records = self._run_powershell(command)

        return [
            NetworkAdapterInfo(
                name=str(record.get("Name", "")),
                status=str(record.get("Status", "")),
                interface_description=str(
                    record.get("InterfaceDescription", "")
                ),
                mac_address=(
                    str(record["MacAddress"])
                    if record.get("MacAddress") is not None
                    else None
                ),
                link_speed=(
                    str(record["LinkSpeed"])
                    if record.get("LinkSpeed") is not None
                    else None
                ),
            )
            for record in records
        ]

    def get_adapter(self, name: str) -> NetworkAdapterInfo | None:
        """Return one adapter by exact name."""

        if not isinstance(name, str) or not name.strip():
            raise ValueError("adapter name cannot be empty")

        target = name.strip().casefold()

        for adapter in self.list_adapters():
            if adapter.name.casefold() == target:
                return adapter

        return None

    def get_ip_configuration(self) -> list[dict[str, Any]]:
        """Return current IP configuration information."""

        command = (
            "Get-NetIPConfiguration | "
            "Select-Object InterfaceAlias,InterfaceIndex,"
            "IPv4Address,IPv6Address,DNSServer,"
            "IPv4DefaultGateway,IPv6DefaultGateway | "
            "ConvertTo-Json -Depth 6 -Compress"
        )

        return self._run_powershell(command)

    def get_tcp_connections(self) -> list[dict[str, Any]]:
        """Return current TCP connection information."""

        command = (
            "Get-NetTCPConnection | "
            "Select-Object LocalAddress,LocalPort,"
            "RemoteAddress,RemotePort,State,"
            "OwningProcess | "
            "ConvertTo-Json -Depth 4 -Compress"
        )

        return self._run_powershell(command)

    def get_summary(self) -> dict[str, int]:
        """Return a compact read-only network summary."""

        adapters = self.list_adapters()
        ip_configuration = self.get_ip_configuration()
        tcp_connections = self.get_tcp_connections()

        return {
            "adapter_count": len(adapters),
            "ip_configuration_count": len(ip_configuration),
            "tcp_connection_count": len(tcp_connections),
        }


class V9DeviceInspector:
    """Read-only Windows Plug-and-Play device inspection."""

    @staticmethod
    def _run_powershell(command: str) -> list[dict[str, Any]]:
        """Run a read-only PowerShell device query."""

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
            message = result.stderr.strip() or "PowerShell device query failed"
            raise RuntimeError(message)

        output = result.stdout.strip()

        if not output:
            return []

        try:
            data = json.loads(output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "PowerShell returned invalid device JSON"
            ) from exc

        if isinstance(data, dict):
            return [data]

        if isinstance(data, list):
            return data

        return []

    def list_devices(self) -> list[DeviceInfo]:
        """Return all Plug-and-Play devices without modifying them."""

        command = (
            "Get-PnpDevice | "
            "Select-Object FriendlyName,Status,Class,InstanceId,"
            "Manufacturer | "
            "ConvertTo-Json -Depth 4 -Compress"
        )

        records = self._run_powershell(command)

        devices: list[DeviceInfo] = []

        for record in records:
            devices.append(
                DeviceInfo(
                    name=str(record.get("FriendlyName", "")),
                    status=str(record.get("Status", "")),
                    device_class=str(record.get("Class", "")),
                    instance_id=str(record.get("InstanceId", "")),
                    manufacturer=(
                        str(record["Manufacturer"])
                        if record.get("Manufacturer") is not None
                        else None
                    ),
                )
            )

        return devices

    def get_device(self, instance_id: str) -> DeviceInfo | None:
        """Return one device by exact Plug-and-Play instance ID."""

        if not isinstance(instance_id, str) or not instance_id.strip():
            raise ValueError("instance ID cannot be empty")

        target = instance_id.strip().casefold()

        for device in self.list_devices():
            if device.instance_id.casefold() == target:
                return device

        return None

    def get_summary(self) -> dict[str, int]:
        """Return a compact read-only device summary."""

        devices = self.list_devices()

        status_counts: dict[str, int] = {}

        for device in devices:
            status = device.status or "Unknown"
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "device_count": len(devices),
            **{
                f"status_{key.lower()}": value
                for key, value in sorted(status_counts.items())
            },
        }
