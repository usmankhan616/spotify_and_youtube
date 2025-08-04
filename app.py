import os
from flask import Flask, render_template, request, redirect, session, url_for
from spotify_client import get_playlist_songs
from youtube_client import create_playlist, add_songs_to_playlist
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials # <-- ADD THIS IMPORT

app = Flask(__name__)
app.secret_key = os.urandom(24)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    session['spotify_url'] = request.form.get('spotify_url')
    session['playlist_title'] = request.form.get('playlist_title')

    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    return redirect(url_for('create_youtube_playlist'))

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('create_youtube_playlist'))

@app.route('/create')
def create_youtube_playlist():
    if 'credentials' not in session or 'spotify_url' not in session:
        return redirect(url_for('index'))

    try:
        spotify_url = session.pop('spotify_url', None)
        playlist_title = session.pop('playlist_title', None)
        
        # Updated to handle two return values
        song_list, error_message = get_playlist_songs(spotify_url)
        
        # If there's an error message, display it
        if error_message:
            return render_template('index.html', error=error_message)

        credentials = Credentials(**session['credentials'])
        youtube_service = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials)
        
        new_playlist_id = create_playlist(youtube_service, playlist_title, "Created from Spotify", "public")
        add_songs_to_playlist(youtube_service, new_playlist_id, song_list)
        
        result_url = f"https://www.youtube.com/playlist?list={new_playlist_id}"
        return render_template('index.html', result_url=result_url)
    
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)