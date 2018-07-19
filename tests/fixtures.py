import os
import pytest
import httpretty
import json

SERVER_ADDRESS = os.environ.get('JUSTLETIC_SERVER_ADDRESS')

USER_LIST = [{"id": 1,"username": "edith@mailinator.com"},
    {"id": 2,"username": "joe@mailinator.com"},
    {"id": 3,"username": "admin"}]
TOKEN_LIST = [{"user_id": 1,"key": "173ce3ae65b1afbd5df6d16e564a085755d2f9d2"},
    {"user_id": 2,"key": "52ad621f36ca868405b3c3afece8da650dca34d5"},
    {"user_id": 3,"key": "5935e11788b40f18f95cc7c70ddb876a3ff3bf41"}]
STRAVA_KEY_SINGLE = {
    "token": "4b177fb1430b99d30a4966e01f5582f34170e912",
    "strava_id": "21400992"}

@pytest.fixture
def enable_httpretty():
    httpretty.enable()
    yield
    httpretty.disable()
    httpretty.reset()

@pytest.fixture
def set_get_user_to_return_valid_users():
    httpretty.register_uri(
        httpretty.GET,
        f"http://{SERVER_ADDRESS}/API/user/",
        body= json.dumps(USER_LIST))

@pytest.fixture
def set_get_token_to_return_token_list():
    httpretty.register_uri(
        httpretty.GET,
        f"http://{SERVER_ADDRESS}/API/token/",
        body= json.dumps(TOKEN_LIST))

@pytest.fixture
def set_get_token_to_return_401_error():
    httpretty.register_uri(
        httpretty.GET,
        f"http://{SERVER_ADDRESS}/API/token/",
        body = '"detail": "Authentication credentials were not provided."',
        status = 401
    )

            
@pytest.fixture
def set_strava_get_stream_to_ok_data():
    httpretty.register_uri(
        httpretty.GET,
        f'https://www.strava.com/api/v3/activities/1/streams',
        body= json.dumps(USER_LIST))

@pytest.fixture
def set_get_key_to_ok_data():
    httpretty.register_uri(
        httpretty.GET,
        f"http://{SERVER_ADDRESS}/API/key/",
        body = json.dumps(STRAVA_KEY_SINGLE)
    )

@pytest.fixture
def set_get_key_to_return_401_error():
    httpretty.register_uri(
        httpretty.GET,
        f"http://{SERVER_ADDRESS}/API/key/",
        body = '"detail": "Authentication credentials were not provided."',
        status = 401
    )
