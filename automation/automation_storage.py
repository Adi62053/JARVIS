"""
JARVIS V8 - Automation Storage

Provides local JSON persistence for automation definitions.

This module does not execute automation actions.
"""

import json
from pathlib import Path

from automation.automation_conditions import AutomationCondition
from automation.automation_model import Automation, AutomationStep


class AutomationStorage:
    """Save and load automation definitions locally."""

    def __init__(self, file_path: str = "data/automations.json") -> None:
        self.file_path = Path(file_path)

    def save(self, automations: list[Automation]) -> None:
        """Save automations to the local JSON file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        data = []

        for automation in automations:
            data.append(
                {
                    "name": automation.name,
                    "description": automation.description,
                    "enabled": automation.enabled,
                    "conditions": [
                        {
                            "condition_type": condition.condition_type,
                            "expected_value": condition.expected_value,
                            "value_name": condition.value_name,
                        }
                        for condition in automation.conditions
                    ],
                    "steps": [
                        {
                            "action": step.action,
                            "parameters": step.parameters,
                            "security_level": step.security_level,
                        }
                        for step in automation.steps
                    ],
                }
            )

        self.file_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def load(self) -> list[Automation]:
        """Load automation definitions from the local JSON file."""
        if not self.file_path.exists():
            return []

        raw_data = json.loads(
            self.file_path.read_text(encoding="utf-8")
        )

        automations = []

        for item in raw_data:
            automation = Automation(
                name=item["name"],
                description=item.get("description", ""),
                enabled=item.get("enabled", True),
            )

            for condition_data in item.get("conditions", []):
                automation.add_condition(
                    AutomationCondition(
                        condition_type=condition_data[
                            "condition_type"
                        ],
                        expected_value=condition_data.get(
                            "expected_value"
                        ),
                        value_name=condition_data.get(
                            "value_name",
                            "value",
                        ),
                    )
                )

            for step_data in item.get("steps", []):
                automation.add_step(
                    AutomationStep(
                        action=step_data["action"],
                        parameters=step_data.get("parameters", {}),
                        security_level=step_data.get(
                            "security_level",
                            "SAFE",
                        ),
                    )
                )

            automations.append(automation)

        return automations
