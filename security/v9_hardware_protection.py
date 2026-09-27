from enum import Enum

from .v9_hardware_capability_model import HardwareResourceType


class HardwareProtectionCategory(str, Enum):
    ORDINARY = "ordinary"
    SENSITIVE = "sensitive"
    CRITICAL = "critical"
    PROTECTED = "protected"


class V9HardwareProtectionManager:
    """Classifies hardware resources into security protection categories."""

    PROTECTED_TYPES = {
        HardwareResourceType.MOTHERBOARD,
        HardwareResourceType.BIOS,
    }

    CRITICAL_TYPES = {
        HardwareResourceType.CPU,
        HardwareResourceType.MEMORY,
        HardwareResourceType.GPU,
        HardwareResourceType.STORAGE,
    }

    SENSITIVE_TYPES = {
        HardwareResourceType.BATTERY,
        HardwareResourceType.USB,
    }

    def classify(
        self,
        resource_type: HardwareResourceType,
        identifier: str = "",
    ) -> HardwareProtectionCategory:

        if not isinstance(resource_type, HardwareResourceType):
            raise TypeError("resource_type must be HardwareResourceType.")

        if not isinstance(identifier, str):
            raise TypeError("identifier must be a string.")

        normalized = identifier.strip().casefold()

        if resource_type in self.PROTECTED_TYPES:
            return HardwareProtectionCategory.PROTECTED

        if resource_type in self.CRITICAL_TYPES:
            return HardwareProtectionCategory.CRITICAL

        if resource_type in self.SENSITIVE_TYPES:
            return HardwareProtectionCategory.SENSITIVE

        # Additional identifier-level protection.
        if any(
            marker in normalized
            for marker in (
                "firmware",
                "uefi",
                "bios",
                "motherboard",
            )
        ):
            return HardwareProtectionCategory.PROTECTED

        return HardwareProtectionCategory.ORDINARY

    def get_protection_level(
        self,
        resource_type: HardwareResourceType,
        identifier: str = "",
    ) -> HardwareProtectionCategory:
        return self.classify(resource_type, identifier)

    def is_protected(
        self,
        resource_type: HardwareResourceType,
        identifier: str = "",
    ) -> bool:
        return (
            self.classify(resource_type, identifier)
            == HardwareProtectionCategory.PROTECTED
        )

    def requires_extra_protection(
        self,
        resource_type: HardwareResourceType,
        identifier: str = "",
    ) -> bool:
        return self.classify(
            resource_type,
            identifier,
        ) != HardwareProtectionCategory.ORDINARY
