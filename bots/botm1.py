import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

def create_channel(client):
    channel_name = input("Enter channel name: ")
    print("Available channel types: 1 - private, 2 - private with members that belong with the same Zoom account, 3 - public")
    channel_type = int(input("Enter channel type: "))

    if (channel_type < 1 and channel_type > 3):
        print("Invalid channel type. Returning to menu.")
        return

    number_members = 0
    members = []
    while number_members < 5:
        member = input("Type stop to stop adding members. Enter member email: ")
        if member == "stop":
            break

        members.append({'email' : member})
    
    if (client.chat_channels.create(name=channel_name, type=channel_type, members=members).status_code == 201):
        print("Channel created!")

def list_channels(client):
    channels = json.loads(client.chat_channels.list().content)["channels"]
    print(channels)

def get_channel(client):
    channel_id = input("Enter channel id: ")
    channel = json.loads(client.chat_channels.get(channel_id = channel_id).content)
    print(channel)

def list_channel_members(client):
    channel_id = input("Enter channel id: ")
    response = client.chat_channels.list_members(channel_id = channel_id)
    if (response.status_code == 200):
        print(json.loads(response.content)["members"])
    else:
        print("Incorrect channel id")
        
def delete_channel(client):
    channel_id = input("Enter channel id: ")
    if ((client.chat_channels.delete(channel_id = channel_id)).status_code == 204):
        print("Channel deleted")
    else:
        print("Error deleting channel")

def update_channel(client):
    channel_id = input("Enter channel id: ")
    channel_name = input("Enter channel name: ")
    if (client.chat_channels.update(channel_id = channel_id, name = channel_name).status_code == 204):
        print("Channel updated!")
    else:
        print("Error updating channel")

def invite_channel_members(client):
    channel_id = input("Enter channel id: ")
    number_members = 0
    members = []
    while number_members < 5:
        member = input("Type stop to stop adding members. Enter member email: ")
        if member == "stop":
            break

        members.append({'email' : member})
    
    if (client.chat_channels.invite_members(channel_id = channel_id, members=members).status_code == 200):
        print("Invitations sent!")
    else:
        print("Invalid action. Check if channel exists or if users are already members of the channel.")
    
def remove_channel_member(client):
    channel_id = input("Enter channel id: ")
    member_id = input("Enter member id: ")
    if (client.chat_channels.remove_member(channel_id = channel_id, member_id = member_id).status_code == 204):
        print("Member removed!")
    else:
        print("Error removing member")

def list_messages(client, user_id):
    response = input("Retrieve messages by email or channel? ")
    if response == "email":
        email = input("Please enter email: ")
        messages = json.loads(client.chat_messages.list(user_id = user_id, to_contact = email).content)["messages"]
    elif response == "channel":
        channel = input("Please enter channel id: ")
        messages = json.loads(client.chat_messages.list(user_id = user_id, to_channel = channel).content)["messages"]
    else:
        print("Invalid entry")
    print(messages)

def send_message(client):
    email = input("Please enter email of the contact you'd like to send a message: ")
    message = input("Enter message: ")
    print(client.chat_messages.post(to_contact = email, message=message)) 

user_id = "me"
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
    elif command == "list channel members":
        list_channel_members(client)
    elif command == "delete channel":
        delete_channel(client)
    elif command == "update channel":
        update_channel(client)
    elif command == "invite channel members":
        invite_channel_members(client)
    elif command == "remove channel member":
        remove_channel_member(client)
    elif command == "list messages":
        list_messages(client, user_id)
    elif command == "send message":
        send_message(client)
    else:
        print("Invalid command.")      