import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# --- Database Connection ---
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.get_database('playlist_converter')

# --- User Functions ---
def create_user(username, email, password):
    users_collection = db.get_collection('users')
    hashed_password = generate_password_hash(password)
    return users_collection.insert_one({
        'username': username,
        'email': email,
        'password': hashed_password
    })

def find_user_by_email(email):
    users_collection = db.get_collection('users')
    return users_collection.find_one({'email': email})

# --- Playlist Functions ---
def save_playlist(user_id, spotify_url, youtube_url, playlist_title):
    playlists_collection = db.get_collection('playlists')
    return playlists_collection.insert_one({
        'user_id': user_id,
        'spotify_url': spotify_url,
        'youtube_url': youtube_url,
        'playlist_title': playlist_title,
        'created_at': datetime.utcnow()
    })