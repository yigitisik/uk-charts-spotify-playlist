# Import required libraries
from pprint import pprint  # For pretty-printing data structures (useful for debugging)
import requests  # For making HTTP requests to web pages
import spotipy  # Spotify API wrapper library
from bs4 import BeautifulSoup  # For parsing and scraping HTML content
import dotenv  # For loading environment variables from .env files

dotenv.load_dotenv(dotenv_path="keys.env")  # Load environment variables from keys.env file
import os  # For accessing environment variables

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

# Official Charts API Configuration
MAIN_URL = "https://www.officialcharts.com/charts/singles-chart/"  # Base URL for UK singles charts

# HTTP headers to mimic a real browser request (helps avoid bot detection)
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml"
}

# CSS selector path to find track names on the Official Charts page
PAGE_SELECTOR_PATH = ".no-intro div div:nth-child(1) div:nth-child(2) p:nth-child(1) a:nth-child(1) span:nth-child(2)"

# Spotify API Configuration
SPOTIPY_SCOPE = "playlist-modify-public"  # Permission scope needed to create and modify public playlists

# Load Spotify OAuth credentials from environment variables (stored in keys.env)
SPOTIFY_OAUTH_AUTHORIZE_URL = os.getenv("SPOTIFY_OAUTH_AUTHORIZE_URL")  # OAuth authorization endpoint
SPOTIFY_OAUTH_TOKEN_URL = os.getenv("SPOTIFY_OAUTH_TOKEN_URL")  # OAuth token endpoint
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")  # Redirect URI after authentication
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")  # Spotify app client ID
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")  # Spotify app client secret

# ============================================================================
# MAIN FUNCTION
# ============================================================================
def main():
    """
    Main function that orchestrates the entire playlist creation process:
    1. Prompts user for a date
    2. Scrapes the UK Singles Chart for that date
    3. Searches for matching tracks on Spotify
    4. Creates a new Spotify playlist with those tracks
    """

    # ========================================================================
    # STEP 1: Get user input and construct the chart URL
    # ========================================================================
    date_input = input("To what time in music life do you want to travel back to? Type in this format (YYYY-MM-DD):\n")
    generated_endpoint = f"{MAIN_URL}{date_input}/7501/"  # Construct full URL with date (7501 appears to be a chart ID)

    # ========================================================================
    # STEP 2: Scrape the Official Charts website
    # ========================================================================
    api_resp = requests.get(url=generated_endpoint, headers=HEADER)  # Make HTTP request to get chart page

    # Parse the HTML response using BeautifulSoup
    playlist_soup = BeautifulSoup(api_resp.text, "html.parser")

    # Extract all track names using the CSS selector
    selected_items = playlist_soup.select(selector=PAGE_SELECTOR_PATH)
    # print(selected_items)  # Debugging line (commented out)

    # ========================================================================
    # STEP 3: Authenticate with Spotify
    # ========================================================================
    # Create OAuth connection manager for Spotify authentication
    spotify_connection = spotipy.oauth2.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SPOTIPY_SCOPE)

    # Get access token (initiates OAuth flow if needed)
    spotify_connection.get_access_token(as_dict=False)

    # Create Spotify client with authenticated session
    spotipy_client = spotipy.client.Spotify(oauth_manager=spotify_connection)

    # Get current user information
    spotify_user = spotipy_client.current_user()
    # pprint(spotify_user)  # Debugging line (commented out)

    # Extract user ID from user profile (needed for playlist creation)
    spotify_user_id = spotify_user["id"]

    # ========================================================================
    # STEP 4: Search for tracks on Spotify and collect URIs
    # ========================================================================
    track_uris = []  # List to store Spotify track URIs
    count = 0  # Counter to limit number of tracks

    # Loop through each track found on the charts page
    for track in selected_items:
        if count >= 20:  # Limit playlist to 20 tracks
            break

        track_name = track.getText()  # Extract track name from HTML element

        # Search for the track on Spotify (limit to 1 result)
        track_search_result = spotipy_client.search(q=track_name, type="track", limit=1)

        # Extract the track URI from search results
        # URI format is "spotify:track:<uri_value>", so split on ":" and take the 3rd element
        track_uri = track_search_result["tracks"]["items"][0]["uri"].split(":")[2]

        # Add URI to our list
        track_uris.append(track_uri)
        count += 1  # Increment counter

    # ========================================================================
    # STEP 5: Create Spotify playlist and add tracks
    # ========================================================================
    # Create a new public playlist on the user's Spotify account
    spotipy_playlist = spotipy_client.user_playlist_create(
        user=spotify_user_id,
        name=f"MYI {date_input}",  # Playlist name includes the date
        public=True,  # Make playlist publicly visible
        description=f"generated playlist from date chosen as:{date_input}")  # Description with date

    # Extract the playlist ID from the created playlist
    playlist_id = spotipy_playlist['id']

    # Add all collected track URIs to the newly created playlist
    spotipy_client.playlist_add_items(playlist_id=playlist_id, items=track_uris)

# SCRIPT ENTRY POINT
main()  # Execute the main function when script is run