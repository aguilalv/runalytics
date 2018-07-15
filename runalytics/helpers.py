import os
import requests
import json

SERVER_ADDRESS = os.environ.get("JUSTLETIC_SERVER_ADDRESS")
ADMIN_TOKEN = os.environ.get("JUSTLETIC_ADMIN_TOKEN")

def get_user_tokens():
    headers = {'Authorization': 'Token ' + ADMIN_TOKEN}
    response = requests.get(f"http://{SERVER_ADDRESS}/API/user/", headers=headers)
    user_list = json.loads(response.text)
    response = requests.get(f"http://{SERVER_ADDRESS}/API/token/", headers=headers)
    token_list = json.loads(response.text)
    
    return_list = []
    for user in user_list:
        token = next(x.get('key') for x in token_list if x.get('user_id')==user.get('id'))
        dictionary = {'id': user.get('id'),'token':token}        
        return_list.append(dictionary)
    return return_list

