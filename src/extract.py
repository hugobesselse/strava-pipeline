import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from config import RAW_DATA_PATH, LAST_EXTRACT_FILE

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

def refresh_token_if_needed():
    "Retrieve new access token if prior one expired."
    expires_at = int(os.getenv("STRAVA_TOKEN_EXPIRES_AT"))

    if time.time() < expires_at:
        return os.getenv("STRAVA_ACCESS_TOKEN")
    
    # Token expired, request new token via refresh_token. 
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": os.getenv("STRAVA_CLIENT_ID"),
            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
            "grant_type": "refresh_token",
            "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
        },
    )
    tokens = response.json()
    print("Token renewed.")
    return tokens["access_token"]

def get_activities(access_token, page=1, per_page=50, after=None):
    "Retrieve a page of activities via Strava API."
    params={"page":page,"per_page":per_page}
    if after:
        params["after"] = after
    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params,
    )
    return response.json()

def extract_all_activities():
    "Retrieve all activities and save them as JSON in data/raw/."
    access_token = refresh_token_if_needed()
    all_activities = []
    page = 1

    if LAST_EXTRACT_FILE.exists():
        with open(LAST_EXTRACT_FILE,"r") as f:
            after = int(f.read().strip())
        print(f"Incremental extract: activities after timestamp {after}")
    else:
        after = None
        print("First extract: retrieve all activities")

    while True:
        activities = get_activities(access_token,page=page, after=after)
        # Strava returns an empty list if there are no more activities. 
        if not activities:
            break

        all_activities.extend(activities)
        print(f"Page {page}: {len(activities)} activities extracted")

        # Strava rate limit: 100 requests per 15 minutes. 
        time.sleep(0.5)
        page += 1
    
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    output_file = RAW_DATA_PATH / "activities.json"

    if output_file.exists():
        with open (output_file,"r") as f:
            existing = json.load(f)
        all_activities = existing + all_activities

    with open(output_file, "w") as f:
        json.dump(all_activities,f,indent=2)

    with open (LAST_EXTRACT_FILE,"w") as f:
        f.write(str(int(time.time())))
    
    print(f"\nFinished! {len(all_activities)} activities saved in {output_file}")

if __name__ == "__main__":
    print("Script started")
    extract_all_activities()
