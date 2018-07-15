import os
import pytest
import json
import httpretty

import requests

import runalytics.helpers

#class TestGetUserTokens(object):
#    """Tests for get_user_tokens helper method"""

SERVER_ADDRESS = os.environ.get('JUSTLETIC_SERVER_ADDRESS')
ADMIN_TOKEN = os.environ.get('JUSTLETIC_ADMIN_TOKEN')

USER_LIST = [{"id": 1,"username": "edith@mailinator.com"},
    {"id": 2,"username": "joe@mailinator.com"},
    {"id": 3,"username": "admin"}]
TOKEN_LIST = [{"user_id": 1,"key": "173ce3ae65b1afbd5df6d16e564a085755d2f9d2"},
    {"user_id": 2,"key": "52ad621f36ca868405b3c3afece8da650dca34d5"},
    {"user_id": 3,"key": "5935e11788b40f18f95cc7c70ddb876a3ff3bf41"}]

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

def test_sends_get_request_to_user_and_token_api_endpoints(
    enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list):
    runalytics.helpers.get_user_tokens()
    assert len(httpretty.HTTPretty.latest_requests) == 2
    req = httpretty.HTTPretty.latest_requests[-2]
    requested_url = req.headers.get('Host') + req.path
    assert requested_url == f"{SERVER_ADDRESS}/API/user/"
    req = httpretty.HTTPretty.latest_requests[-1]
    requested_url = req.headers.get('Host') + req.path
    assert requested_url == f"{SERVER_ADDRESS}/API/token/"

def test_includes_admin_token_in_request_headers(
    enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list):
    runalytics.helpers.get_user_tokens()
    assert len(httpretty.HTTPretty.latest_requests) == 2
    req = httpretty.HTTPretty.latest_requests[-2]
    auth_header_sent = req.headers.get('Authorization')
    assert auth_header_sent == f"Token {ADMIN_TOKEN}"
    req = httpretty.HTTPretty.latest_requests[-1]
    auth_header_sent = req.headers.get('Authorization')
    assert auth_header_sent == f"Token {ADMIN_TOKEN}"

def test_returns_list_of_users_with_tokens(
    enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list):
    list_returned = runalytics.helpers.get_user_tokens()
    assert len(list_returned) == len(USER_LIST)
    expected_list = []
    for i, user in enumerate(USER_LIST):
        dictionary = {
            "id": user.get("id"),
            "token": TOKEN_LIST[i].get("key")
        }
        expected_list.append(dictionary)
    assert list_returned == expected_list
