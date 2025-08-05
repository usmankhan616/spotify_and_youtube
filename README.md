# PlaylistSync: Spotify to YouTube Converter

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</div>

**A full-stack web application that seamlessly converts your Spotify playlists into YouTube video playlists.**

---

### ► Overview

PlaylistSync is a web application designed to solve a common problem for music lovers: wanting to listen to a Spotify playlist on YouTube. This tool provides a simple and elegant interface for users to convert any public Spotify playlist into a new video playlist on their own YouTube account. It features a complete user authentication system, a personal profile page to track created playlists, and a secure connection to both the Spotify and YouTube APIs.

The application's backend is powered by Python and the Flask micro-framework. It communicates with the Spotify Web API to retrieve track data and utilizes a secure OAuth 2.0 flow with the YouTube Data API v3 to manage playlists on a user's behalf. All user information and conversion history are securely stored in a MongoDB Atlas cloud database. The frontend is built with clean HTML and modern CSS, providing a responsive and intuitive user experience across all devices.

### ✨ Key Features

-   **Full User Authentication:** Secure registration and login system with password hashing.
-   **Spotify Playlist Fetching:** Retrieves the complete tracklist from any public Spotify playlist.
-   **YouTube Playlist Creation:** Creates a new public or private video playlist on the user's YouTube account.
-   **Smart Video Search:** Automatically searches YouTube for the best video match for each song.
-   **User Profile Page:** Displays a history of all playlists created by the user.
-   **Cloud Database:** All data is stored securely on MongoDB Atlas.
-   **Modern UI:** A clean, responsive, and beautifully designed user interface.

### 🛠️ Technology Stack

| Category      | Technologies & Tools                                                                                               |
| :------------ | :----------------------------------------------------------------------------------------------------------------- |
| **Backend** | Python, Flask, Spotipy, Google API Python Client, PyMongo, Werkzeug, Python-dotenv                                 |
| **Frontend** | HTML5, CSS3, Google Fonts, Font Awesome                                                                            |
| **Database** | MongoDB Atlas                                                                                                      |
| **APIs** | Spotify Web API, YouTube Data API v3                                                                               |
| **DevOps** | Git, GitHub, Vercel                                                                                                |

### 🚀 Setup and Local Installation

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/usmankhan616/spotify-and-youtube.git](https://github.com/usmankhan616/spotify-and-youtube.git)
    cd spotify-and-youtube
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    -   Create a file named `.env` in the root directory.
    -   Add your API keys and database URI to this file:
        ```
        SPOTIPY_CLIENT_ID=your_spotify_client_id
        SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
        MONGO_URI=your_mongodb_atlas_connection_string
        ```

5.  **Add Google API Credentials:**
    -   Place your `client_secret.json` file (downloaded from Google Cloud Console) in the root directory.

6.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

### 🌐 Deployment

This application is configured for easy deployment on **Vercel**. Simply import the GitHub repository into Vercel, add the environment variables from your `.env` file, and deploy.