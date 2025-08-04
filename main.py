from spotify_client import get_playlist_songs
from youtube_client import get_authenticated_service, create_playlist, add_songs_to_playlist
from database import create_user, find_user_by_email, save_playlist
from werkzeug.security import check_password_hash

def main():
    logged_in_user = None

    while True:
        choice = input("Welcome! Do you want to [1] Register or [2] Login? ")
        if choice == '1':
            email = input("Enter your email: ")
            if find_user_by_email(email):
                print("An account with this email already exists.")
                continue
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            create_user(username, email, password)
            print("Registration successful! Please log in.")
        
        elif choice == '2':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user = find_user_by_email(email)
            if user and check_password_hash(user['password'], password):
                print(f"Welcome back, {user['username']}!")
                logged_in_user = user
                break
            else:
                print("Invalid email or password.")
        else:
            print("Invalid choice.")

    if logged_in_user:
        spotify_playlist_url = input("Please enter the Spotify playlist URL to convert: ")
        
        print("\nFetching songs from Spotify...")
        song_list = get_playlist_songs(spotify_playlist_url)

        if song_list:
            print(f"Successfully fetched {len(song_list)} songs from Spotify.")
            
            print("\nPlease log in to your Google account to authorize YouTube access...")
            youtube_service = get_authenticated_service()
            
            playlist_title = input("Enter a title for your new YouTube playlist: ")

            # Ask the user for their privacy choice
            privacy_choice = input("Make playlist [1] Public or [2] Private? ")
            privacy_status = "public" if privacy_choice == '1' else "private"

            playlist_description = f"Created from Spotify: {spotify_playlist_url}"
            # Pass the user's choice to the function
            new_playlist_id = create_playlist(youtube_service, playlist_title, playlist_description, privacy_status)
            
            add_songs_to_playlist(youtube_service, new_playlist_id, song_list)
            
            youtube_link = f"https://www.youtube.com/playlist?list={new_playlist_id}"
            save_playlist(logged_in_user['_id'], spotify_playlist_url, youtube_link, playlist_title)

            print("\nProcess complete!")
            print(f"View your new playlist here: {youtube_link}")
        else:
            print("Could not fetch song list from Spotify. Exiting.")

if __name__ == '__main__':
    main()