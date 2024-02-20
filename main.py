# Import necessary libraries
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import time
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# Retrieve Spotify API credentials from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:8888/callback'

# Initialize the Spotify client with OAuth for accessing user's library and playlists
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-library-read, playlist-read-private'))

def main():
    # Create a YouTube API service object to interact with YouTube API
    service = create_youtube_api_service()

    # Retrieve saved tracks from Spotify and create a 'Favorites' playlist on YouTube, adding those tracks
    tracks = spotify_saved_tracks()
    favorites = "Favorites"
    playlist_id = youtube_create_playlist(service, favorites)
    youtube_add_track_to_playlist(service, tracks, playlist_id, favorites)

    # Retrieve user's Spotify playlists and replicate them on YouTube
    spotify_playlist_names, spotify_playlist_ids = spotify_saved_playlists()
    for i in range(3):  # Limit to exporting 3 playlists for demonstration
        youtube_playlist_id = youtube_create_playlist(service, spotify_playlist_names[i])
        tracks = spotify_playlist_tracks(spotify_playlist_ids[i])
        youtube_add_track_to_playlist(service, tracks, youtube_playlist_id, spotify_playlist_names[i])

def create_youtube_api_service():
    # Define API service name, version, and required scopes for accessing YouTube
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

    # Initialize OAuth flow and create credentials object for YouTube API
    flow = InstalledAppFlow.from_client_secrets_file(os.getenv("YOUTUBE_CREDENTIALS"), SCOPES)
    credentials = flow.run_local_server(port=0)

    # Build YouTube API service object with credentials
    service = build(API_NAME, API_VERSION, credentials=credentials)
    return service

def spotify_saved_tracks():
    # Fetch and display user's saved tracks from Spotify
    print("Your saved tracks:")
    tracks = []
    results = sp.current_user_saved_tracks(limit=50)
    items = results['items']

    # Paginate through Spotify results to retrieve all saved tracks
    while results['next']:
        results = sp.next(results)
        items.extend(results['items'])

    # Extract and format track name and artist for each saved track
    for item in items[:10]:  # Limit to first 10 tracks for demonstration
        track_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        formatted_track = f"{track_name} {artist_name}"
        tracks.append(formatted_track)
        print(track_name)
    return tracks

def spotify_saved_playlists():
    # Retrieve and display user's Spotify playlists
    results = sp.current_user_playlists()
    playlists = results['items']
    playlist_names = []
    playlist_ids = []

    print("User's playlists:")
    for playlist in playlists:
        print("Playlist: ", playlist['name'])
        playlist_names.append(playlist['name'])
        playlist_ids.append(playlist['id'])

    return playlist_names, playlist_ids

def spotify_playlist_tracks(playlist_id):
    # Fetch tracks within a specified Spotify playlist by ID
    tracks = []
    playlist_tracks = sp.playlist_tracks(playlist_id)

    print("Songs in the playlist:")
    for track in playlist_tracks['items']:
        print(track['track']['name'])
        tracks.append(track['track']['name'])

    return tracks

def youtube_create_playlist(service, playlist_name):
    # Create a new YouTube playlist with a given name
    print("Create Playlist:", playlist_name)
    request = service.playlists().insert(part='snippet', body={'snippet': {'title': playlist_name, 'description': ''}})
    response = request.execute()
    playlist_id = response['id']
    return playlist_id

def youtube_add_track_to_playlist(service, tracks, playlist_id, playlist_name):
    # Add tracks to a specified YouTube playlist by searching for each track and adding it to the playlist
    for track in tracks:
        retries = 5
        while retries > 0:
            try:
                # Search for YouTube video matching the track name
                request = service.search().list(part='id', q=track, type='video')
                response = request.execute()

                # Handle potential errors in search response
                if 'error' in response:
                    print("YouTube API Error:", response['error']['message'])

                # If a matching video is found, add it to the playlist
                if 'items' in response and response['items']:
                    video_id = response['items'][0]['id']['videoId']
                    request = service.playlistItems().insert(part='snippet', body={'snippet': {'playlistId': playlist_id, 'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}})
                    response = request.execute()
                    print("Track:", track, "added to playlist", playlist_name)
                    break
                else:
                    print("Video not found for track: ", track)
                    break

                time.sleep(1)  # Sleep to avoid rate limits

            except HttpError as e:
                # Handle specific HTTP errors, e.g., conflicts or service unavailability
                if e.resp.status in [409, 503]:
                    print(f"Error: {e}")
                    retries -= 1
                else:
                    print("An error has occurred")
                    break

if __name__ == "__main__":
    main()
