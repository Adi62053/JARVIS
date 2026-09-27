from enum import Enum
import re

from security.v9_firmware_model import FirmwareResourceType


class FirmwareProtectionLevel(str, Enum):
    ORDINARY = "ORDINARY"
    SENSITIVE = "SENSITIVE"
    CRITICAL = "CRITICAL"
    PROTECTED = "PROTECTED"


class V9FirmwareProtectionManager:
    """
    Defines the security boundary for firmware and boot resources.

    This module performs classification only.
    It does not modify BIOS, UEFI, Secure Boot, BCD,
    system firmware, ACPI, or any firmware state.
    """

    _PROTECTED_TYPES = {
        FirmwareResourceType.BIOS,
        FirmwareResourceType.UEFI,
        FirmwareResourceType.SYSTEM_FIRMWARE,
        FirmwareResourceType.SECURE_BOOT,
    }

    _CRITICAL_TYPES = {
        FirmwareResourceType.SMBIOS,
        FirmwareResourceType.ACPI,
        FirmwareResourceType.BCD_FIRMWARE,
    }

    _PROTECTED_MARKERS = (
        "bios",
        "uefi",
        "firmware",
        "secure_boot",
        "secureboot",
        "spi",
    )

    _CRITICAL_MARKERS = (
        "acpi",
        "smbios",
        "bcd",
        "bootmgr",
        "boot manager",
    )

    def classify(
        self,
        resource_type: FirmwareResourceType,
        identifier: str = "",
    ) -> FirmwareProtectionLevel:
        if not isinstance(resource_type, FirmwareResourceType):
            raise TypeError("resource_type must be a FirmwareResourceType")

        if not isinstance(identifier, str):
            raise TypeError("identifier must be a string")

        normalized_identifier = identifier.strip().lower()

        if resource_type in self._PROTECTED_TYPES:
            return FirmwareProtectionLevel.PROTECTED

        protected_pattern = r"(^|[\s_\\/:.\-])(" + "|".join(
            re.escape(marker)
            for marker in self._PROTECTED_MARKERS
        ) + r")($|[\s_\\/:.\-])"

        if re.search(protected_pattern, normalized_identifier):
            return FirmwareProtectionLevel.PROTECTED

        if resource_type in self._CRITICAL_TYPES:
            return FirmwareProtectionLevel.CRITICAL

        critical_pattern = r"(^|[\s_\\/:.\-])(" + "|".join(
            re.escape(marker)
            for marker in self._CRITICAL_MARKERS
        ) + r")($|[\s_\\/:.\-])"

        if re.search(critical_pattern, normalized_identifier):
            return FirmwareProtectionLevel.CRITICAL

        return FirmwareProtectionLevel.SENSITIVE

    def get_protection_level(
        self,
        resource_type: FirmwareResourceType,
        identifier: str = "",
    ) -> FirmwareProtectionLevel:
        return self.classify(resource_type, identifier)

    def is_protected(
        self,
        resource_type: FirmwareResourceType,
        identifier: str = "",
    ) -> bool:
        return (
            self.classify(resource_type, identifier)
            == FirmwareProtectionLevel.PROTECTED
        )

    def requires_extra_protection(
        self,
        resource_type: FirmwareResourceType,
        identifier: str = "",
    ) -> bool:
        level = self.classify(resource_type, identifier)

        return level in {
            FirmwareProtectionLevel.CRITICAL,
            FirmwareProtectionLevel.PROTECTED,
        }
