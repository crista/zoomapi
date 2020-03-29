import json
from zoomapi import OAuthZoomClient
from Config import ConfigParser
from pyngrok import ngrok

parser = ConfigParser()
parser.read("bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")

redirect_url = ngrok.connect(4000, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, redirect_url)

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(user_id=user_id).content))

print ('---')

meetings_list = client.meeting.list(user_id='diva@metaverseink.com')
print(json.loads(meetings_list.content))
