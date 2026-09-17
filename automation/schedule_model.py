from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class AutomationSchedule:
    """
    V8.9 scheduling data model.

    Supported schedule types:
    - ONCE
    - DAILY
    - WEEKLY
    """

    automation_name: str
    schedule_type: str
    run_time: time
    run_date: date | None = None
    weekdays: list[int] = field(default_factory=list)
    enabled: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.automation_name, str):
            raise TypeError("automation_name must be a string")

        self.automation_name = self.automation_name.strip()

        if not self.automation_name:
            raise ValueError("automation_name cannot be empty")

        if not isinstance(self.schedule_type, str):
            raise TypeError("schedule_type must be a string")

        self.schedule_type = self.schedule_type.strip().upper()

        supported_types = {
            "ONCE",
            "DAILY",
            "WEEKLY",
        }

        if self.schedule_type not in supported_types:
            raise ValueError(
                f"Unsupported schedule type: {self.schedule_type}"
            )

        if not isinstance(self.run_time, time):
            raise TypeError("run_time must be a datetime.time")

        if self.schedule_type == "ONCE" and self.run_date is None:
            raise ValueError("ONCE schedules require run_date")

        if self.schedule_type != "ONCE" and self.run_date is not None:
            raise ValueError(
                "run_date is only valid for ONCE schedules"
            )

        if self.schedule_type == "WEEKLY":
            if not self.weekdays:
                raise ValueError(
                    "WEEKLY schedules require at least one weekday"
                )

            for weekday in self.weekdays:
                if not isinstance(weekday, int):
                    raise TypeError(
                        "weekday values must be integers"
                    )

                if weekday < 0 or weekday > 6:
                    raise ValueError(
                        "weekday values must be between 0 and 6"
                    )

        if self.schedule_type != "WEEKLY" and self.weekdays:
            raise ValueError(
                "weekdays are only valid for WEEKLY schedules"
            )

        if not isinstance(self.enabled, bool):
            raise TypeError("enabled must be a boolean")

    def is_enabled(self) -> bool:
        return self.enabled

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False
