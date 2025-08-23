import os
from ytmusicapi import YTMusic
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# load environment variable
load_dotenv(dotenv_path=".env.api", override=True)
load_dotenv(dotenv_path=".env.path", override=True)
# Path to your OAuth client secrets JSON downloaded from Google Cloud Console
CLIENT_SECRETS_FILE = 'client_secrets.json'
OAUTH_TOKEN_FILE = os.path.join(os.getenv("YTMUSIC_CACHE_PATH") , ".cache")
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_and_get_token():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8080)  # Starts localhost server, open browser for consent

    # Save token for future use
    with open(OAUTH_TOKEN_FILE, 'w') as f:
        f.write(credentials.to_json())

    return OAUTH_TOKEN_FILE

def main():
    # Authenticate only if token file doesn't exist
    if not os.path.exists(OAUTH_TOKEN_FILE):
        authenticate_and_get_token()

    # Initialize YTMusic with OAuth token file
    ytmusic = YTMusic(OAUTH_TOKEN_FILE)

    # Fetch user playlists
    playlists = ytmusic.get_library_playlists()
    print("User Playlists:")
    for p in playlists:
        print(f"{p['title']} (ID: {p['playlistId']})")

if __name__ == "__main__":
    main()
