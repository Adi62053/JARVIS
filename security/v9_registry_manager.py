"""
JARVIS V9.14 - Windows Registry Management

Controlled Windows Registry inspection.

This module:
- reads registry keys and values
- checks whether registry paths exist
- protects sensitive registry locations
- does not bypass Windows security
- does not modify registry values yet
"""

from __future__ import annotations

from dataclasses import dataclass
import winreg

from security.v9_protection_manager import (
    ProtectionLevel,
    V9ProtectionManager,
)


@dataclass(frozen=True)
class RegistryValueInfo:
    """Information about one registry value."""

    name: str
    value: object
    value_type: int


@dataclass(frozen=True)
class RegistryKeyInfo:
    """Information about a registry key."""

    hive: str
    path: str
    protection_level: ProtectionLevel


class V9RegistryManager:
    """Controlled Windows Registry inspection."""

    _HIVES = {
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKCR": winreg.HKEY_CLASSES_ROOT,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKU": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
        "HKCC": winreg.HKEY_CURRENT_CONFIG,
    }

    _PROTECTED_PREFIXES = (
        r"SAM",
        r"SECURITY",
    )

    def __init__(
        self,
        protection_manager: V9ProtectionManager | None = None,
    ) -> None:
        self.protection_manager = (
            protection_manager or V9ProtectionManager()
        )

    def normalize_hive(
        self,
        hive: str,
    ) -> str:
        """Return the canonical hive name."""

        if not isinstance(hive, str):
            raise TypeError("hive must be a string")

        hive = hive.strip().upper()

        if hive not in self._HIVES:
            raise ValueError(
                f"Unsupported registry hive: {hive}"
            )

        if hive == "HKLM":
            return "HKEY_LOCAL_MACHINE"

        if hive == "HKCU":
            return "HKEY_CURRENT_USER"

        if hive == "HKCR":
            return "HKEY_CLASSES_ROOT"

        if hive == "HKU":
            return "HKEY_USERS"

        if hive == "HKCC":
            return "HKEY_CURRENT_CONFIG"

        return hive

    def _get_hive_handle(
        self,
        hive: str,
    ):
        """Return a Windows registry hive handle."""

        canonical = self.normalize_hive(hive)
        return self._HIVES[canonical]

    def classify_key(
        self,
        hive: str,
        path: str,
    ) -> RegistryKeyInfo:
        """Classify a registry key using V9 protection rules."""

        if not isinstance(path, str):
            raise TypeError("path must be a string")

        path = path.strip()

        if not path:
            raise ValueError("path must not be empty")

        canonical_hive = self.normalize_hive(hive)

        normalized_path = path.replace("/", "\\").strip("\\")
        upper_path = normalized_path.upper()

        protection = self.protection_manager.classify_path(
            f"{canonical_hive}\\{normalized_path}"
        )

        if canonical_hive == "HKEY_LOCAL_MACHINE":
            for prefix in self._PROTECTED_PREFIXES:
                if (
                    upper_path == prefix
                    or upper_path.startswith(prefix + "\\")
                ):
                    protection = ProtectionLevel.PROTECTED
                    break

        return RegistryKeyInfo(
            hive=canonical_hive,
            path=normalized_path,
            protection_level=protection,
        )

    def create_key(
        self,
        hive: str,
        path: str,
    ) -> bool:
        """Create a registry key after protection validation."""

        self._check_read_protection(hive, path)

        handle = self._get_hive_handle(hive)

        key = winreg.CreateKeyEx(
            handle,
            path,
            0,
            winreg.KEY_WRITE,
        )

        winreg.CloseKey(key)
        return True

    def key_exists(
        self,
        hive: str,
        path: str,
    ) -> bool:
        """Return True when a registry key exists."""

        handle = self._get_hive_handle(hive)

        try:
            key = winreg.OpenKey(
                handle,
                path,
                0,
                winreg.KEY_READ,
            )
        except FileNotFoundError:
            return False

        winreg.CloseKey(key)
        return True

    def read_value(
        self,
        hive: str,
        path: str,
        value_name: str,
    ) -> RegistryValueInfo:
        """Read one registry value."""

        if not isinstance(value_name, str):
            raise TypeError(
                "value_name must be a string"
            )

        self._check_read_protection(hive, path)

        handle = self._get_hive_handle(hive)

        key = winreg.OpenKey(
            handle,
            path,
            0,
            winreg.KEY_READ,
        )

        try:
            value, value_type = winreg.QueryValueEx(
                key,
                value_name,
            )
        finally:
            winreg.CloseKey(key)

        return RegistryValueInfo(
            name=value_name,
            value=value,
            value_type=value_type,
        )

    def write_value(
        self,
        hive: str,
        path: str,
        value_name: str,
        value: object,
        value_type: int = winreg.REG_SZ,
    ) -> bool:
        """Write one registry value after protection validation."""

        if not isinstance(value_name, str):
            raise TypeError(
                "value_name must be a string"
            )

        self._check_read_protection(hive, path)

        handle = self._get_hive_handle(hive)

        key = winreg.OpenKey(
            handle,
            path,
            0,
            winreg.KEY_SET_VALUE,
        )

        try:
            winreg.SetValueEx(
                key,
                value_name,
                0,
                value_type,
                value,
            )
        finally:
            winreg.CloseKey(key)

        return True

    def list_values(
        self,
        hive: str,
        path: str,
    ) -> list[RegistryValueInfo]:
        """List values contained in a registry key."""

        self._check_read_protection(hive, path)

        handle = self._get_hive_handle(hive)

        key = winreg.OpenKey(
            handle,
            path,
            0,
            winreg.KEY_READ,
        )

        values: list[RegistryValueInfo] = []

        try:
            index = 0

            while True:
                try:
                    name, value, value_type = (
                        winreg.EnumValue(key, index)
                    )
                except OSError:
                    break

                values.append(
                    RegistryValueInfo(
                        name=name,
                        value=value,
                        value_type=value_type,
                    )
                )

                index += 1
        finally:
            winreg.CloseKey(key)

        return values

    def _check_read_protection(
        self,
        hive: str,
        path: str,
    ) -> None:
        """Validate registry read access against V9 protection."""

        info = self.classify_key(hive, path)

        if info.protection_level == ProtectionLevel.PROTECTED:
            raise PermissionError(
                "Protected registry key cannot be accessed "
                "through V9.14 registry management"
            )
