from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os
import sys
import csv
import traceback
import random
import time

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

def banner():
    os.system('clear')
    print(f"""
    {re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
    {re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
    {re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

                   Version: 1.01
     {re}Subscribe Termux Professor on Youtube
       {cy}www.youtube.com/c/TermuxProfessorYT
    """)

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re + "[!] Run 'python3 setup.py' first!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))

users = []
with open(r"members.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print(gr + 'Choose a group to add members:')
i = 0
for group in groups:
    print(str(i) + ' - ' + group.title)
    i += 1

g_index = input(gr + "Enter a Number: " + re)
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input(gr + "Enter 1 to add by username or 2 to add by ID: " + cy))

N = 0  # Counter for added members
SLEEP_INTERVAL = 60  # Time to sleep between adding members (in seconds)

for user in users:
    N += 1
    if N % 300 == 0:
        print(f"Waiting for {SLEEP_INTERVAL} seconds...")
        time.sleep(SLEEP_INTERVAL)

    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting for 60-180 Seconds...")
        time.sleep(random.randrange(60, 180))
    except PeerFloodError as e:
        print(f"Flood error: {e}, waiting for {SLEEP_INTERVAL} seconds...")
        time.sleep(SLEEP_INTERVAL)
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
        print("Waiting for 5 Seconds...")
        time.sleep(random.randrange(0, 5))
    except Exception as e:
        traceback.print_exc()
        print(f"Unexpected Error: {str(e)}")
        continue
