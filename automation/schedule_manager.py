from datetime import date, time

from automation.schedule_model import AutomationSchedule
from automation.schedule_storage import ScheduleStorage


class ScheduleManager:
    """High-level management for V8 automation schedules."""

    def __init__(
        self,
        storage: ScheduleStorage | None = None,
    ) -> None:
        self.storage = storage or ScheduleStorage()
        self._schedules = self.storage.load()

    def _save(self) -> None:
        self.storage.save(self._schedules)

    def create(
        self,
        automation_name: str,
        schedule_type: str,
        run_time: time,
        run_date: date | None = None,
        weekdays: list[int] | None = None,
    ) -> AutomationSchedule:
        """Create and persist a new schedule."""
        if self.get(automation_name) is not None:
            raise ValueError(
                f"Schedule already exists for automation: "
                f"{automation_name}"
            )

        schedule = AutomationSchedule(
            automation_name=automation_name,
            schedule_type=schedule_type,
            run_time=run_time,
            run_date=run_date,
            weekdays=weekdays or [],
        )

        self._schedules.append(schedule)
        self._save()

        return schedule

    def get(
        self,
        automation_name: str,
    ) -> AutomationSchedule | None:
        """Return a schedule by automation name."""
        for schedule in self._schedules:
            if schedule.automation_name.lower() == automation_name.lower():
                return schedule

        return None

    def list_all(self) -> list[AutomationSchedule]:
        """Return all schedules."""
        return list(self._schedules)

    def enable(
        self,
        automation_name: str,
    ) -> bool:
        """Enable a schedule."""
        schedule = self.get(automation_name)

        if schedule is None:
            return False

        schedule.enable()
        self._save()

        return True

    def disable(
        self,
        automation_name: str,
    ) -> bool:
        """Disable a schedule."""
        schedule = self.get(automation_name)

        if schedule is None:
            return False

        schedule.disable()
        self._save()

        return True

    def delete(
        self,
        automation_name: str,
    ) -> bool:
        """Delete a schedule."""
        schedule = self.get(automation_name)

        if schedule is None:
            return False

        self._schedules.remove(schedule)
        self._save()

        return True
