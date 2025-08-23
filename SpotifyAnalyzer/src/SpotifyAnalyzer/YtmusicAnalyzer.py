import os
from ytmusicapi import YTMusic, OAuthCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# Load environment variables from both files
load_dotenv(dotenv_path=".env.api", override=True)
load_dotenv(dotenv_path=".env.path", override=True)

OAUTH_TOKEN_FILE = "src\cache\ytmusic_cache\oauth.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
print("Cache path:", os.getenv("YTMUSIC_CACHE_PATH"))
def authenticate_and_get_token():
    client_id = os.getenv("YTMUSIC_OAUTH_CLIENT_ID")
    client_secret = os.getenv("YTMUSIC_OAUTH_CLIENT_SECRET")
    redirect_uri = os.getenv("YTMUSIC_API_REDIRECT_URI")

    # Build client config dict for OAuth flow
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_local_server(port=8080)

    # Save token for future use
    with open(OAUTH_TOKEN_FILE, 'w') as f:
        f.write(credentials.to_json())

    return OAUTH_TOKEN_FILE

def main():
    if not os.path.exists(OAUTH_TOKEN_FILE):
        authenticate_and_get_token()

    # Pass OAuth credentials explicitly to YTMusic
    client_id = os.getenv("YTMUSIC_OAUTH_CLIENT_ID")
    client_secret = os.getenv("YTMUSIC_OAUTH_CLIENT_SECRET")
    ytmusic = YTMusic(
        OAUTH_TOKEN_FILE,
        oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret)
    )

    playlists = ytmusic.get_library_playlists()
    print("User Playlists:")
    for p in playlists:
        print(f"{p['title']} (ID: {p['playlistId']})")

if __name__ == "__main__":
    main()
