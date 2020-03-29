import json
from zoomapi import OAuthZoomClient
from configparser import ConfigParser
from pyngrok import ngrok

parser = ConfigParser()
parser.read("bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
print(f'id: {client_id} secret: {client_secret}')

redirect_url = ngrok.connect(4000, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, redirect_url)

user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
print ('---')

print(json.loads(client.meeting.list(user_id="me").content))
client.chat_channels.list()
channels = json.loads(client.chat_channels.list().content)["channels"]
print(channels)
for c in channels:
    print(c)
    if "test" in c.values():
        print("Found channel test", c["id"])
        print(client.chat_messages.post(to_channel=c["id"], message="Blah!"))