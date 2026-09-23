from dotenv import load_dotenv
from requests import post, get, Response
import os
import base64
import json

# CONSTANTS
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SEC = os.getenv("SPOTIFY_CLIENT_SECRET")

GET_AUTH_ENDPOINT = "https://accounts.spotify.com/api/token"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"

def check_response_code(response: Response, msg: str) -> dict:
    """Handles response codes from the calls and parses JSON for convenience"""
    if response.status_code == 200:
        return json.loads(response.content)

    print(f"[ERROR]: Got error code {response.status_code} when {msg}")
    print(response.content)
    return {}

def get_token() -> dict:
    """Get authorization token from Spotify API"""
    auth_string = CLIENT_ID + ":" + CLIENT_SEC
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = post(GET_AUTH_ENDPOINT, headers=headers, data=data)

    return check_response_code(response, "trying to generate authorization token.")

def get_auth_header(token: str) -> dict:
    """Function to construct headers for interacting with API"""
    return {"Authorization": "Bearer " + token}

def search_spotify(token: str, search_type: str, search_query: str) -> dict:
    """
    General function for searching something on Spotify
    search_type Domain: {'album', 'artist', 'track'}
    """
    # Get the ID for the required search
    headers = get_auth_header(token)
    cleaned_query = search_query.replace(" ", "%20")

    url = SEARCH_ENDPOINT + f"?q={search_type}%3A{cleaned_query}&type={search_type}&limit=1"
    response = get(url, headers=headers)
    return check_response_code(response, f"trying to search for {search_type}.")

def run():
    """Main function for interacting with Spotify"""
    auth_token_json = get_token()

    if not auth_token_json:
        print("Terminating")
        return

    token = auth_token_json["access_token"]
    print("-----------------------------------------------------")
    print("Drake:")
    print(search_spotify(token, "artist", "Drake"))

    print("\n-----------------------------------------------------")
    print("Hardstone Pyscho:")
    print(search_spotify(token, "album", "Hardstone Psycho"))

    print("\n-----------------------------------------------------")
    print("FWU:")
    print(search_spotify(token, "track", "FWU"))

run()