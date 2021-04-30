"""Watch for a 42 correction slot. Author: tmarx."""

if (__name__ != "__main__"):
    exit(1)

import pync
import time
import requests
import datetime
import pickle

# Time waited between every check, in seconds
WAIT_TIME = 15

def get_params():
    """Get the last params saved on the disk. Return None if no params saved."""
    try:
        with open("./params.pkl", "rb") as file:
            url, team_id, token = pickle.load(file)
            return (url, team_id, token)
    except:
        return (None, None, None)

def save_params(url, team_id, token):
    """Save params on the disk."""
    with open("./params.pkl", "wb+") as file:
        pickle.dump((url, team_id, token), file)

def notify(title, message):
    """Send a desktop notification."""
    pync.notify(message, title=title, contentImage="./logo.png", sound="default")

def get_slots():
    """Send a request to 42 intra."""
    today = datetime.date.today()
    start = today
    end = today + datetime.timedelta(days=days_to_watch)
    print(f"Getting slots from {today} to {end}")
    request = requests.get(
        f"https://projects.intra.42.fr/projects/{project_url}/slots.json?team_id={team_id}&start={today}&end={end}",
        headers={
            "Host": "projects.intra.42.fr",
            "Cookie": f"_intra_42_session_production={token};"
        }
    )
    response = request.json()
    print(response)
    if ("error" in response):
        print("Unable to connect, check the token!")
        exit(0)
    return response


# Check if we previously saved params
previous_url, previous_team_id, previous_token = get_params()

url_placeholder = ""
team_id_placeholder = ""
token_placeholder = ""
if (not previous_url is None):
    url_placeholder = f" (default {previous_url})"
if (not previous_team_id is None):
    team_id_placeholder = f" (default {previous_team_id})"
if (not previous_token is None):
    token_placeholder = f" (default {previous_token})"

# Get variables
print("Refer to ReadMe.md to help you find the following data.")

project_url = input(f"Project URL{url_placeholder}: ")
if (project_url == ""):
    project_url = previous_url

team_id = input(f"Team ID{team_id_placeholder}: ")
if (team_id == ""):
    team_id = previous_team_id

token = input(f"Session token{token_placeholder}: ")
if (token == ""):
    token = previous_token

try:
    days_to_watch = int(input("Number of days you want to watch (default 3): "))
except:
    days_to_watch = 3

save_params(project_url, team_id, token)

notify("Running", "You'll be notified when an open slot is found.")

while True:
    print("Checking...")
    slots = get_slots()
    if (len(slots) > 0):
        print("Slot found.")
        notify("Correction found!", "An open slot has been found.")
    time.sleep(WAIT_TIME)