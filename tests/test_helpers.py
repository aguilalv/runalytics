import os
import pytest
import json
import httpretty

from .fixtures import enable_httpretty, set_get_user_to_return_valid_users, set_get_token_to_return_token_list,set_strava_get_stream_to_ok_data,set_get_key_to_ok
from .fixtures import USER_LIST, TOKEN_LIST
import runalytics.helpers

SERVER_ADDRESS = os.environ.get('JUSTLETIC_SERVER_ADDRESS')
ADMIN_TOKEN = os.environ.get('JUSTLETIC_ADMIN_TOKEN')

class TestGetJustleticToken(object):
    """Tests for get_jusetltic_token helper method"""

    def test_sends_get_request_to_token_api_endpoint(
        self,enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list):
        ret_token = runalytics.helpers.get_justletic_token(TOKEN_LIST[2].get('user_id'))
        req = httpretty.HTTPretty.latest_requests[-1]
        requested_url = req.headers.get('Host') + req.path
        assert requested_url == f"{SERVER_ADDRESS}/API/token/"

    def test_includes_admin_token_in_request_header(
        self,enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list):
        ret_token = runalytics.helpers.get_justletic_token(TOKEN_LIST[2].get('user_id'))
        req = httpretty.HTTPretty.latest_requests[-1]
        auth_header_sent = req.headers.get('Authorization')
        assert auth_header_sent == f"Token {ADMIN_TOKEN}"

    def test_returns_justletic_token_for_requested_user(
        self,enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list):
        ret_token = runalytics.helpers.get_justletic_token(TOKEN_LIST[2].get('user_id'))
        assert ret_token == TOKEN_LIST[2].get('key')

    def test_returns_none_if_user_doesnt_exist(self): 
        ret_token = runalytics.helpers.get_justletic_token(999)
        assert ret_token == None    
        
class TestJustleticUserInit(object):
    """Tests for Init method of user class"""

    def test_stores_user_id(self,enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list,set_get_key_to_ok):
        user = runalytics.helpers.JustleticUser(2)
        assert user.id == 2

    def test_stores_user_token(self,enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list,set_get_key_to_ok):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        assert user.justletic_token == TOKEN_LIST[2].get('key')

    def test_raises_exception_if_user_does_not_exist(self,enable_httpretty,set_get_user_to_return_valid_users,set_get_token_to_return_token_list,set_get_key_to_ok):
        with pytest.raises(IndexError):
            user = runalytics.helpers.JustleticUser(999)

