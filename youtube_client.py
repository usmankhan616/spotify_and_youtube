import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

def create_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": { "title": title, "description": description, "defaultLanguage": "en" },
            "status": { "privacyStatus": "private" }
        }
    )
    response = request.execute()
    print(f"Created new YouTube playlist with ID: {response['id']}")
    return response['id']

def add_songs_to_playlist(youtube, playlist_id, song_list):
    for song_info in song_list:
        query = f"{song_info['song']} by {song_info['artist']} official video"
        print(f"Searching for: {query}")
        search_request = youtube.search().list(
            part="snippet", maxResults=1, q=query, type="video"
        )
        search_response = search_request.execute()
        if not search_response["items"]:
            print(f"--> Could not find a video for '{query}'. Skipping.")
            continue
        video_id = search_response["items"][0]["id"]["videoId"]
        video_title = search_response["items"][0]["snippet"]["title"]
        print(f"--> Found '{video_title}'. Adding to playlist.")
        add_request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": { "kind": "youtube#video", "videoId": video_id }
                }
            }
        )
        add_request.execute()