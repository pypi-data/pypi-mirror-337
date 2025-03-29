import pytest
from unittest.mock import patch, MagicMock
from celery_cloud.runners.aws_lambda_runner import (
    parse_task_url,
    call_lambda_task,
    call_local_task,
    call_task,
    get_event,
    get_message,
    get_task,
    lambda_handler,
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
# parse_task_url
# ===================================

def test_parse_task_url_basic():
    url = "task://my_module/my_function"
    route = parse_task_url(url)
    assert route.scheme == "task"
    assert route.module == "my_module"
    assert route.function == "my_function"
    assert route.query == {}

def test_parse_task_url_with_query():
    url = "task://my_mod/my_func?x=1&y=2"
    route = parse_task_url(url)
    assert route.query == {"x": ["1"], "y": ["2"]}

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
        "FunctionError": "Handled"
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

@patch("celery_cloud.runners.aws_lambda_runner.call_local_task")
@patch("celery_cloud.runners.aws_lambda_runner.settings")
def test_call_task_supported_task(mock_settings, mock_local_call):
    mock_local_call.return_value = 42
    mock_settings.TASKS = {"my.task": "task://mod/fn"}

    task = Task(id="123", task="my.task", args=[], kwargs={})
    result = call_task(task)
    assert result == 42

@patch("celery_cloud.runners.aws_lambda_runner.settings")
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
            "delivery_info": {
                "exchange": "default",
                "routing_key": "task_queue"
            },
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
        "delivery_info": {
            "exchange": "default",
            "routing_key": "task_queue"
        },
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
        "delivery_info": {
            "exchange": "default",
            "routing_key": "task_queue"
        },
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




# from unittest.mock import AsyncMock, MagicMock, Mock, patch

# import pytest


# from celery_cloud.entities import (
#     Task,
#     FailedTask,
#     LambdaResponse,
#     ProcessedTask,
#     SQSEvent,
#     SQSMessage,
#     SQSRecord,
# )
# from celery_cloud.exceptions import (
#     BackendException,
#     EventDecodeException,
#     MessageDecodeException,
#     TaskDecodeException,
#     TaskExecutionException,
# )
# from celery_cloud.logging import logger, trace_id_context
# from celery_cloud.models.task_model import TaskModel
# from celery_cloud.settings import settings

# from celery_cloud.runners.aws_lambda_runner import (
#     TaskRoute,
#     call_lambda_task,
#     call_local_task,
#     call_task,
#     get_event,
#     get_message,
#     get_task,
#     lambda_handler,
#     parse_task_url,
# )


# # TODO: Add more tests
# def test_parse_task_url_with_query_params():
#     url = "task://my_module/my_function?param1=value1&param2=value2"
#     result = parse_task_url(url)

#     assert result == TaskRoute(
#         scheme="task",
#         module="my_module",
#         function="my_function",
#         query={"param1": ["value1"], "param2": ["value2"]},
#     )


# @patch("boto3.client")
# def test_call_lambda_task_with_error(mock_boto_client):

#     mock_lambda_client = MagicMock()
#     mock_boto_client.return_value = mock_lambda_client
#     mock_lambda_client.invoke.return_value = {
#         "Payload": MagicMock(read=lambda: '{"errorMessage": "error"}'),
#         "FunctionError": "Unhandled",
#     }

#     task = Task(id="1", task="test_task", args=[], kwargs={})
#     route = TaskRoute(
#         scheme="lambda",
#         module="arn:aws:lambda:us-east-1:123456789012:function:my-function",
#         function="",
#         query={},
#     )

#     with pytest.raises(TaskExecutionException) as exc_info:
#         call_lambda_task(task, route)
#     assert "Lambda function" in str(exc_info.value)


# @patch("builtins.__import__")
# def test_call_local_task_with_invalid_function(mock_import):
#     fake_module = MagicMock()
#     # Evita que tenga 'non_existent_function'
#     del fake_module.non_existent_function  # esto es seguro incluso si no existe

#     mock_import.return_value = fake_module

#     task = Task(id="1", task="test_task", args=[], kwargs={})
#     route = TaskRoute(
#         scheme="task", module="my_module", function="non_existent_function", query={}
#     )

#     with pytest.raises(AttributeError):
#         call_local_task(task, route)


# @patch("celery_cloud.runners.aws_lambda_runner.settings")
# def test_call_task_with_unsupported_scheme(mock_settings):
#     mock_settings.TASKS = {"test_task": "unsupported:my_module.my_function"}
#     task = Task(id="1", task="test_task", args=[], kwargs={})

#     with pytest.raises(TaskExecutionException) as exc_info:
#         call_task(task)
#     assert "Unsupported task scheme" in str(exc_info.value)


# def test_get_event_with_invalid_format():
#     event = {"InvalidKey": []}
#     with pytest.raises(EventDecodeException):
#         get_event(event)


# def test_get_message_with_invalid_format():
#     record = MagicMock()
#     record.get_message.return_value = {"invalid_key": "value"}
#     with pytest.raises(MessageDecodeException):
#         get_message(record)


# from pydantic import ValidationError

# def test_sqs_message_validation_fails():
#     with pytest.raises(ValidationError):
#         SQSMessage(
#             body="test_body",
#             content_encoding="utf-8",
#             content_type="application/json",
#             headers={"invalid_header": "value"},
#             properties={},
#         )


# # @patch("celery_cloud.runners.aws_lambda_runner.TaskModel")
# # @patch("celery_cloud.runners.aws_lambda_runner.get_event")
# # @patch("celery_cloud.runners.aws_lambda_runner.get_message")
# # @patch("celery_cloud.runners.aws_lambda_runner.get_task")
# # @patch("celery_cloud.runners.aws_lambda_runner.call_task")
# # @patch("celery_cloud.runners.aws_lambda_runner.settings")
# # def test_lambda_handler_with_unsupported_task(
# #     mock_settings,
# #     mock_call_task,
# #     mock_get_task,
# #     mock_get_message,
# #     mock_get_event,
# #     mock_task_model,
# # ):
# #     mock_settings.TASKS = {}
# #     mock_get_event.return_value = SQSEvent(Records=[MagicMock()])
# #     mock_get_message.return_value = SQSMessage(
# #         body="test_body",
# #         content_encoding="utf-8",
# #         content_type="application/json",
# #         headers={"id": "1", "task": "unsupported_task", "argsrepr": "[]", "kwargsrepr": "{}"},
# #         properties={},
# #     )
# #     mock_get_task.return_value = Task(id="1", task="unsupported_task", args=[], kwargs={})

# #     event = {"Records": []}
# #     context = MagicMock()
# #     result = lambda_handler(event, context)

# #     assert result["status"] == "completed"
# #     assert result["processed_messages"] == 0
# #     assert result["failed_messages"] == 1


# # @patch("celery_cloud.runners.aws_lambda_runner.TaskModel")
# # @patch("celery_cloud.runners.aws_lambda_runner.get_event")
# # @patch("celery_cloud.runners.aws_lambda_runner.get_message")
# # @patch("celery_cloud.runners.aws_lambda_runner.get_task")
# # @patch("celery_cloud.runners.aws_lambda_runner.call_task")
# # @patch("celery_cloud.runners.aws_lambda_runner.settings")
# # def test_lambda_handler_with_exception(
# #     mock_settings,
# #     mock_call_task,
# #     mock_get_task,
# #     mock_get_message,
# #     mock_get_event,
# #     mock_task_model,
# # ):
# #     mock_settings.TASKS = {"test_task": "task:my_module.my_function"}
# #     mock_get_event.return_value = SQSEvent(Records=[MagicMock()])
# #     mock_get_message.return_value = SQSMessage(
# #         body="test_body",
# #         content_encoding="utf-8",
# #         content_type="application/json",
# #         headers={"id": "1", "task": "test_task", "argsrepr": "[]", "kwargsrepr": "{}"},
# #         properties={},
# #     )
# #     mock_get_task.return_value = Task(id="1", task="test_task", args=[], kwargs={})
# #     mock_call_task.side_effect = TaskExecutionException("Task execution failed")

# #     event = {"Records": []}
# #     context = MagicMock()
# #     result = lambda_handler(event, context)

# #     assert result["status"] == "completed"
# #     assert result["processed_messages"] == 0
# #     assert result["failed_messages"] == 1
