import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv

load_dotenv()

def get_playlist_songs(playlist_url):
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        playlist_id = playlist_url.split('/')[-1].split('?')[0]
        results = sp.playlist_tracks(playlist_id, market='IN')
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        song_list = []
        for item in tracks:
            if item.get('track'):
                song_name = item['track']['name']
                artist_name = item['track']['artists'][0]['name']
                song_list.append({'song': song_name, 'artist': artist_name})
        # On success, return the list and no error message
        return song_list, None
    
    except SpotifyException as e:
        # Check for specific error codes
        if e.http_status == 429 or e.http_status >= 500:
            error_message = "Spotify is currently busy. Please try again in 15-30 minutes."
            return None, error_message
        else:
            # Handle other potential Spotify API errors
            return None, f"A Spotify API error occurred: {e.msg}"
            
    except Exception as e:
        # Handle other general errors (e.g., network issues)
        return None, f"An unexpected error occurred: {str(e)}"