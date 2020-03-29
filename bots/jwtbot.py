import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import JWTZoomClient

import json
from configparser import ConfigParser

parser = ConfigParser()
parser.read("bots/bot.ini")
api_key = parser.get("JWT", "api_key")
api_secret = parser.get("JWT", "api_secret")
print(f'id: {api_key} secret: {api_secret}')

client = JWTZoomClient(api_key, api_secret)

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(user_id=user_id).content))

print ('---')

meetings_list = client.meeting.list(user_id='diva@metaverseink.com')
print(json.loads(meetings_list.content))
