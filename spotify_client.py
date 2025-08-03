import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
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
        return song_list
    except Exception as e:
        print(f"An error occurred during Spotify fetch: {e}")
        return None