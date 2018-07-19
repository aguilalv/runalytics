import os
import requests
import json

SERVER_ADDRESS = os.environ.get("JUSTLETIC_SERVER_ADDRESS")
ADMIN_TOKEN = os.environ.get("JUSTLETIC_ADMIN_TOKEN")

def get_justletic_token(user_id):
    headers = {'Authorization': 'Token ' + ADMIN_TOKEN}
    response = requests.get(f"http://{SERVER_ADDRESS}/API/token/", headers=headers)
    if response.status_code != 200:
        return None
    token_list = json.loads(response.text)
    return next(x.get('key') for x in token_list if x.get('user_id') == user_id)

def get_strava_key(justletic_token):
    headers = {'Authorization': f'Token {justletic_token}'}
    response = requests.get(f"http://{SERVER_ADDRESS}/API/key/", headers=headers)
    if response.status_code != 200:
        return None
    received_data = json.loads(response.text)
    return received_data.get('token')

class JustleticUser(object):

    def __init__(self,user_id):
        self.id = user_id
        try:
            self.justletic_token = get_justletic_token(user_id)
        except StopIteration:
            raise IndexError()
        self.strava_key = get_strava_key(self.justletic_token)

#def get_user_activities(user_id):
#        user_tokens = get_user_tokens()
#        token = next(x.get('token') for x in user_tokens if x.get('id')==user_id)
#        
#        headers = {'Authorization': 'Token ' + token}
#        response = requests.get(f"http://{SERVER_ADDRESS}/API/key/", headers=headers)
#
#        credentials = json.loads(response.text)
#
#        print(f'<<<< {credentials.get["token"]} // {credentials.get["strava_id"]}')
    

