"""
JARVIS V9.12 - Process Management

Windows process inspection and controlled process management.

This module:
- lists running processes
- inspects individual processes
- searches for processes by name
- starts processes
- stops/terminates non-protected processes
- protects critical processes through V9.11
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
class ProcessInfo:
    """Basic information about a running process."""

    pid: int
    name: str
    protection_level: ProtectionLevel


class V9ProcessManager:
    """Process inspection and controlled process management."""

    def __init__(
        self,
        protection_manager: V9ProtectionManager | None = None,
    ) -> None:
        self.protection_manager = (
            protection_manager or V9ProtectionManager()
        )

    def list_processes(self) -> list[ProcessInfo]:
        """Return running processes using Windows tasklist."""

        result = subprocess.run(
            [
                "tasklist",
                "/FO",
                "CSV",
                "/NH",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
                or "Unable to retrieve process list"
            )

        processes: list[ProcessInfo] = []

        for line in result.stdout.splitlines():
            line = line.strip()

            if not line:
                continue

            parts = self._parse_csv_line(line)

            if len(parts) < 2:
                continue

            name = parts[0].strip()
            pid_text = parts[1].strip()

            try:
                pid = int(pid_text)
            except ValueError:
                continue

            protection = self.protection_manager.classify_process(
                name
            )

            processes.append(
                ProcessInfo(
                    pid=pid,
                    name=name,
                    protection_level=protection,
                )
            )

        return processes

    def find_processes(
        self,
        name: str,
    ) -> list[ProcessInfo]:
        """Find processes whose executable name matches exactly."""

        if not isinstance(name, str):
            raise TypeError("name must be a string")

        name = name.strip().lower()

        if not name:
            raise ValueError("name must not be empty")

        return [
            process
            for process in self.list_processes()
            if process.name.lower() == name
        ]

    def get_process(
        self,
        pid: int,
    ) -> ProcessInfo | None:
        """Return process information for a PID."""

        if not isinstance(pid, int):
            raise TypeError("pid must be an integer")

        if pid <= 0:
            raise ValueError("pid must be greater than zero")

        for process in self.list_processes():
            if process.pid == pid:
                return process

        return None

    def start_process(
        self,
        executable: str,
        *arguments: str,
    ) -> int:
        """Start a process and return its PID."""

        if not isinstance(executable, str):
            raise TypeError("executable must be a string")

        executable = executable.strip()

        if not executable:
            raise ValueError(
                "executable must not be empty"
            )

        command = [executable]

        for argument in arguments:
            if not isinstance(argument, str):
                raise TypeError(
                    "process arguments must be strings"
                )

            command.append(argument)

        process = subprocess.Popen(command)

        return process.pid

    def terminate_process(
        self,
        pid: int,
        force: bool = False,
    ) -> bool:
        """
        Terminate a process when it is not protected.

        Protected and critical processes are refused before
        termination.

        force=False requests normal termination.
        force=True requests Windows force termination.
        """

        if not isinstance(pid, int):
            raise TypeError("pid must be an integer")

        if pid <= 0:
            raise ValueError(
                "pid must be greater than zero"
            )

        if not isinstance(force, bool):
            raise TypeError(
                "force must be a boolean"
            )

        process = self.get_process(pid)

        if process is None:
            return False

        if process.protection_level in {
            ProtectionLevel.PROTECTED,
            ProtectionLevel.CRITICAL,
        }:
            raise PermissionError(
                "Protected process cannot be terminated "
                "through V9.12 process management"
            )

        command = [
            "taskkill",
            "/PID",
            str(pid),
        ]

        if force:
            command.append("/F")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        return result.returncode == 0

    @staticmethod
    def _parse_csv_line(line: str) -> list[str]:
        """Parse one tasklist CSV row safely."""

        if not line.startswith('"'):
            return []

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