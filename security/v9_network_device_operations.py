"""
JARVIS V9.16.11 + V9.16.12
Network & Device Security Controller Integration
and Controlled Network Operations.

V9.16.11:
- Connects network/device requests to the existing V9 Security Controller.
- Uses existing permission, policy, authorization, elevation and audit flow.
- Does not bypass V9 security.

V9.16.12:
- Provides controlled network adapter operations.
- Actual mutation is opt-in through execute=True.
- Default execution is dry-run.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from security.v9_capability_model import SecurityCapabilityRequest
from security.v9_network_device_model import (
    DeviceInfo,
    DeviceOperation,
    NetworkAdapterInfo,
    NetworkOperation,
)
from security.v9_network_device_security import (
    V9NetworkDeviceSecurityRequestBuilder,
)
from security.v9_security_controller import V9SecurityController


@dataclass(frozen=True)
class NetworkOperationResult:
    operation: NetworkOperation
    adapter_name: str
    executed: bool
    allowed: bool
    message: str


class V9NetworkDeviceSecurityController:
    """
    V9.16.11 integration layer.

    Builds the request and sends it through the existing
    V9 Security Controller.
    """

    def __init__(
        self,
        controller: V9SecurityController | None = None,
    ) -> None:
        self._controller = controller or V9SecurityController()
        self._builder = V9NetworkDeviceSecurityRequestBuilder()

    def evaluate_network(
        self,
        operation: NetworkOperation,
        adapter: NetworkAdapterInfo | None = None,
    ):
        request = self._builder.build_network_request(operation, adapter)
        risk, privilege = self._builder.evaluate_network(operation, adapter)

        decision = self._controller.evaluate(
            operation_id=request.operation_id,
            capability=request.capability,
            resource=request.target,
            risk_level=risk,
            required_privilege=privilege,
        )

        return request, risk, privilege, decision

    def evaluate_device(
        self,
        operation: DeviceOperation,
        device: DeviceInfo,
    ):
        request = self._builder.build_device_request(operation, device)
        risk, privilege = self._builder.evaluate_device(operation, device)

        decision = self._controller.evaluate(
            operation_id=request.operation_id,
            capability=request.capability,
            resource=request.target,
            risk_level=risk,
            required_privilege=privilege,
        )

        return request, risk, privilege, decision


class V9ControlledNetworkOperations:
    """
    V9.16.12 controlled network operations.

    execute=False is the safe default.

    Supported mutation operations:
    - ENABLE
    - DISABLE

    The V9 Security Controller is evaluated before any mutation.
    """

    def __init__(
        self,
        security_controller: V9NetworkDeviceSecurityController | None = None,
    ) -> None:
        self._security = (
            security_controller
            or V9NetworkDeviceSecurityController()
        )

    @staticmethod
    def _validate_adapter_name(adapter_name: str) -> str:
        if not isinstance(adapter_name, str) or not adapter_name.strip():
            raise ValueError("adapter_name cannot be empty")
        return adapter_name.strip()

    @staticmethod
    def _run_powershell(command: str) -> None:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            error = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(
                f"PowerShell network operation failed: {error}"
            )

    def set_adapter_state(
        self,
        adapter: NetworkAdapterInfo,
        operation: NetworkOperation,
        *,
        execute: bool = False,
    ) -> NetworkOperationResult:
        if not isinstance(adapter, NetworkAdapterInfo):
            raise TypeError("adapter must be NetworkAdapterInfo")

        if operation not in (
            NetworkOperation.ENABLE,
            NetworkOperation.DISABLE,
        ):
            raise ValueError(
                "V9.16.12 supports ENABLE and DISABLE only"
            )

        adapter_name = self._validate_adapter_name(adapter.name)

        _, risk, privilege, decision = (
            self._security.evaluate_network(operation, adapter)
        )

        if decision.name != "ALLOW":
            return NetworkOperationResult(
                operation=operation,
                adapter_name=adapter_name,
                executed=False,
                allowed=False,
                message=(
                    f"Security decision: {decision.value}; "
                    f"risk={risk.value}; "
                    f"required_privilege={privilege.value}"
                ),
            )

        if not execute:
            return NetworkOperationResult(
                operation=operation,
                adapter_name=adapter_name,
                executed=False,
                allowed=True,
                message=(
                    f"DRY-RUN: {operation.value} would be executed "
                    f"on adapter '{adapter_name}'"
                ),
            )

        escaped_name = adapter_name.replace("'", "''")

        if operation == NetworkOperation.ENABLE:
            command = (
                f"Enable-NetAdapter -Name '{escaped_name}' "
                "-Confirm:$false"
            )
        else:
            command = (
                f"Disable-NetAdapter -Name '{escaped_name}' "
                "-Confirm:$false"
            )

        self._run_powershell(command)

        return NetworkOperationResult(
            operation=operation,
            adapter_name=adapter_name,
            executed=True,
            allowed=True,
            message=(
                f"{operation.value} executed successfully on "
                f"adapter '{adapter_name}'"
            ),
        )
