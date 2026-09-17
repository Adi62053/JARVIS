import json
from dataclasses import asdict
from datetime import date, time
from pathlib import Path

from automation.schedule_model import AutomationSchedule


class ScheduleStorage:
    """Local JSON persistence for V8 automation schedules."""

    def __init__(
        self,
        file_path: str | Path = "data/schedules.json",
    ) -> None:
        self.file_path = Path(file_path)

    def load(self) -> list[AutomationSchedule]:
        """Load all schedules from local JSON storage."""
        if not self.file_path.exists():
            return []

        with self.file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Schedule storage must contain a JSON list."
            )

        schedules: list[AutomationSchedule] = []

        for item in data:
            if not isinstance(item, dict):
                raise ValueError(
                    "Each stored schedule must be a JSON object."
                )

            schedules.append(
                AutomationSchedule(
                    automation_name=item["automation_name"],
                    schedule_type=item["schedule_type"],
                    run_time=time.fromisoformat(
                        item["run_time"]
                    ),
                    run_date=(
                        date.fromisoformat(item["run_date"])
                        if item.get("run_date")
                        else None
                    ),
                    weekdays=item.get("weekdays", []),
                    enabled=item.get("enabled", True),
                )
            )

        return schedules

    def save(
        self,
        schedules: list[AutomationSchedule],
    ) -> None:
        """Save all schedules to local JSON storage."""
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        serialized = []

        for schedule in schedules:
            data = asdict(schedule)

            data["run_time"] = schedule.run_time.isoformat()

            data["run_date"] = (
                schedule.run_date.isoformat()
                if schedule.run_date is not None
                else None
            )

            serialized.append(data)

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                serialized,
                file,
                indent=4,
            )
