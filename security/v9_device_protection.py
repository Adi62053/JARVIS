"""
JARVIS V9.16.7 - Device Classification & Protection

Read-only security classification for Windows Plug-and-Play devices.

This module does not enable, disable, configure, uninstall, or modify
any device or driver.
"""

from __future__ import annotations

from enum import Enum

from security.v9_network_device_model import DeviceInfo
from security.v9_protection_manager import ProtectionLevel


class DeviceProtectionCategory(str, Enum):
    ORDINARY = "ordinary"
    SENSITIVE = "sensitive"
    CRITICAL = "critical"
    PROTECTED = "protected"


class V9DeviceProtectionManager:
    """Classify Windows devices before privileged operations are allowed."""

    _PROTECTED_CLASSES = {
        "system",
        "processor",
        "computer",
        "firmware",
    }

    _CRITICAL_CLASSES = {
        "storage",
        "diskdrive",
        "swd",
        "volume",
        "usb",
        "scsiadapter",
        "hdc",
    }

    _SENSITIVE_CLASSES = {
        "net",
        "netservice",
        "bluetooth",
        "media",
        "audioendpoint",
        "camera",
        "image",
        "hidclass",
        "keyboard",
        "mouse",
        "monitor",
    }

    _PROTECTED_NAME_MARKERS = (
        "microsoft acpi",
        "acpi fixed feature button",
        "system timer",
        "system clock",
        "system speaker",
        "motherboard resources",
        "processor",
        "firmware",
    )

    _CRITICAL_NAME_MARKERS = (
        "disk",
        "storage",
        "usb host controller",
        "usb root hub",
        "pci express root",
        "sata",
        "nvme",
    )

    _SENSITIVE_NAME_MARKERS = (
        "wireless",
        "wi-fi",
        "wifi",
        "bluetooth",
        "ethernet",
        "audio",
        "headset",
        "microphone",
        "camera",
        "webcam",
        "keyboard",
        "mouse",
        "touchpad",
        "display",
        "monitor",
    )

    @staticmethod
    def _normalize(value: str | None) -> str:
        if value is None:
            return ""
        return str(value).strip().casefold()

    def classify_device(
        self,
        device: DeviceInfo,
    ) -> DeviceProtectionCategory:
        """Return the security category for a device."""

        if not isinstance(device, DeviceInfo):
            raise TypeError("device must be a DeviceInfo instance")

        name = self._normalize(device.name)
        device_class = self._normalize(device.device_class)

        if (
            device_class in self._PROTECTED_CLASSES
            or any(marker in name for marker in self._PROTECTED_NAME_MARKERS)
        ):
            return DeviceProtectionCategory.PROTECTED

        if (
            device_class in self._CRITICAL_CLASSES
            or any(marker in name for marker in self._CRITICAL_NAME_MARKERS)
        ):
            return DeviceProtectionCategory.CRITICAL

        if (
            device_class in self._SENSITIVE_CLASSES
            or any(marker in name for marker in self._SENSITIVE_NAME_MARKERS)
        ):
            return DeviceProtectionCategory.SENSITIVE

        return DeviceProtectionCategory.ORDINARY

    def get_protection_level(
        self,
        device: DeviceInfo,
    ) -> ProtectionLevel:
        """Map device classification to the existing V9 protection model."""

        category = self.classify_device(device)

        mapping = {
            DeviceProtectionCategory.ORDINARY: ProtectionLevel.ORDINARY,
            DeviceProtectionCategory.SENSITIVE: ProtectionLevel.SENSITIVE,
            DeviceProtectionCategory.CRITICAL: ProtectionLevel.CRITICAL,
            DeviceProtectionCategory.PROTECTED: ProtectionLevel.PROTECTED,
        }

        return mapping[category]

    def is_protected(self, device: DeviceInfo) -> bool:
        """Return whether the device is inside the protected boundary."""

        return (
            self.classify_device(device)
            == DeviceProtectionCategory.PROTECTED
        )

    def requires_extra_protection(self, device: DeviceInfo) -> bool:
        """Return whether the device requires elevated security handling."""

        return self.classify_device(device) in {
            DeviceProtectionCategory.SENSITIVE,
            DeviceProtectionCategory.CRITICAL,
            DeviceProtectionCategory.PROTECTED,
        }

    def get_category_summary(
        self,
        devices: list[DeviceInfo],
    ) -> dict[str, int]:
        """Return counts by security category."""

        if not isinstance(devices, list):
            raise TypeError("devices must be a list")

        summary = {
            DeviceProtectionCategory.ORDINARY.value: 0,
            DeviceProtectionCategory.SENSITIVE.value: 0,
            DeviceProtectionCategory.CRITICAL.value: 0,
            DeviceProtectionCategory.PROTECTED.value: 0,
        }

        for device in devices:
            category = self.classify_device(device)
            summary[category.value] += 1

        return summary
