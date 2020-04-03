import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id} browser: {browser_path}')

redirect_url = ngrok.connect(port, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)

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
        cid = to_channel=c["id"]
stop = False
while not stop:
    message = input("Enter message: ")
    print(client.chat_messages.post(to_channel=cid, message=message))
    if message == "stop":
        stop = True 