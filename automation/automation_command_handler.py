import re

from automation.automation_conditions import AutomationCondition
from automation.automation_model import AutomationStep


class AutomationCommandHandler:
    """Parse user commands for automation management."""

    def __init__(self, manager):
        self.manager = manager

    def handle(self, command: str) -> str:
        """Handle one automation command."""
        if not isinstance(command, str):
            return "Invalid automation command."

        command = command.strip()

        if not command:
            return "Please provide an automation command."

        lowered = command.lower()

        if lowered.startswith("create automation"):
            return self._create(command)

        if lowered in {
            "list automations",
            "show automations",
        }:
            return self._list()

        if lowered.startswith("show automation"):
            return self._show(command)

        if lowered.startswith("enable automation"):
            return self._enable(command)

        if lowered.startswith("disable automation"):
            return self._disable(command)

        if lowered.startswith("delete automation"):
            return self._delete(command)

        if lowered.startswith("add step to automation"):
            return self._add_step(command)

        if lowered.startswith("remove step from automation"):
            return self._remove_step(command)

        if lowered.startswith("add condition to automation"):
            return self._add_condition(command)

        if lowered.startswith("remove condition from automation"):
            return self._remove_condition(command)

        if lowered.startswith("show conditions for automation"):
            return self._show_conditions(command)

        return "Unknown automation command."

    def _create(self, command: str) -> str:
        match = re.match(
            r"^create automation\s+(.+?)(?:\s+description\s+(.+))?$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return "Please provide an automation name."

        name = match.group(1).strip()
        description = (match.group(2) or "").strip()

        try:
            automation = self.manager.create(
                name=name,
                description=description,
            )
        except ValueError as exc:
            return str(exc)

        return f"Automation created: {automation.name}"

    def _list(self) -> str:
        automations = self.manager.list_all()

        if not automations:
            return "No automations found."

        lines = []

        for automation in automations:
            status = (
                "enabled"
                if automation.enabled
                else "disabled"
            )

            lines.append(
                f"{automation.name} "
                f"({status}, "
                f"{automation.step_count()} steps, "
                f"{automation.condition_count()} conditions)"
            )

        return "\n".join(lines)

    def _show(self, command: str) -> str:
        match = re.match(
            r"^show automation\s+(.+)$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return "Please provide an automation name."

        name = match.group(1).strip()
        automation = self.manager.get(name)

        if automation is None:
            return f"Automation not found: {name}"

        status = (
            "enabled"
            if automation.enabled
            else "disabled"
        )

        lines = [
            f"Automation: {automation.name}",
            f"Description: {automation.description}",
            f"Status: {status}",
            f"Conditions: {automation.condition_count()}",
            f"Steps: {automation.step_count()}",
        ]

        return "\n".join(lines)

    def _enable(self, command: str) -> str:
        match = re.match(
            r"^enable automation\s+(.+)$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return "Please provide an automation name."

        name = match.group(1).strip()

        try:
            automation = self.manager.enable(name)
        except ValueError as exc:
            return str(exc)

        return f"Automation enabled: {automation.name}"

    def _disable(self, command: str) -> str:
        match = re.match(
            r"^disable automation\s+(.+)$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return "Please provide an automation name."

        name = match.group(1).strip()

        try:
            automation = self.manager.disable(name)
        except ValueError as exc:
            return str(exc)

        return f"Automation disabled: {automation.name}"

    def _delete(self, command: str) -> str:
        match = re.match(
            r"^delete automation\s+(.+)$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return "Please provide an automation name."

        name = match.group(1).strip()

        try:
            self.manager.delete(name)
        except ValueError as exc:
            return str(exc)

        return f"Automation deleted: {name}"

    def _add_step(self, command: str) -> str:
        match = re.match(
            r"^add step to automation\s+(.+?)\s+"
            r"action\s+([A-Za-z_]+)"
            r"(?:\s+parameters\s+(.+?))?"
            r"(?:\s+security\s+([A-Za-z]+))?$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return (
                "Please provide an automation name, "
                "action, and optional parameters."
            )

        name = match.group(1).strip()
        action = match.group(2).strip()
        parameters_text = (
            (match.group(3) or "").strip()
        )
        security_level = (
            (match.group(4) or "SAFE").strip()
        )

        parameters = {}

        if parameters_text:
            parameter_parts = [
                part.strip()
                for part in parameters_text.split()
            ]

            for part in parameter_parts:
                if "=" not in part:
                    continue

                key, value = part.split(
                    "=",
                    1,
                )

                parameters[key] = value

        step = AutomationStep(
            action=action,
            parameters=parameters,
            security_level=security_level,
        )

        try:
            automation = self.manager.add_step(
                name=name,
                step=step,
            )
        except (TypeError, ValueError) as exc:
            return str(exc)

        return (
            f"Step added to {automation.name}: "
            f"{step.action}"
        )

    def _remove_step(self, command: str) -> str:
        match = re.match(
            r"^remove step from automation\s+"
            r"(.+?)\s+(\d+)$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return (
                "Please provide an automation name "
                "and step number."
            )

        name = match.group(1).strip()
        step_number = int(match.group(2))

        try:
            automation = self.manager.remove_step(
                name=name,
                step_number=step_number,
            )
        except (TypeError, ValueError, IndexError) as exc:
            return str(exc)

        removed_number = step_number

        if automation.step_count() >= removed_number:
            removed_number = step_number

        return (
            f"Step {removed_number} removed from "
            f"{automation.name}."
        )

    def _add_condition(self, command: str) -> str:
        match = re.match(
            r"^add condition to automation\s+"
            r"(.+?)\s+"
            r"type\s+(ALWAYS|VALUE_EQUALS|VALUE_NOT_EQUALS)"
            r"(?:\s+value_name\s+(.+?))?"
            r"(?:\s+expected\s+(.+))?$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return (
                "Please provide an automation name, "
                "condition type, and required values."
            )

        name = match.group(1).strip()
        condition_type = match.group(2).strip()
        value_name = (
            (match.group(3) or "value").strip()
        )
        expected_value = match.group(4)

        if expected_value is not None:
            expected_value = expected_value.strip()

        if (
            condition_type.upper() != "ALWAYS"
            and expected_value is None
        ):
            return (
                f"{condition_type.upper()} requires "
                "an expected value."
            )

        try:
            condition = AutomationCondition(
                condition_type=condition_type,
                expected_value=expected_value,
                value_name=value_name,
            )

            automation = self.manager.add_condition(
                name=name,
                condition=condition,
            )

        except (TypeError, ValueError) as exc:
            return str(exc)

        return (
            f"Condition added to {automation.name}: "
            f"{condition.condition_type}"
        )

    def _remove_condition(self, command: str) -> str:
        match = re.match(
            r"^remove condition from automation\s+"
            r"(.+?)\s+(\d+)$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return (
                "Please provide an automation name "
                "and condition number."
            )

        name = match.group(1).strip()
        condition_number = int(match.group(2))

        try:
            automation = self.manager.remove_condition(
                name=name,
                condition_number=condition_number,
            )
        except (TypeError, ValueError, IndexError) as exc:
            return str(exc)

        return (
            f"Condition {condition_number} removed from "
            f"{automation.name}."
        )

    def _show_conditions(self, command: str) -> str:
        match = re.match(
            r"^show conditions for automation\s+(.+)$",
            command,
            re.IGNORECASE,
        )

        if not match:
            return "Please provide an automation name."

        name = match.group(1).strip()
        automation = self.manager.get(name)

        if automation is None:
            return f"Automation not found: {name}"

        if not automation.conditions:
            return (
                f"No conditions found for "
                f"{automation.name}."
            )

        lines = []

        for index, condition in enumerate(
            automation.conditions,
            start=1,
        ):
            if condition.condition_type == "ALWAYS":
                detail = "ALWAYS"
            else:
                detail = (
                    f"{condition.condition_type} "
                    f"{condition.value_name} "
                    f"expected={condition.expected_value}"
                )

            lines.append(
                f"Condition {index}: {detail}"
            )

        return "\n".join(lines)
