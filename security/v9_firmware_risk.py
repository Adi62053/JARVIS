from security.v9_firmware_model import FirmwareOperation


class V9FirmwareRiskEvaluator:
    def evaluate(
        self,
        operation: FirmwareOperation,
        *,
        protection_level="SENSITIVE",
    ) -> tuple[str, str]:
        if not isinstance(operation, FirmwareOperation):
            raise TypeError("operation must be a FirmwareOperation")

        if hasattr(protection_level, "value"):
            level = str(protection_level.value).upper()
        else:
            level = str(protection_level).upper()

        if level == "PROTECTED":
            return ("CRITICAL", "SYSTEM")

        if operation == FirmwareOperation.READ:
            if level == "CRITICAL":
                return ("HIGH", "ADMINISTRATOR")
            if level == "SENSITIVE":
                return ("SAFE", "USER")
            return ("SAFE", "USER")

        if level == "CRITICAL":
            return ("CRITICAL", "SYSTEM")

        if level == "SENSITIVE":
            return ("HIGH", "ADMINISTRATOR")

        return ("CAUTION", "USER")
