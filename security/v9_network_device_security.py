"""
JARVIS V9.16.10 - Network & Device Permission Integration

Builds security resources using the existing V9 capability model.

Risk and required privilege are evaluated separately by the V9.16
risk evaluators. No network or device operations are executed here.
"""

from __future__ import annotations

from security.v9_capability_model import (
    SecurityCapabilityRequest,
    SecurityResource,
)
from security.v9_device_risk import V9DeviceRiskEvaluator
from security.v9_network_device_capability import (
    get_device_capability,
    get_network_capability,
    map_device_operation,
    map_network_operation,
)
from security.v9_network_device_model import (
    DeviceInfo,
    DeviceOperation,
    NetworkAdapterInfo,
    NetworkOperation,
)
from security.v9_network_risk import V9NetworkRiskEvaluator


class V9NetworkDeviceSecurityRequestBuilder:
    """Build V9 security requests without executing operations."""

    def __init__(self) -> None:
        self._network_risk = V9NetworkRiskEvaluator()
        self._device_risk = V9DeviceRiskEvaluator()

    def build_network_request(
        self,
        operation: NetworkOperation,
        adapter: NetworkAdapterInfo | None = None,
    ) -> SecurityCapabilityRequest:
        if not isinstance(operation, NetworkOperation):
            raise TypeError("operation must be a NetworkOperation")

        self._network_risk.evaluate(operation, adapter)

        identifier = (
            adapter.name.strip()
            if adapter is not None
            else "network"
        )

        resource = SecurityResource(
            capability=get_network_capability(),
            operation=map_network_operation(operation),
            resource=identifier,
        )

        return SecurityCapabilityRequest(
            operation_id=f"network.{operation.value}",
            resource=resource,
        )

    def build_device_request(
        self,
        operation: DeviceOperation,
        device: DeviceInfo,
    ) -> SecurityCapabilityRequest:
        if not isinstance(operation, DeviceOperation):
            raise TypeError("operation must be a DeviceOperation")

        if not isinstance(device, DeviceInfo):
            raise TypeError("device must be a DeviceInfo")

        self._device_risk.evaluate(device, operation)

        resource = SecurityResource(
            capability=get_device_capability(),
            operation=map_device_operation(operation),
            resource=device.instance_id,
        )

        return SecurityCapabilityRequest(
            operation_id=f"device.{operation.value}",
            resource=resource,
        )

    def evaluate_network(
        self,
        operation: NetworkOperation,
        adapter: NetworkAdapterInfo | None = None,
    ):
        """Return network risk and required privilege without execution."""

        return self._network_risk.evaluate(operation, adapter)

    def evaluate_device(
        self,
        operation: DeviceOperation,
        device: DeviceInfo,
    ):
        """Return device risk and required privilege without execution."""

        return self._device_risk.evaluate(device, operation)
