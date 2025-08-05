import os
import json
from flask import Flask, render_template, request, redirect, session, url_for, flash
from spotify_client import get_playlist_songs
from youtube_client import create_playlist, add_songs_to_playlist
from database import create_user, find_user_by_email, save_playlist, get_user_playlists
from werkzeug.security import check_password_hash
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- YouTube OAuth Configuration ---
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Load client secrets from environment variable
try:
    CLIENT_SECRETS_STR = os.getenv('CLIENT_SECRET_JSON')
    CLIENT_SECRETS_DICT = json.loads(CLIENT_SECRETS_STR)
except (TypeError, json.JSONDecodeError):
    CLIENT_SECRETS_DICT = None
    print("ERROR: CLIENT_SECRET_JSON environment variable is not set or is invalid.")


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = find_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        if find_user_by_email(email):
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        create_user(username, email, password)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_details = {'username': session['username'], 'email': session['email']}
    user_playlists = get_user_playlists(session['user_id'])
    return render_template('profile.html', user=user_details, playlists=user_playlists)

@app.route('/convert', methods=['POST'])
def convert():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    session['spotify_url'] = request.form.get('spotify_url')
    session['playlist_title'] = request.form.get('playlist_title')
    session['privacy_status'] = request.form.get('privacy')
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    return redirect(url_for('create_youtube_playlist'))

@app.route('/authorize')
def authorize():
    if not CLIENT_SECRETS_DICT:
        return "Server configuration error: YouTube client secrets are not set.", 500
    # Use from_client_config instead of from_client_secrets_file
    flow = google_auth_oauthlib.flow.Flow.from_client_config(CLIENT_SECRETS_DICT, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    if not state or not CLIENT_SECRETS_DICT:
        return redirect(url_for('login'))
    # Use from_client_config instead of from_client_secrets_file
    flow = google_auth_oauthlib.flow.Flow.from_client_config(CLIENT_SECRETS_DICT, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token, 'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri, 'client_id': credentials.client_id,
        'client_secret': credentials.client_secret, 'scopes': credentials.scopes
    }
    return redirect(url_for('create_youtube_playlist'))

@app.route('/create')
def create_youtube_playlist():
    if 'user_id' not in session or 'credentials' not in session or 'spotify_url' not in session:
        return redirect(url_for('login'))
    try:
        spotify_url = session.pop('spotify_url', None)
        playlist_title = session.pop('playlist_title', None)
        privacy_status = session.pop('privacy_status', 'private')
        credentials = Credentials(**session['credentials'])
        
        youtube_service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        
        song_list, error_message = get_playlist_songs(spotify_url)
        if error_message:
            return render_template('dashboard.html', username=session.get('username'), error=error_message)
        
        new_playlist_id = create_playlist(youtube_service, playlist_title, f"Created from {spotify_url}", privacy_status)
        add_songs_to_playlist(youtube_service, new_playlist_id, song_list)
        
        result_url = f"https://www.youtube.com/playlist?list={new_playlist_id}"
        save_playlist(session['user_id'], spotify_url, result_url, playlist_title, privacy_status)
        
        return render_template('dashboard.html', username=session.get('username'), result_url=result_url)
    except Exception as e:
        return render_template('dashboard.html', username=session.get('username'), error=str(e))

# This is needed for Vercel to find the app
if __name__ == "__main__":
    app.run(debug=True)