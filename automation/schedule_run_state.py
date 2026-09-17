from datetime import date


class ScheduleRunState:
    """Track whether a schedule has already executed for an occurrence."""

    def __init__(self) -> None:
        self._last_run_dates: dict[str, date] = {}

    def has_run(
        self,
        schedule_key: str,
        occurrence_date: date,
    ) -> bool:
        """Return True when the schedule already ran for this date."""
        return (
            self._last_run_dates.get(schedule_key)
            == occurrence_date
        )

    def mark_run(
        self,
        schedule_key: str,
        occurrence_date: date,
    ) -> None:
        """Mark a schedule as executed for this date."""
        self._last_run_dates[schedule_key] = occurrence_date

    def clear(self, schedule_key: str) -> None:
        """Clear stored run state for one schedule."""
        self._last_run_dates.pop(schedule_key, None)

    def clear_all(self) -> None:
        """Clear all stored run state."""
        self._last_run_dates.clear()
