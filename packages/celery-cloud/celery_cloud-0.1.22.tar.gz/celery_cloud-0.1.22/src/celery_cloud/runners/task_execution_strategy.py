from abc import ABC, abstractmethod
from typing import Any
from celery_cloud.entities import Task, TaskRoute


class TaskExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, task: Task, route: TaskRoute) -> Any:
        """Execute a task based on the strategy"""
        ...
