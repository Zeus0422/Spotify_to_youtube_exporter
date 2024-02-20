# Spotify to YouTube Playlist Transfer

This Python application automates the transfer of saved tracks and playlists from Spotify to YouTube. It uses the Spotify Web API to fetch saved tracks and playlists from a user's Spotify account and the YouTube Data API to create corresponding playlists on YouTube, populating them with matching tracks found on YouTube.

## Overview

The program is divided into several key functions, each handling a specific part of the transfer process, including authenticating with Spotify and YouTube, fetching data from Spotify, creating playlists on YouTube, and populating these playlists with tracks.

## Setup

Before running the program, ensure you have the necessary credentials:

- Spotify Client ID and Client Secret
- YouTube API credentials in a `client_secrets.json` file

Store your Spotify credentials in a `.env` file as `CLIENT_ID` and `CLIENT_SECRET`.

## Main Components

### `main()`

The entry point of the program. It orchestrates the flow of the application, starting with creating a YouTube API service object, transferring saved Spotify tracks to a YouTube playlist, and replicating Spotify playlists on YouTube.

### `create_youtube_api_service()`

Initializes and returns a service object for interacting with the YouTube API. It handles OAuth 2.0 authentication using the credentials stored in `client_secrets.json`.

### `spotify_saved_tracks()`

Fetches the user's saved tracks from Spotify, formatting each track's name and artist for YouTube searches. It returns a list of formatted track names.

### `spotify_saved_playlists()`

Retrieves the names and IDs of the user's Spotify playlists, returning them as two lists for further processing.

### `spotify_playlist_tracks(playlist_id)`

Given a Spotify playlist ID, fetches the tracks within the playlist. It returns a list of track names.

### `youtube_create_playlist(service, playlist_name)`

Creates a new YouTube playlist with the specified name using the YouTube API service object. It returns the ID of the newly created playlist.

### `youtube_add_track_to_playlist(service, tracks, playlist_id, playlist_name)`

Attempts to find each track on YouTube using the provided track names, adding found videos to the specified YouTube playlist. Handles retries and rate limiting.

## Additional Information

This program showcases the use of APIs to integrate services (Spotify and YouTube), demonstrating authentication flows, data manipulation, and automated web interactions. It's a practical example of bridging content between different platforms, useful for personal music library management and automation enthusiasts.

## Note

The program is designed for educational purposes and personal use. Ensure you comply with the terms of service for Spotify and YouTube when using their APIs.

## Credits

This Blackjack game was developed by Carlos Eckert, a passionate programmer with a keen interest in creating engaging and interactive gaming experiences. For more information on the developer or to explore other projects, visit https://github.com/Zeus0422 or contact via email: carloseckert05coding@gmail.com. 