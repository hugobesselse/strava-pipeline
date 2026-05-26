import os
import json
import time
import requests
from config import RAW_DATA_PATH

def load_config():
    return{
        "access_token": os.getenv("STRAVA_ACCESS_TOKEN"),
        "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
        "client_id": os.getenv("STRAVA_CLIENT_ID"),
        "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
        "expires_at": int(os.getenv("STRAVA_TOKEN_EXPIRES_AT")),
    }

def refresh_token_if_needed(config,http_client=requests):
    "Retrieve new access token if prior one expired."

    if time.time() < config["expires_at"]:
        return config["access_token"]
    
    # Token expired, request new token via refresh_token. 
    response = http_client.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "grant_type": "refresh_token",
            "refresh_token": config["refresh_token"],
        },
    )
    tokens = response.json()
    print("Token renewed.")
    return tokens["access_token"]

def get_activities(access_token, page=1, per_page=50, http_client=requests):
    # Retrieve a single page of activities. 
    response = http_client.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"page": page, "per_page": per_page},
    )
    return response.json()

def extract_all_activities(config, http_client=requests):
    # Retrieve all activities as a list. 
    access_token = refresh_token_if_needed(config,http_client=http_client)
    all_activities = []
    page = 1

    print("Full extract: retrieving all activities.")

    while True:
        activities = get_activities(access_token, page=page, http_client=http_client)
        if not activities:
            break
        all_activities.extend(activities)
        print(f"Page {page}: { len(activities)} activities extracted.")
        time.sleep(0.5)
        page +=1

    print(f"Extraction complete: { len(all_activities)} activities retrieved")
    return all_activities

def save_activities(activities, output_path=None):
    # Save activities as timestamped JSON. 
    if output_path is None:
        timestamp = int(time.time())
        output_path = RAW_DATA_PATH / f"activities_{timestamp}.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(activities, f , indent=2)
    
    print(f"Saved {len(activities)} activities to {output_path}.")
    return output_path

if __name__ == "__main__":
    from pathlib import Path
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
    config = load_config()
    activities = extract_all_activities(config)
    save_activities(activities)



