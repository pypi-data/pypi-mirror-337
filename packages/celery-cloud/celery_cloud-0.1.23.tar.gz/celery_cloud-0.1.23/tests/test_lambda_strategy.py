import pytest
import json
from unittest.mock import patch, MagicMock
from celery_cloud.runners.lambda_strategy import LambdaTaskExecutionStrategy
from celery_cloud.entities import Task, TaskRoute
from celery_cloud.exceptions import TaskExecutionException

@patch("boto3.client")
def test_lambda_strategy_success(mock_boto_client):
    # Mock de respuesta exitosa
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {
        "Payload": MagicMock(read=lambda: json.dumps({"body": "ok"}).encode())
    }
    mock_boto_client.return_value = mock_lambda

    strategy = LambdaTaskExecutionStrategy()
    task = Task(id="abc", task="t", args=["x"], kwargs={"y": 1})
    route = TaskRoute(scheme="lambda", module="arn:aws:lambda:us-east-1:123456:function:my-fn", function="", query={})

    result = strategy.execute(task, route)
    assert result == "ok"
    mock_lambda.invoke.assert_called_once()

@patch("boto3.client")
def test_lambda_strategy_with_error_response(mock_boto_client):
    # Mock con error de ejecución
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {
        "FunctionError": "Handled",
        "Payload": MagicMock(read=lambda: json.dumps({"error": "fail"}).encode())
    }
    mock_boto_client.return_value = mock_lambda

    strategy = LambdaTaskExecutionStrategy()
    task = Task(id="abc", task="t", args=[], kwargs={})
    route = TaskRoute(scheme="lambda", module="arn:aws:lambda:us-east-1:123456:function:bad-fn", function="", query={})

    with pytest.raises(TaskExecutionException) as exc:
        strategy.execute(task, route)

    assert "Lambda function" in exc.value.message
    assert "returned an error" in exc.value.message
