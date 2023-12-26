import requests
import json
import creds
import datetime
import colorama

from colorama import Fore, Back, Style

from bs4 import BeautifulSoup

from datetime import datetime

# SOFTWARE FUNCTIONS
def GetToken(user, passw):
	login_response = requests.post("https://api.wasteof.money/session", json={"username": user, "password": passw})
	login_dict = login_response.json()
	return(login_dict["token"])

def help():
	print('Available commands:')
	print(f"[post]                  Create a post")
	print(f"[msg <option>]          Show unread messages")
	print(f" - count                Shows count of unread messages")
	print(f" - markread             Marks all unread messages as read")
	print(f"")
	print(f'\n[exit]                Exit the program')


def post(body_text, token):
	json_text = {"post": body_text, "repost": None}
	post_response = requests.post("https://api.wasteof.money/posts", headers={"Authorization": token}, json=json_text)

def markread(ids ,token):
	json_text = {"messages": ids}
	post_response = requests.post("https://api.wasteof.money/messages/mark/read", headers={"Authorization": token}, json=json_text)
	print(post_response)

def GetMessages(token):
	login_response = requests.get("https://api.wasteof.money/messages/unread", headers={"Authorization": token})
	return login_response.json()

def GetMessageCount(token):
	login_response = requests.get("https://api.wasteof.money/messages/count", headers={"Authorization": token})
	return login_response.json()

def dprint(my_dict):
    print(json.dumps(my_dict, indent=2))

def html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    formatted_text = ''

    for tag in soup.recursiveChildGenerator():
        if tag.name == 'p':
            formatted_text += f"{Fore.GREEN}{tag.text}{Style.RESET_ALL}\n"
        elif tag.name == 'b':
            formatted_text += f"{Style.BRIGHT}{Fore.RED}{tag.text}{Style.RESET_ALL}"
        # Add more conditions for other HTML tags as needed
    return formatted_text

# LOGIN
print('Welcome to wasteofCLI!')
username = creds.cre["Username"]
password = creds.cred["Password"]

token = GetToken(username, password)

print('Logged in!\n')

# MAIN PROMPT

prompt_input = ""

while prompt_input != "exit":
	prompt_input = input('>>> ')
	if prompt_input == "help":
		help()

	if prompt_input == "post":
		print('Write your post below')
		post_body = input('')
		post(post_body, token)

	if prompt_input.startswith("msg"):
		if prompt_input == "msg count":
			count = GetMessageCount(token)['count']
			if count > 0:
				print(f"Unread Messages: {Fore.GREEN}{GetMessageCount(token)['count']}{Style.RESET_ALL}")
			if count == 0:
				print(f"Unread Messages: {Fore.RED}{GetMessageCount(token)['count']}{Style.RESET_ALL}")


		elif prompt_input == "msg markread":

			msgOutput = GetMessages(token)
			message_ids = []
			if "unread" in msgOutput:
				for msg in msgOutput["unread"]:
					if "_id" in msg:
						message_ids.append(msg["_id"])
			markread(message_ids, token)

		else:
			msgOutput = GetMessages(token)
			if msgOutput == {'unread': [], 'last': True}:
				print("No new messages!")

			else:
				print(f"Total Messages: {GetMessageCount(token)['count']}")
				print('')
				for msg in msgOutput["unread"]:
					if msg['type'] == "post_mention":
						timestamp_ms = msg["time"]
						formatted_time = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M')

						print(f"  {msg['data']['actor']['name']:<9}[{formatted_time}]")
						print(f"  {html(msg['data']['post']['content'])}")
						print('')
					if msg['type'] == "follow":
						print(f"  New Follower!")
						print(f"  {Fore.YELLOW}{msg['data']['actor']['name']}{Style.RESET_ALL}")
						print('')
