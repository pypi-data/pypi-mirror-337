from celery_cloud.entities import Task, TaskRoute
from celery_cloud.exceptions import TaskExecutionException
import boto3
import json
from typing import Any

from celery_cloud.runners.task_execution_strategy import TaskExecutionStrategy


class LambdaTaskExecutionStrategy(TaskExecutionStrategy):
    def execute(self, task: Task, route: TaskRoute) -> Any:
        region = route.module.split(":")[3]
        lambda_client = boto3.client("lambda", region_name=region)

        response = lambda_client.invoke(
            FunctionName=route.module,
            InvocationType="RequestResponse",
            Payload=json.dumps({"args": task.args, "kwargs": task.kwargs}),
        )

        response_payload = json.loads(response["Payload"].read())
        if "FunctionError" in response:
            raise TaskExecutionException(
                message=f"Lambda function {route.module} returned an error",
                detail=response_payload,
            )

        return response_payload.get("body", response_payload)
