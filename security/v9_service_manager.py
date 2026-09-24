"""
JARVIS V9.13 - Windows Service Management

Windows service inspection and controlled service management.

This module:
- lists Windows services
- inspects individual services
- searches for services by name
- classifies protected services
- provides controlled start/stop/restart operations
- does not bypass Windows security
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from security.v9_protection_manager import (
    ProtectionLevel,
    V9ProtectionManager,
)


@dataclass(frozen=True)
class ServiceInfo:
    """Basic information about a Windows service."""

    name: str
    display_name: str
    status: str
    protection_level: ProtectionLevel


class V9ServiceManager:
    """Windows service inspection and controlled management."""

    def __init__(
        self,
        protection_manager: V9ProtectionManager | None = None,
    ) -> None:
        self.protection_manager = (
            protection_manager or V9ProtectionManager()
        )

    def list_services(self) -> list[ServiceInfo]:
        """Return Windows services using PowerShell CIM."""

        command = [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            (
                "Get-CimInstance Win32_Service | "
                "Select-Object Name,DisplayName,State | "
                "ConvertTo-Csv -NoTypeInformation"
            ),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or "Unable to retrieve Windows services"
            )

        lines = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        if len(lines) < 2:
            return []

        services: list[ServiceInfo] = []

        for line in lines[1:]:
            parts = self._parse_csv_line(line)

            if len(parts) < 3:
                continue

            name = parts[0].strip()
            display_name = parts[1].strip()
            status = parts[2].strip()

            if not name:
                continue

            protection = (
                self.protection_manager.classify_service(
                    name
                )
            )

            services.append(
                ServiceInfo(
                    name=name,
                    display_name=display_name,
                    status=status,
                    protection_level=protection,
                )
            )

        return services

    def find_services(
        self,
        name: str,
    ) -> list[ServiceInfo]:
        """Find services by exact service name."""

        if not isinstance(name, str):
            raise TypeError("name must be a string")

        name = name.strip().lower()

        if not name:
            raise ValueError("name must not be empty")

        return [
            service
            for service in self.list_services()
            if service.name.lower() == name
        ]

    def get_service(
        self,
        name: str,
    ) -> ServiceInfo | None:
        """Return service information by service name."""

        services = self.find_services(name)

        if not services:
            return None

        return services[0]

    def start_service(
        self,
        name: str,
    ) -> bool:
        """Start a non-protected Windows service."""

        service = self.get_service(name)

        if service is None:
            return False

        self._check_service_protection(service)

        result = subprocess.run(
            [
                "sc.exe",
                "start",
                service.name,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        return result.returncode == 0

    def stop_service(
        self,
        name: str,
    ) -> bool:
        """Stop a non-protected Windows service."""

        service = self.get_service(name)

        if service is None:
            return False

        self._check_service_protection(service)

        result = subprocess.run(
            [
                "sc.exe",
                "stop",
                service.name,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        return result.returncode == 0

    def restart_service(
        self,
        name: str,
    ) -> bool:
        """Restart a non-protected Windows service."""

        service = self.get_service(name)

        if service is None:
            return False

        self._check_service_protection(service)

        stop_result = self.stop_service(
            service.name
        )

        if not stop_result:
            return False

        return self.start_service(
            service.name
        )

    @staticmethod
    def _check_service_protection(
        service: ServiceInfo,
    ) -> None:
        """Block operations against protected services."""

        if service.protection_level in {
            ProtectionLevel.PROTECTED,
            ProtectionLevel.CRITICAL,
        }:
            raise PermissionError(
                "Protected service cannot be modified "
                "through V9.13 service management"
            )

    @staticmethod
    def _parse_csv_line(
        line: str,
    ) -> list[str]:
        """Parse one CSV row safely."""

        values: list[str] = []
        current: list[str] = []
        inside_quotes = False

        for character in line:
            if character == '"':
                inside_quotes = not inside_quotes
                continue

            if character == "," and not inside_quotes:
                values.append("".join(current))
                current = []
                continue

            current.append(character)

        values.append("".join(current))

        return values
