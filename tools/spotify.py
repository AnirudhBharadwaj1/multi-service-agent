from dotenv import load_dotenv
from requests import post, get, Response
import os
import base64
import json

# CONSTANTS
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SEC = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

TOKEN_URL = "https://accounts.spotify.com/api/token"

GET_AUTH_ENDPOINT = "https://accounts.spotify.com/api/token"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
GET_PLAYLISTS_ENDPOINT = "https://api.spotify.com/v1/me/playlists"
API_BASE = "https://api.spotify.com/v1"

# CONNECTION FUNCTIONS
def check_response_code(response: Response, msg: str) -> dict:
    """Handles response codes from the calls and parses JSON for convenience"""
    if response.status_code == 200:
        try:
            return json.loads(response.content)

        except Exception as e:
            print(f"[ERROR]: Cannot parse JSON output: {e}")
            print(response.content)

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

def get_access_token() -> str:
    """Exchange saved refresh_token for a new user access_token"""
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SEC
    }

    response = post(TOKEN_URL, data=data)
    return check_response_code(response, "trying to generate access token.")

def get_user_id(access_token: str) -> str:
    """Get the current user's Spotify ID"""
    response = get(f"{API_BASE}/me", headers=get_auth_header(access_token))
    return check_response_code(response, "trying current user ID")

# TOOL HELPERS
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

def get_my_playlists(access_token: str) -> dict:
    """Function for retrieving my playlists"""
    playlists = []
    url = GET_PLAYLISTS_ENDPOINT
    params = {"limit": 50}

    while url:
        response = get(url, headers=get_auth_header(access_token), params=params)
        data = check_response_code(response, "trying to get my playlists")

        print(data)

        if not data:
            break

        playlists.extend(data.get("items", []))
        url = data.get("next")
        params = None

    return playlists

def run():
    """Main function for interacting with Spotify"""
    auth_token_json = get_token()

    if not auth_token_json:
        print("Terminating")
        return

    search_token = auth_token_json["access_token"]
    # print("-----------------------------------------------------")
    # print("Drake:")
    # print(search_spotify(token, "artist", "Drake"))

    # print("\n-----------------------------------------------------")
    # print("Hardstone Pyscho:")
    # print(search_spotify(token, "album", "Hardstone Psycho"))

    # print("\n-----------------------------------------------------")
    # print("FWU:")
    # print(search_spotify(token, "track", "FWU"))

    print(get_my_playlists(search_token))
    user_token_json = get_access_token()
    if not user_token_json:
        print("Terminating")
        return

    user_token = user_token_json["access_token"]

    user_id = get_user_id(user_token)
    print(f"Authenticated as: {user_id}\n")

    playlists = get_my_playlists(user_token)
    for p in playlists:
        print(f"- {p['name']} (id: {p['id']}, tracks: {p['tracks']['total']})")

run()