import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

def create_channel(client):
    channel_name = input("Enter channel name: ")
    number_members = 0
    members = []
    while number_members < 5:
        member = input("Type stop to stop adding members. Enter member email: ")
        if member == "stop":
            break

        members.append({'email' : member})
    
    client.chat_channels.create(name=channel_name, type=1, members=members)
    print("Channel created!")

def list_channels(client):
    channels = json.loads(client.chat_channels.list().content)["channels"]
    print(channels)

def get_channel(client):
    channel_id = input("Enter channel id: ")
    response = client.chat_channels.get(channel_id = channel_id)
    channel = json.loads(client.chat_channels.get(channel_id = channel_id).content)
    print(channel)

parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id} secret: {client_secret} browser: {browser_path}')

redirect_url = ngrok.connect(port, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)

user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
print ('---')


stop = False
while not stop:
    command = input("Enter action: ")
    if command == "stop":
        stop = True 
    elif command == "create channel":
        create_channel(client)
    elif command == "list channels":
        list_channels(client)
    elif command == "get channel":
        get_channel(client)
    else:
        print("Invalid command.")



        

          