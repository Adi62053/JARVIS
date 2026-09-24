import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_protection_manager import (
    ProtectionLevel,
    V9ProtectionManager,
)


manager = V9ProtectionManager()

print(
    "ordinary_path:",
    manager.classify_path(r"C:\Temp\test.txt").value,
)

print(
    "sensitive_path:",
    manager.classify_path(r"C:\Users\Test\file.txt").value,
)

print(
    "critical_path:",
    manager.classify_path(r"C:\Windows\example.txt").value,
)

print(
    "protected_path:",
    manager.classify_path(
        r"C:\Windows\System32\example.dll"
    ).value,
)

print(
    "protected_process:",
    manager.classify_process("lsass.exe").value,
)

print(
    "ordinary_process:",
    manager.classify_process("notepad.exe").value,
)

print(
    "protected_service:",
    manager.classify_service("WinDefend").value,
)

print(
    "ordinary_service:",
    manager.classify_service("SomeUnknownService").value,
)

print(
    "protected_check:",
    manager.is_protected(
        ProtectionLevel.PROTECTED
    ),
)

print(
    "critical_extra_protection:",
    manager.requires_extra_protection(
        ProtectionLevel.CRITICAL
    ),
)

print(
    "ordinary_extra_protection:",
    manager.requires_extra_protection(
        ProtectionLevel.ORDINARY
    ),
)

print("V9.11 protection validation complete")
