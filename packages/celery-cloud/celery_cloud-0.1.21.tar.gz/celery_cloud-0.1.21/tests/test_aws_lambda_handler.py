import pytest
from unittest.mock import patch, MagicMock
from celery_cloud.runners.aws_lambda import lambda_handler
from celery_cloud.entities import Task


@patch("celery_cloud.runners.aws_lambda.settings")
@patch("celery_cloud.runners.aws_lambda.call_task")
@patch("celery_cloud.runners.aws_lambda.TaskModel.update_task")
@patch("celery_cloud.runners.aws_lambda.TaskModel.insert_task")
@patch("celery_cloud.runners.aws_lambda.get_task")
@patch("celery_cloud.runners.aws_lambda.SQSMessage")
@patch("celery_cloud.runners.aws_lambda.get_event")
def test_lambda_handler_success(
    mock_get_event,
    mock_sqs_message_class,
    mock_get_task,
    mock_insert_task,
    mock_update_task,
    mock_call_task,
    mock_settings,
):
    # Configuración de mocks
    mock_settings.TASKS = {"my.task": "task://module/function"}
    fake_task = Task(id="abc123", task="my.task", args=[], kwargs={})
    mock_get_task.return_value = fake_task
    mock_call_task.return_value = {"result": 42}

    # Mock del mensaje SQS y record
    mock_record = MagicMock()
    mock_record.messageId = "msg-1"
    mock_record.get_message.return_value = {
        "body": "{}",
        "content-encoding": "utf-8",
        "content-type": "application/json",
        "headers": {
            "lang": "py",
            "task": "my.task",
            "id": "abc123",
            "retries": 0,
            "timelimit": [None, None],
            "root_id": "abc123",
            "argsrepr": "[]",
            "kwargsrepr": "{}",
            "origin": "unittest",
            "ignore_result": False,
            "replaced_task_nesting": 0,
            "stamps": {},
        },
        "properties": {
            "correlation_id": "abc",
            "reply_to": "r",
            "delivery_mode": 2,
            "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
            "priority": 0,
            "body_encoding": "base64",
            "delivery_tag": "xyz",
        },
    }

    mock_get_event.return_value = MagicMock(Records=[mock_record])
    mock_sqs_message_class.return_value = MagicMock()

    # Ejecutar lambda_handler
    result = lambda_handler({"Records": [{}]}, context={})

    # Validaciones
    assert result["status"] == "completed"
    assert result["processed_messages"] == 1
    assert result["failed_messages"] == 0
    assert len(result["processed_tasks"]) == 1
    assert result["processed_tasks"][0]["task_id"] == "abc123"
    assert result["processed_tasks"][0]["status"] == "SUCCESS"


@patch("celery_cloud.runners.aws_lambda.settings")
@patch("celery_cloud.runners.aws_lambda.TaskModel.update_task")
@patch("celery_cloud.runners.aws_lambda.TaskModel.insert_task")
@patch("celery_cloud.runners.aws_lambda.get_task")
@patch("celery_cloud.runners.aws_lambda.SQSMessage")
@patch("celery_cloud.runners.aws_lambda.get_event")
def test_lambda_handler_unsupported_task(
    mock_get_event,
    mock_sqs_message_class,
    mock_get_task,
    mock_insert_task,
    mock_update_task,
    mock_settings,
):
    # Configura una tarea no soportada
    mock_settings.TASKS = {}

    task_id = "abc123"
    fake_task = Task(id=task_id, task="unknown.task", args=[], kwargs={})
    mock_get_task.return_value = fake_task

    mock_record = MagicMock()
    mock_record.messageId = "msg-2"
    mock_record.get_message.return_value = {
        "body": "{}",
        "content-encoding": "utf-8",
        "content-type": "application/json",
        "headers": {
            "lang": "py",
            "task": "unknown.task",
            "id": task_id,
            "retries": 0,
            "timelimit": [None, None],
            "root_id": task_id,
            "argsrepr": "[]",
            "kwargsrepr": "{}",
            "origin": "unittest",
            "ignore_result": False,
            "replaced_task_nesting": 0,
            "stamps": {},
        },
        "properties": {
            "correlation_id": "abc",
            "reply_to": "r",
            "delivery_mode": 2,
            "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
            "priority": 0,
            "body_encoding": "base64",
            "delivery_tag": "xyz",
        },
    }

    mock_get_event.return_value = MagicMock(Records=[mock_record])
    mock_sqs_message_class.return_value = MagicMock()

    result = lambda_handler({"Records": [{}]}, context={})

    assert result["status"] == "completed"
    assert result["processed_messages"] == 0
    assert result["failed_messages"] == 1
    assert result["failed_tasks"][0]["task_id"] == task_id
    assert "not supported" in result["failed_tasks"][0]["error"]


@patch("celery_cloud.runners.aws_lambda.settings")
@patch("celery_cloud.runners.aws_lambda.call_task", side_effect=Exception("boom"))
@patch("celery_cloud.runners.aws_lambda.TaskModel.update_task")
@patch("celery_cloud.runners.aws_lambda.TaskModel.insert_task")
@patch("celery_cloud.runners.aws_lambda.get_task")
@patch("celery_cloud.runners.aws_lambda.SQSMessage")
@patch("celery_cloud.runners.aws_lambda.get_event")
def test_lambda_handler_call_task_raises(
    mock_get_event,
    mock_sqs_message_class,
    mock_get_task,
    mock_insert_task,
    mock_update_task,
    mock_call_task,
    mock_settings,
):
    # Tarea válida en settings
    mock_settings.TASKS = {"my.task": "task://mod/fn"}

    fake_task = Task(id="abc123", task="my.task", args=[], kwargs={})
    mock_get_task.return_value = fake_task

    mock_record = MagicMock()
    mock_record.messageId = "msg-3"
    mock_record.get_message.return_value = {
        "body": "{}",
        "content-encoding": "utf-8",
        "content-type": "application/json",
        "headers": {
            "lang": "py",
            "task": "my.task",
            "id": "abc123",
            "retries": 0,
            "timelimit": [None, None],
            "root_id": "abc123",
            "argsrepr": "[]",
            "kwargsrepr": "{}",
            "origin": "unittest",
            "ignore_result": False,
            "replaced_task_nesting": 0,
            "stamps": {},
        },
        "properties": {
            "correlation_id": "abc",
            "reply_to": "r",
            "delivery_mode": 2,
            "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
            "priority": 0,
            "body_encoding": "base64",
            "delivery_tag": "xyz",
        },
    }

    mock_get_event.return_value = MagicMock(Records=[mock_record])
    mock_sqs_message_class.return_value = MagicMock()

    result = lambda_handler({"Records": [{}]}, context={})

    assert result["status"] == "error"
    assert "General error" in result["message"]
    assert "boom" in result["details"]
