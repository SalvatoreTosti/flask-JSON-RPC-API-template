from app import app, db
import pytest
import json
from hypothesis import given
import hypothesis.strategies as st


import os
import tempfile
import test.setup as setup
import uuid
import datetime

TEST_DB = "test.db"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DEBUG"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), TEST_DB
    )

    assert not app.debug

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            setup.run()
        yield client


def JSONRPCRequest(method, params=None):
    return {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": params,
    }


def valid_task_create_payload(user_id):
    return st.fixed_dictionaries(
        {
            "user_id": st.just(user_id),
            "title": st.text(),
            "description": st.text(),
            "due_time": st.just(datetime.datetime.now().isoformat() + "Z"),
        }
    )


def valid_task_update_payload(user_id, target_id):
    return st.fixed_dictionaries(
        {
            "target_id": st.just(target_id),
            "user_id": st.just(user_id),
            "title": st.text(),
            "description": st.text(),
            "due_time": st.just(datetime.datetime.now().isoformat() + "Z"),
            "completion_time": st.just(datetime.datetime.now().isoformat() + "Z"),
        }
    )


def test_index(client):
    response = client.get("/", follow_redirects=True)
    assert 200 == response.status_code


def test_404(client):
    response = client.get("/404", follow_redirects=True)
    assert 404 == response.status_code


@given(st.data())
def test_create(client, data):
    request_params = data.draw(valid_task_create_payload(1))
    request_payload = JSONRPCRequest("task.create", request_params)

    response = client.post("/rpc", json=request_payload)
    assert 200 == response.status_code
    result_payload = response.json["result"]
    assert request_params["user_id"] == result_payload["user_id"]
    assert request_params["title"] == result_payload["title"]
    assert request_params["description"] == result_payload["description"]


@given(st.data())
def test_read(client, data):
    request_params = data.draw(valid_task_create_payload(1))
    request_payload = JSONRPCRequest("task.create", request_params)

    response = client.post("/rpc", json=request_payload)
    assert 200 == response.status_code
    result_payload = response.json["result"]
    assert request_params["user_id"] == result_payload["user_id"]
    assert request_params["title"] == result_payload["title"]
    assert request_params["description"] == result_payload["description"]
    assert request_params["due_time"] == result_payload["due_time"]
    assert not result_payload["completion_time"]

    target_id = result_payload["id"]

    request_payload = JSONRPCRequest("task.read", {"target_id": target_id})
    response = client.post("/rpc", json=request_payload)
    assert 200 == response.status_code
    result_payload = response.json["result"]
    assert target_id == result_payload["id"]
    assert request_params["user_id"] == result_payload["user_id"]
    assert request_params["title"] == result_payload["title"]
    assert request_params["description"] == result_payload["description"]
    assert request_params["due_time"] == result_payload["due_time"]
    assert not result_payload["completion_time"]


@given(st.data())
def test_read_all(client, data):
    request_params = data.draw(valid_task_create_payload(1))
    request_payload = JSONRPCRequest("task.create", request_params)

    response = client.post("/rpc", json=request_payload)
    assert 200 == response.status_code
    result_payload = response.json["result"]
    assert request_params["user_id"] == result_payload["user_id"]
    assert request_params["title"] == result_payload["title"]
    assert request_params["description"] == result_payload["description"]
    target_id = result_payload["id"]

    request_payload = JSONRPCRequest("task.read_all")
    response = client.post("/rpc", json=request_payload)
    assert 200 == response.status_code
    result_payload = response.json["result"]


@given(st.data())
def test_update(client, data):
    request_params = data.draw(valid_task_create_payload(1))
    request_payload = JSONRPCRequest("task.create", request_params)

    response = client.post("/rpc", json=request_payload)
    assert 200 == response.status_code
    result_payload = response.json["result"]
    assert request_params["user_id"] == result_payload["user_id"]
    assert request_params["title"] == result_payload["title"]
    assert request_params["description"] == result_payload["description"]
    target_id = result_payload["id"]

    request_params = data.draw(valid_task_update_payload(1, target_id=target_id))
    request_payload = JSONRPCRequest("task.update", request_params)

    response = client.post("/rpc", json=request_payload)
    assert 200 == response.status_code
    result_payload = response.json["result"]
    assert request_params["user_id"] == result_payload["user_id"]
    assert request_params["title"] == result_payload["title"]
    assert request_params["description"] == result_payload["description"]
    assert request_params["due_time"] == result_payload["due_time"]
    assert request_params["completion_time"] == result_payload["completion_time"]

    assert target_id == result_payload["id"]
