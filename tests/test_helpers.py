import os
import pytest
import json
import httpretty
#from unittest.mock import patch, call, Mock, PropertyMock
import pandas as pd
import numpy as np

from .fixtures import enable_httpretty, set_get_user_to_return_valid_users, set_get_token_to_return_token_list,set_get_key_to_ok_data, set_get_token_to_return_401_error, set_get_key_to_return_401_error,set_strava_activities_ok_data, set_strava_activities_to_return_404_error, set_strava_streams_ok_data
from .fixtures import USER_LIST, TOKEN_LIST, STRAVA_KEY_SINGLE, STRAVA_ACTIVITIES, STRAVA_STREAMS
import runalytics.helpers

SERVER_ADDRESS = os.environ.get('JUSTLETIC_SERVER_ADDRESS')
ADMIN_TOKEN = os.environ.get('JUSTLETIC_ADMIN_TOKEN')

class TestGetJustleticToken(object):
    """Tests for get_jusetltic_token helper method"""

    def test_sends_get_request_to_token_api_endpoint(
        self,enable_httpretty,set_get_token_to_return_token_list):
        ret_token = runalytics.helpers.get_justletic_token(TOKEN_LIST[2].get('user_id'))
        req = httpretty.HTTPretty.latest_requests[-1]
        requested_url = req.headers.get('Host') + req.path
        assert requested_url == f"{SERVER_ADDRESS}/API/token/"

    def test_includes_admin_token_in_request_header(
        self,enable_httpretty,set_get_token_to_return_token_list):
        ret_token = runalytics.helpers.get_justletic_token(TOKEN_LIST[2].get('user_id'))
        req = httpretty.HTTPretty.latest_requests[-1]
        auth_header_sent = req.headers.get('Authorization')
        assert auth_header_sent == f"Token {ADMIN_TOKEN}"

    def test_returns_justletic_token_for_requested_user(
        self,enable_httpretty,set_get_token_to_return_token_list):
        ret_token = runalytics.helpers.get_justletic_token(TOKEN_LIST[2].get('user_id'))
        assert ret_token == TOKEN_LIST[2].get('key')

    def test_raise_exception_if_user_doesnt_exit(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data):
        with pytest.raises(StopIteration):
            ret_token = runalytics.helpers.get_justletic_token(999)

    def test_raise_exception_if_request_fails(self,enable_httpretty,set_get_token_to_return_401_error):
        with pytest.raises(Exception):
            ret_token = runalytics.helpers.get_justletic_token(TOKEN_LIST[2].get('user_id'))


class TestGetStravaKey(object):
    """Tests for get_strava_key helper method"""
    
    def test_sends_get_request_to_strava_endpoint(
        self,enable_httpretty,set_get_key_to_ok_data):
        ret_key = runalytics.helpers.get_strava_key(2)
        req = httpretty.HTTPretty.latest_requests[-1]
        requested_url = req.headers.get('Host') + req.path
        assert requested_url == f"{SERVER_ADDRESS}/API/key/"

    def test_includes_user_token_in_request_header(
        self,enable_httpretty,set_get_key_to_ok_data):
        ret_key = runalytics.helpers.get_strava_key("2")
        req = httpretty.HTTPretty.latest_requests[-1]
        auth_header_sent = req.headers.get('Authorization')
        assert auth_header_sent == "Token 2"
    
    def test_raise_exception_if_request_fails(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_return_401_error):
        with pytest.raises(Exception):
            ret_key = runalytics.helpers.get_strava_key(2)

class TestJustleticUserInit(object):
    """Tests for Init method of user class"""

    def test_stores_user_id(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data):
        user = runalytics.helpers.JustleticUser(2)
        assert user.id == 2

    def test_stores_user_token(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        assert user.justletic_token == TOKEN_LIST[2].get('key') 

    def test_stores_strava_key(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        assert user.strava_key == STRAVA_KEY_SINGLE.get('token')

    def test_stores_activities__as_dataframe(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        assert type(user.activities) == pd.DataFrame 
 
    def test_stores_activities_dataframe_stores_id_and_date(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        assert user.activities.shape == (len(STRAVA_ACTIVITIES),2)
        assert user.activities['id'].values.tolist() == [x.get('id') for x in STRAVA_ACTIVITIES]
        assert user.activities['start_date'].values.tolist() == [x.get('start_date') for x in STRAVA_ACTIVITIES]

    def test_raises_exception_if_user_does_not_exist(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data):
        with pytest.raises(IndexError):
            user = runalytics.helpers.JustleticUser(999)

    def test_raise_exception_if_key_request_fails(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_return_401_error):
        with pytest.raises(Exception):
            user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))

    def test_raise_exception_if_token_request_fails(self,enable_httpretty,set_get_token_to_return_401_error):
        with pytest.raises(Exception):
            user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))

    def test_raise_exception_if_activities_request_fails(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_to_return_404_error):
        with pytest.raises(Exception):
            user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))

    def test_stores_user_id(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data):
        user = runalytics.helpers.JustleticUser(2)
        assert user.id == 2

class TestGetActivity(object):
    """Tests for activity method of user class"""

    def test_sends_get_request_to_strava(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        req = httpretty.HTTPretty.latest_requests[-1]
        requested_url = req.headers.get('Host') + req.path
        assert f"www.strava.com/api/v3/activities/{STRAVA_ACTIVITIES[1].get('id')}/streams" in requested_url

    def test_key_by_type_true_in_query(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        req = httpretty.HTTPretty.latest_requests[-1]
        request_payload = req.querystring
        assert 'key_by_type' in request_payload.keys()
        assert request_payload.get('key_by_type')[0] == "true"
    
    def test_keys_in_query(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        req = httpretty.HTTPretty.latest_requests[-1]
        request_payload = req.querystring
        assert 'keys' in request_payload.keys()
        for key in STRAVA_STREAMS.keys():
            assert key in request_payload.get('keys')[0]

    def test_returns_pandas_dataframe(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        assert type(returned_activity) is pd.DataFrame

    def test_returned_dataframe_has_expected_columns(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        for key in STRAVA_STREAMS.keys():
            assert key in returned_activity.columns

    def test_returned_dataframe_has_expected_number_of_rows(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        for key in STRAVA_STREAMS.keys():
            assert returned_activity.shape[0] == len(STRAVA_STREAMS[key]['data'])
    
    def test_returned_dataframe_includes_all_strava_data(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        for key in STRAVA_STREAMS.keys():
            l1 = returned_activity[key].values.tolist()
            l2 = STRAVA_STREAMS[key]['data']
            assert l1 == l2
    
    def test_returned_dataframe_includes_activity_id(self,enable_httpretty,set_get_token_to_return_token_list,set_get_key_to_ok_data,set_strava_activities_ok_data, set_strava_streams_ok_data):
        user = runalytics.helpers.JustleticUser(TOKEN_LIST[2].get('user_id'))
        returned_activity = user.activity(-1)
        expected_series = pd.Series(
            np.repeat(STRAVA_ACTIVITIES[-1].get('id'),len(STRAVA_STREAMS['time']['data']))
        )
        assert returned_activity['id'].values.tolist() == expected_series.values.tolist()
