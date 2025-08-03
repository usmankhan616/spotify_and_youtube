from spotify_client import get_playlist_songs
from youtube_client import get_authenticated_service, create_playlist, add_songs_to_playlist

def main():
    spotify_playlist_url = "https://open.spotify.com/playlist/530gAraM8G9yBnl2Bqkl62?si=Qjg5_6ViSPWFWEVj-JowoA"
    
    print("Fetching songs from Spotify...")
    song_list = get_playlist_songs(spotify_playlist_url)

    if song_list:
        print(f"Successfully fetched {len(song_list)} songs from Spotify.")
        
        print("\nPlease log in to your Google account to authorize YouTube access...")
        youtube_service = get_authenticated_service()
        
        playlist_title = "My Sad Bollywood Songs (from Spotify)"
        playlist_description = f"A playlist created from Spotify playlist: {spotify_playlist_url}"
        new_playlist_id = create_playlist(youtube_service, playlist_title, playlist_description)
        
        add_songs_to_playlist(youtube_service, new_playlist_id, song_list)
        
        print("\nProcess complete!")
        print(f"View your new playlist here: https://www.youtube.com/playlist?list={new_playlist_id}")
    else:
        print("Could not fetch song list from Spotify. Exiting.")

if __name__ == '__main__':
    main()