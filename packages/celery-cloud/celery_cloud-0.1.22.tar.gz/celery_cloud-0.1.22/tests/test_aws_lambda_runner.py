import pytest
from unittest.mock import patch, MagicMock
from celery_cloud.runners.aws_lambda import (
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
