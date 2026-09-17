from datetime import datetime

from automation.automation_conditions import ConditionEvaluator
from automation.automation_manager import AutomationManager
from automation.condition_context import ConditionContext
from automation.schedule_manager import ScheduleManager
from automation.scheduler_engine import SchedulerEngine
from automation.schedule_run_state import ScheduleRunState
from automation.workflow_runner import WorkflowRunner


class ScheduleRunner:
    """Find and execute automations whose schedules are due."""

    def __init__(
        self,
        automation_manager=None,
        schedule_manager=None,
        workflow_runner=None,
        run_state=None,
    ):
        self.automation_manager = (
            automation_manager or AutomationManager()
        )
        self.schedule_manager = (
            schedule_manager or ScheduleManager()
        )
        self.workflow_runner = (
            workflow_runner or WorkflowRunner()
        )
        self.run_state = run_state or ScheduleRunState()

    def _conditions_pass(
        self,
        automation,
        context: ConditionContext,
    ) -> bool:
        """Return True when all automation conditions pass."""
        for condition in automation.conditions:
            if not ConditionEvaluator.evaluate(
                condition,
                context=context,
            ):
                return False

        return True

    def run_due(self, current_time: datetime) -> list[object]:
        """Execute each due automation once for the current date."""
        results = []

        schedules = self.schedule_manager.list_all()

        for schedule in schedules:
            if not SchedulerEngine.is_due(
                schedule,
                current_time,
            ):
                continue

            schedule_key = schedule.automation_name

            if self.run_state.has_run(
                schedule_key,
                current_time.date(),
            ):
                continue

            automation = self.automation_manager.get(
                schedule.automation_name
            )

            if automation is None:
                continue

            context = ConditionContext(values={})

            if not self._conditions_pass(
                automation,
                context,
            ):
                continue

            execution_results = self.workflow_runner.run(
                automation
            )

            results.extend(execution_results)

            self.run_state.mark_run(
                schedule_key,
                current_time.date(),
            )

        return results
