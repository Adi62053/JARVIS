from .v9_hardware_capability_model import HardwareOperation


class V9HardwareRiskEvaluator:
    """Determines risk and required privilege for hardware operations."""

    def evaluate(
        self,
        operation: HardwareOperation,
        *,
        protected: bool = False,
        critical: bool = False,
        sensitive: bool = False,
    ) -> tuple[str, str]:

        if not isinstance(operation, HardwareOperation):
            raise TypeError("operation must be HardwareOperation.")

        # Protected hardware remains a hard privileged boundary,
        # including read access.
        if protected:
            return ("CRITICAL", "SYSTEM")

        # Read-only inspection does not modify hardware state.
        if operation == HardwareOperation.READ:
            return ("SAFE", "USER")

        if critical:
            return ("HIGH", "ADMINISTRATOR")

        if sensitive:
            return ("HIGH", "ADMINISTRATOR")

        return ("CAUTION", "USER")

    def get_risk_level(
        self,
        operation: HardwareOperation,
        *,
        protected: bool = False,
        critical: bool = False,
        sensitive: bool = False,
    ) -> str:
        return self.evaluate(
            operation,
            protected=protected,
            critical=critical,
            sensitive=sensitive,
        )[0]

    def get_required_privilege(
        self,
        operation: HardwareOperation,
        *,
        protected: bool = False,
        critical: bool = False,
        sensitive: bool = False,
    ) -> str:
        return self.evaluate(
            operation,
            protected=protected,
            critical=critical,
            sensitive=sensitive,
        )[1]
