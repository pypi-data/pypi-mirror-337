from celery_cloud.entities import Task, TaskRoute
from celery_cloud.exceptions import TaskExecutionException
from typing import Any
from .lambda_strategy import LambdaTaskExecutionStrategy
from .local_strategy import LocalTaskExecutionStrategy


class TaskExecutor:
    def __init__(self):
        self.strategies = {
            "lambda": LambdaTaskExecutionStrategy(),
            "task": LocalTaskExecutionStrategy(),
        }

    def execute(self, task: Task, route: TaskRoute) -> Any:
        strategy = self.strategies.get(route.scheme)
        if not strategy:
            raise TaskExecutionException(
                message=f"Unsupported task scheme: {route.scheme}",
                detail=route.scheme,
            )
        return strategy.execute(task, route)
