from datetime import date, datetime, time

from automation.schedule_model import AutomationSchedule


class SchedulerEngine:
    """Determine whether automation schedules are due."""

    @staticmethod
    def is_due(
        schedule: AutomationSchedule,
        current_time: datetime,
    ) -> bool:
        """Return True when the supplied schedule is due."""
        if not schedule.is_enabled():
            return False

        if not isinstance(current_time, datetime):
            raise TypeError("current_time must be a datetime")

        if current_time.time() < schedule.run_time:
            return False

        if schedule.schedule_type == "ONCE":
            return SchedulerEngine._is_once_due(
                schedule,
                current_time,
            )

        if schedule.schedule_type == "DAILY":
            return SchedulerEngine._is_daily_due(
                schedule,
                current_time,
            )

        if schedule.schedule_type == "WEEKLY":
            return SchedulerEngine._is_weekly_due(
                schedule,
                current_time,
            )

        return False

    @staticmethod
    def _is_once_due(
        schedule: AutomationSchedule,
        current_time: datetime,
    ) -> bool:
        if schedule.run_date is None:
            return False

        return current_time.date() == schedule.run_date

    @staticmethod
    def _is_daily_due(
        schedule: AutomationSchedule,
        current_time: datetime,
    ) -> bool:
        return True

    @staticmethod
    def _is_weekly_due(
        schedule: AutomationSchedule,
        current_time: datetime,
    ) -> bool:
        return current_time.weekday() in schedule.weekdays
