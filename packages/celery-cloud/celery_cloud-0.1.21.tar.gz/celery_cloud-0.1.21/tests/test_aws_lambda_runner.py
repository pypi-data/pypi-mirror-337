import pytest
from unittest.mock import patch, MagicMock
from celery_cloud.runners.aws_lambda import (
    call_lambda_task,
    call_local_task,
    call_task,
    get_event,
    get_message,
    get_task,
    TaskRoute,
    TaskExecutionException,
    EventDecodeException,
    MessageDecodeException,
    TaskDecodeException,
)
from celery_cloud.entities import SQSEvent, SQSMessage, Task
from celery_cloud.models.task_model import TaskModel
import json


# ===================================
# call_lambda_task
# ===================================


@patch("boto3.client")
def test_call_lambda_task_success(mock_boto):
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {
        "Payload": MagicMock(read=lambda: json.dumps({"body": "ok"}).encode())
    }
    mock_boto.return_value = mock_lambda

    task = Task(id="t1", task="demo", args=[], kwargs={})
    route = TaskRoute("lambda", "arn:aws:lambda:us-east-1:123:function:name", "", {})
    result = call_lambda_task(task, route)
    assert result == "ok"


@patch("boto3.client")
def test_call_lambda_task_error(mock_boto):
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {
        "Payload": MagicMock(read=lambda: json.dumps({"error": "fail"}).encode()),
        "FunctionError": "Handled",
    }
    mock_boto.return_value = mock_lambda

    task = Task(id="t1", task="demo", args=[], kwargs={})
    route = TaskRoute("lambda", "arn:aws:lambda:us-east-1:123:function:name", "", {})
    with pytest.raises(TaskExecutionException):
        call_lambda_task(task, route)


# ===================================
# call_local_task
# ===================================


@patch("builtins.__import__")
def test_call_local_task_success(mock_import):
    fake_module = MagicMock()
    fake_module.test_func.return_value = "done"
    mock_import.return_value = fake_module

    task = Task(id="t1", task="local_task", args=[], kwargs={})
    route = TaskRoute("task", "some_mod", "test_func", {})
    result = call_local_task(task, route)
    assert result == "done"


@patch("builtins.__import__")
def test_call_local_task_missing_func(mock_import):
    fake_module = MagicMock()
    del fake_module.non_existent
    mock_import.return_value = fake_module

    task = Task(id="t1", task="demo", args=[], kwargs={})
    route = TaskRoute("task", "some_mod", "non_existent", {})
    with pytest.raises(AttributeError):
        call_local_task(task, route)


# ===================================
# call_task
# ===================================


@patch("celery_cloud.runners.aws_lambda.call_local_task")
@patch("celery_cloud.runners.aws_lambda.settings")
def test_call_task_supported_task(mock_settings, mock_local_call):
    mock_local_call.return_value = 42
    mock_settings.TASKS = {"my.task": "task://mod/fn"}

    task = Task(id="123", task="my.task", args=[], kwargs={})
    result = call_task(task)
    assert result == 42


@patch("celery_cloud.runners.aws_lambda.settings")
def test_call_task_invalid_scheme(mock_settings):
    mock_settings.TASKS = {"weird.task": "ftp://host/path"}

    task = Task(id="123", task="weird.task", args=[], kwargs={})
    with pytest.raises(TaskExecutionException):
        call_task(task)


# ===================================
# get_event
# ===================================


def test_get_event_valid():
    result = get_event({"Records": []})
    assert isinstance(result, SQSEvent)


def test_get_event_invalid():
    with pytest.raises(EventDecodeException):
        get_event({"bad": "input"})


# ===================================
# get_message
# ===================================


def test_get_message_valid():
    record = MagicMock()
    record.get_message.return_value = {
        "body": "{}",
        "content-encoding": "utf-8",
        "content-type": "application/json",
        "headers": {
            "lang": "py",
            "task": "test.fn",
            "id": "abc",
            "retries": 0,
            "timelimit": [None, None],
            "root_id": "abc",
            "argsrepr": "[]",
            "kwargsrepr": "{}",
            "origin": "test",
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
    msg = get_message(record)
    assert isinstance(msg, SQSMessage)


def test_get_message_invalid_validation_error():
    record = MagicMock()
    record.get_message.return_value = {
        "body": "{}",
        "content-encoding": "utf-8",
        "content-type": "application/json",
        "headers": {"invalid": "headers"},
        "properties": {},
    }

    with pytest.raises(MessageDecodeException):
        get_message(record)


# ===================================
# get_task
# ===================================


def test_get_task_valid():
    headers = {
        "lang": "py",
        "task": "test.fn",
        "id": "abc",
        "retries": 0,
        "timelimit": [None, None],
        "root_id": "abc",
        "argsrepr": "[]",
        "kwargsrepr": "{}",
        "origin": "test",
        "ignore_result": False,
        "replaced_task_nesting": 0,
        "stamps": {},
    }
    props = {
        "correlation_id": "abc",
        "reply_to": "r",
        "delivery_mode": 2,
        "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
        "priority": 0,
        "body_encoding": "base64",
        "delivery_tag": "xyz",
    }
    msg = SQSMessage(
        body="{}",
        content_encoding="utf-8",
        content_type="application/json",
        headers=headers,
        properties=props,
    )
    task = get_task(msg)
    assert task.task == "test.fn"


def test_get_task_invalid_argsrepr():
    headers = {
        "lang": "py",
        "task": "test.fn",
        "id": "abc",
        "retries": 0,
        "timelimit": [None, None],
        "root_id": "abc",
        "argsrepr": "[INVALID",  # eval fallará aquí
        "kwargsrepr": "{}",
        "origin": "test",
        "ignore_result": False,
        "replaced_task_nesting": 0,
        "stamps": {},
    }
    props = {
        "correlation_id": "abc",
        "reply_to": "r",
        "delivery_mode": 2,
        "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
        "priority": 0,
        "body_encoding": "base64",
        "delivery_tag": "xyz",
    }
    msg = SQSMessage(
        body="{}",
        content_encoding="utf-8",
        content_type="application/json",
        headers=headers,
        properties=props,
    )

    with pytest.raises(TaskDecodeException) as exc:
        get_task(msg)

    assert "Exception getting task" in str(exc.value.message)
