import sys
import os
import pandas as pd

# Dynamically add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import after modifying the path
#from SpotifyAnalyzer.utils import GenrePrediction
from src.SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalysis


sa = SpotifyAnalysis()

#GET TOP ARTIST SONGS---------------SUCCESS
# artist = input("\nEnter Artist :")
# sa.get_artist_top_tracks(artist)


# CHECK IF TOKEN IS VALID---------------SUCCESS
# sa.check_token_validity()


# CHECK REAUTHENTICATION---------------SUCCESS
# sa.Reauthenticate()


#CHECK USERS PLAYLISTS LIST---------------SUCCESS
# sa.get_user_id()
# list_of_playlists = sa.get_list_of_playlist()
# print(f"\nLIST OF PLAYLISTS")
# list_of_playlist_df = pd.DataFrame(list_of_playlists)
# print(list_of_playlist_df)


#CHECK USERS CURRENT PLAYLISTS CONTENT---------------SUCCESS
# playlist_id = input("\nEnter playlist ID: ")
# playlist_name , playlist_content  = sa.get_playlist_content(playlist_id=playlist_id)
# print(f"\nPLAYLIST CONTENT : {playlist_name}\n")
# playlist_df = pd.DataFrame(playlist_content)
# print(playlist_df)


#GET USERS LIKED SONG DETAILS---------------SUCCESS
# playlist_name, liked_song_details = sa.get_liked_songs_playlist()
# liked_song_df = pd.DataFrame(liked_song_details)
# print("\nplaylist naem: ",playlist_name)
# print(liked_song_df)


#GET USER ID FOR CURRENT USER FROM SPOTIFY---------------SUCCESS
# ui,un = sa.get_user_id()
# print(f"\nuser id  = {ui}\nuser_name = {un}")


#SAVING LIST OF PLAYLIST AS CSV FILE---------------SUCCESS
# playlist_name,playlist_content = sa.get_list_of_playlist()
# print(f"PLAYLIST NAME: {playlist_name}")
# print(pd.DataFrame(playlist_content))
# print("\nSaving started")
# sa.save_data_as_csv(playlist_name , content_code=1)


#SAVING THE DATA FROM SPOTIFY LOCALLY INTO CSV FILES  BY GIVING A SAVE_NAME,CONTENT---------------SUCCESS
# playlist_id = input("\nEnter playlist ID: ")
# playlist_name , playlist_content  = sa.get_playlist_content(playlist_id=playlist_id)
# print(f"\nPLAYLIST NAME : {playlist_name}\n")
# playlist_df = pd.DataFrame(playlist_content)
# print(playlist_df)
# print("\nSaving started")
# sa.save_data_as_csv(playlist_name , content_code=2)


#SAVING LIKED PLAYLIST DATA INTO CSV---------------SUCCESS
# playlist_name , playlist_content  = sa.get_liked_songs_playlist()
# print(f"\nPLAYLIST NAME : {playlist_name}\n")
# playlist_df = pd.DataFrame(playlist_content)
# print(playlist_df)
# print("\nSaving started")
# sa.save_data_as_csv(playlist_name , content_code=3)


# ISSUE IS WITH THE get_list_of_playlist() function in the line sa.current_user_playlists(limit= 20) line as api call returns this 
# {'href': 'https://api.spotify.com/v1/users/31uk6uyvtlxlm43l5tew5xjlosza/playlists?offset=0&limit=50', 'limit': 50, 'next': None, 'offset': 0, 'previous': None, 'total': 0, 'items': []}
# #  This mostly means that i have either hit my api rate limit or for some fucked up reason spotify api does not want to give me list of playlist of user
# Same is happening while fetching liked songs using sa.get_liked_songs_playlist() function