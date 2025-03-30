from celery_cloud.entities import Task, TaskRoute
from typing import Any

from celery_cloud.runners.task_execution_strategy import TaskExecutionStrategy


class LocalTaskExecutionStrategy(TaskExecutionStrategy):
    def execute(self, task: Task, route: TaskRoute) -> Any:
        module = __import__(route.module, fromlist=[route.function])
        function = getattr(module, route.function)
        return function(task.args, task.kwargs)
