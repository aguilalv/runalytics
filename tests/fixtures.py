import os
import pytest
import httpretty
import json

SERVER_ADDRESS = os.environ.get('JUSTLETIC_SERVER_ADDRESS')

USER_LIST = {"users":[  
    {"id": 1,"username": "edith@mailinator.com"},
    {"id": 2,"username": "joe@mailinator.com"},
    {"id": 3,"username": "admin"}]}
TOKEN_LIST = {"tokens":[
    {"user_id": 1,"key": "173ce3ae65b1afbd5df6d16e564a085755d2f9d2"},
    {"user_id": 2,"key": "52ad621f36ca868405b3c3afece8da650dca34d5"},
    {"user_id": 3,"key": "5935e11788b40f18f95cc7c70ddb876a3ff3bf41"}]}
KEYS_LIST = [
    {
        "token": "4b177fb1430b99d30a4966e01f5582f34170e912",
        "refresh_token": "",
        "strava_id": "21400992",
        "service": "STR",
    },
    {
        "token": "BQDWX3kOs-CZz4BUqssV65aiJ36P7ZjbKa3cb86Q1SDuZG0BWGFvVWL2vJl1lKv54kqAdvBDNWjQ7xEGqVMbGH2E_B_y6iSczqe2FWWaoUE4Ebj3fefREMwH_Bd0aMkmJvV5RhbpFSDq4AXyV0-R_Ks69hxDcZsy",
        "refresh_token": "AQCf7Jg1ddgJ9ufplrx51D5cw7di69EmQQx9eo3dSCObPa9hOToHIqDVoOw675gj9Oo9BudIJtE7-iRmFGO8EiWxmoDZOFdtkEERXCVbVzCvwI25Dz1N2RuYqz28LPzOanQ",
        "strava_id": "",
        "service": "SPO",
    },
]

STRAVA_ACTIVITIES = [
    {"id" : 123456778928065,
        "athlete" : {
            "id" : 12343545645788,
            "resource_state" : 1
        },
    "name" : "Chill Day",
    "distance" : 0,
    "moving_time" : 18373,
    "elapsed_time" : 18373,
    "total_elevation_gain" : 0,
    "type" : "Ride",
    "start_date" : "2018-02-20T18:02:13Z",
    "start_date_local" : "2018-02-20T10:02:13Z",
    },
    {"id" : 111111111111111,
        "athlete" : {
            "id" : 12343545645788,
            "resource_state" : 1
        },
    "name" : "Chill Day",
    "distance" : 0,
    "moving_time" : 18000,
    "elapsed_time" : 18000,
    "total_elevation_gain" : 10,
    "type" : "Run",
    "start_date" : "2018-02-19T18:02:13Z",
    "start_date_local" : "2018-02-19T10:02:13Z",
    },
]

STRAVA_STREAMS = {
    "time":{
        "data":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        "series_type":"distance",
        "original_size":16,
        "resolution":"high"
    },
    "distance":{
        "data":[0.0,0.5,1.6,3.4,5.7,7.9,10.0,12.3,14.4,16.5,18.5,19.7,21.1,22.6,24.5,27.1],
        "series_type":"distance",
        "original_size":16,
        "resolution":"high"
    },
    "altitude":{
        "data":[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "heartrate":{
        "data":[100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "cadence":{
        "data":[155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "latlng":{
        "data":[[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],[11,11],[12,12],[13,13],[14,14],[15,15]],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "velocity_smooth":{
        "data":[1.1,2.1,3.1,4.1,5.1,6.1,7.1,8.1,9.1,10.1,11.1,12.1,13.1,14.1,15.1,16.1],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "watts":{
        "data":[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "temp":{
        "data":[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "moving":{
        "data":[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
    "grade_smooth":{
        "data":[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
        "series_type":"time",
        "original_size":16,
        "resolution":"high"
    },
}

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
def set_get_key_to_ok_data():
    httpretty.register_uri(
        httpretty.GET,
        f"http://{SERVER_ADDRESS}/API/key/",
        body = json.dumps(KEYS_LIST)
    )

@pytest.fixture
def set_get_key_to_return_401_error():
    httpretty.register_uri(
        httpretty.GET,
        f"http://{SERVER_ADDRESS}/API/key/",
        body = '"detail": "Authentication credentials were not provided."',
        status = 401
    )

@pytest.fixture
def set_strava_activities_ok_data():
    httpretty.register_uri(
        httpretty.GET,
        f'https://www.strava.com/api/v3/activities/',
        body= json.dumps(STRAVA_ACTIVITIES)
    )

@pytest.fixture
def set_strava_activities_to_return_404_error():
    httpretty.register_uri(
        httpretty.GET,
        f'https://www.strava.com/api/v3/activities/',
        body = '"xxx": "xxx"',
        status = 404
    )

@pytest.fixture
def set_strava_streams_ok_data():
    for act in STRAVA_ACTIVITIES:
        httpretty.register_uri(
            httpretty.GET,
            f'https://www.strava.com/api/v3/activities/{act.get("id")}/streams',
            body = json.dumps(STRAVA_STREAMS)
        )
