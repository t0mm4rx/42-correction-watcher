"""Watch for a 42 correction slot. Author: tmarx."""

if (__name__ != "__main__"):
    exit(1)

import pync
import time
import requests
import datetime

# Time waited between every check, in seconds
WAIT_TIME = 30

def notify(title, message):
    """Send a desktop notification."""
    pync.notify(message, title=title, contentImage="./logo.png")

def get_slots():
    """Send a request to 42 intra."""
    today = datetime.date.today()
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


# Get variables
print("Refer to ReadMe.md to help you find the following data.")
project_url = input("Project URL: ")
team_id = input("Team ID: ")
token = input("Session token: ")

try:
    days_to_watch = int(input("Number of days you want to watch (default 3): "))
except:
    days_to_watch = 3

notify("Running", "You'll be notified when an open slot is found.")

while True:
    print("Checking...")
    slots = get_slots()
    if (len(slots) > 0):
        print("Slot found.")
        notify("Correction found!", "An open slot has been found.")
    time.sleep(WAIT_TIME)