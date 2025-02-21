import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.api")

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
def Spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-top-read user-read-recently-played user-library-read playlist-read-private playlist-read-collaborative user-read-private",
        cache_path=None,
        show_dialog=True
    ))
    return sp
sp = Spotify()

list_track_id = ['1SDiiE3v2z89VxC3aVRKHQ', '3JLrri1xSCui3bzITDJbkk', '6hu1f1cXSw7OAqhpSQ2zDy', '5CQ30WqJwcep0pYcV4AMNc', '70gbuMqwNBE2Y5rkQJE9By', '4JiEyzf0Md7KEFFGWDDdCr', '2N2yrmodOnVF10mKvItC9P', '6Vjk8MNXpQpi0F4BefdTyq', '4EUe6BsZm5wZLxOTaV3kDX', '3YRCqOhFifThpSRFJ1VWFM', '6mAfxuTuRz1FWfriiFf57y', '516pgYk3ZUqaK8af3LDEoo', '3TLKuI3AsHU1p6xWVorCsR', '7FtRUrOEDUHTvenvp1BqZo', '7snQQk1zcKl8gZ92AnueZW', '6eN1f9KNmiWEhpE2RhQqB5', '6i4Qi1mJxXjqNIL9HfJhRs', '3s03nrUInN3NAVjQtmnS0O', '3ovjw5HZZv43SxTwApooCM', '0RdUX4WE0fO30VnlUbDVL6', '1Eolhana7nKHYpcYpdVcT5', '0NWPxcsf5vdjdiFUI8NgkP', '0wJoRiX5K5BxlqZTolB2LD', '3lnavfgHUTrxdRqcPmhqUA', '40riOy7x9W7GXjyGp4pjAv']
string_track_id = '1SDiiE3v2z89VxC3aVRKHQ,3JLrri1xSCui3bzITDJbkk,6hu1f1cXSw7OAqhpSQ2zDy,5CQ30WqJwcep0pYcV4AMNc,70gbuMqwNBE2Y5rkQJE9By,4JiEyzf0Md7KEFFGWDDdCr,2N2yrmodOnVF10mKvItC9P,6Vjk8MNXpQpi0F4BefdTyq,4EUe6BsZm5wZLxOTaV3kDX,3YRCqOhFifThpSRFJ1VWFM,6mAfxuTuRz1FWfriiFf57y,516pgYk3ZUqaK8af3LDEoo,3TLKuI3AsHU1p6xWVorCsR,7FtRUrOEDUHTvenvp1BqZo,7snQQk1zcKl8gZ92AnueZW,6eN1f9KNmiWEhpE2RhQqB5,6i4Qi1mJxXjqNIL9HfJhRs,3s03nrUInN3NAVjQtmnS0O,3ovjw5HZZv43SxTwApooCM,0RdUX4WE0fO30VnlUbDVL6,1Eolhana7nKHYpcYpdVcT5,0NWPxcsf5vdjdiFUI8NgkP,0wJoRiX5K5BxlqZTolB2LD,3lnavfgHUTrxdRqcPmhqUA,40riOy7x9W7GXjyGp4pjAv'
result = sp.audio_features(['1SDiiE3v2z89VxC3aVRKHQ'])

print(result)