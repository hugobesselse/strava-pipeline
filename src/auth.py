import os
import requests
from dotenv import load_dotenv

load_dotenv()

Client_ID = os.getenv("strava_client_id")
Client_Secret = os.getenv("strava_client_secret")
Redirect_Uri = os.getenv("strava_redirect_uri")

def get_authorization_url():
    url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={Client_ID}"
        f"&response_type=code"
        f"&redirect_uri={Redirect_Uri}"
        # Strava requires approval_promt=force to retrieve refresh token each time
        f"&approval_prompt=force"
        # Strava requires scope definition. Read_all is for private activities, read is for public activities. 
        f"&scope=activity:read_all"
    )
    return url

def exchange_code_for_token(code):
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": Client_ID,
            "client_secret": Client_Secret,
            "code": code,
            # Authorization code for first exchange, replaced by refresh_token afterwards. 
            "grant_type":"authorization_code"
        },
    )
    tokens = response.json()
    return tokens

if __name__ == "__main__":
    print("Step 1: open URL in the browser and authorize:")
    print(get_authorization_url())

    # Strava redirects to localhost URL with single use code for query parameter.
    code = input("\nStep 2: paste the code from the redirect URL:")
    tokens = exchange_code_for_token(code)

    # Strava access tokens expire after 6 hours. Refresh token can be used for a long duration to retrieve new access tokens. 
    print("\nThe tokens:")
    print(f"Access token: {tokens['access_token']}")
    print(f"Refresh token: {tokens['refresh_token']}")
    print(f"Expires at: {tokens['expires_at']}")
