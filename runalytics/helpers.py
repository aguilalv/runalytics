import os
import requests
import json
import pandas as pd

SERVER_ADDRESS = os.environ.get("JUSTLETIC_SERVER_ADDRESS")
ADMIN_TOKEN = os.environ.get("JUSTLETIC_ADMIN_TOKEN")

def get_justletic_token(user_id):
    headers = {'Authorization': 'Token ' + ADMIN_TOKEN}
    response = requests.get(f"http://{SERVER_ADDRESS}/API/token/", headers=headers)
    if response.status_code != 200:
        raise Exception()
    token_list = json.loads(response.text).get("tokens")
    return next(x.get('key') for x in token_list if x.get('user_id') == user_id)

def get_strava_key(justletic_token):
    headers = {'Authorization': f'Token {justletic_token}'}
    response = requests.get(f"http://{SERVER_ADDRESS}/API/key/", headers=headers)
    if response.status_code != 200:
        raise Exception()
    received_data = json.loads(response.text)
    return next(x.get('token') for x in received_data if x.get('service') == 'STR')

class JustleticUser(object):

    activities = []

    def __init__(self,user_id):
        self.id = user_id
        try:
            self.justletic_token = get_justletic_token(user_id)
        except StopIteration:
            raise IndexError()
        self.strava_key = get_strava_key(self.justletic_token)
        self._update_activities()
         
    def _update_activities(self):
        headers = {'Authorization': f'Bearer {self.strava_key}'}
        response = requests.get(f"https://www.strava.com/api/v3/activities/", headers=headers)
        if response.status_code != 200:
            raise Exception() 
        received_data = json.loads(response.text)
        aux_df = pd.DataFrame(received_data)
        self.activities = aux_df[['id','start_date']].set_index('id').sort_values(by='start_date',ascending=False)

    def activity(self,index):
        activity_id = self.activities.index[index]        
        headers = {'Authorization': f'Bearer {self.strava_key}'}
        payload = {
            'key_by_type': 'true', 
            'keys': 'time,distance,altitude,heartrate,cadence,latlng,velocity_smooth,watts,temp,moving,grade_smooth'
        }
        response = requests.get(f"https://www.strava.com/api/v3/activities/{activity_id}/streams", headers=headers, params = payload)
        received_dict = json.loads(response.text)
        aux_dict = {'id':activity_id}


        for key in received_dict:
            aux_dict[key] = received_dict.get(key).get('data')
        ret_activity = pd.DataFrame(aux_dict)
        ret_activity['lat'] = ret_activity['latlng'].str[0]
        ret_activity['long'] = ret_activity['latlng'].str[1]
        ret_activity = ret_activity.drop(columns=['latlng'])
        return ret_activity
