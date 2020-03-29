import json
from zoomapi import JWTZoomClient

client = JWTZoomClient('AWGqDsi4SJOuZBTKNkR8Xw', 'RrEybd7htBLyJ7IFzfDGUbCfOY9fkY0VGc9d')

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(user_id=user_id).content))

print ('---')

meetings_list = client.meeting.list(user_id='diva@metaverseink.com')
print(json.loads(meetings_list.content))
