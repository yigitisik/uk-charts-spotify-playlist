# UK Charts to Spotify Playlist Generator

A Python script that creates a Spotify playlist based on the UK Official Singles Chart from any date in history.

## Description

This project scrapes the UK Official Charts website for a specific date and automatically creates a Spotify playlist with the top tracks from that day. Perfect for nostalgia trips or discovering what was popular on a specific date!

## Features

- Scrapes UK Official Singles Chart for any historical date
- Searches for tracks on Spotify
- Automatically creates a public playlist on your Spotify account
- Limits to top 20 tracks for optimal playlist length

## Prerequisites

Before you begin, ensure you have:
- Python 3.7 or higher installed
- A Spotify account
- Spotify Developer credentials (see Setup section)

## Installation

1. Clone this repository:
```bash
   git clone https://github.com/yourusername/uk-charts-spotify-playlist.git
   cd uk-charts-spotify-playlist
```

2. Install required packages:
```bash
   pip install -r requirements.txt
```

3. Set up your Spotify API credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Copy your Client ID and Client Secret
   - Add `http://localhost:8080` as a Redirect URI in your app settings

4. Create your environment file:
   - Copy `keys.env.example` to `keys.env`
   - Fill in your Spotify credentials:
```
     cp keys.env.example keys.env
```
   - Edit `keys.env` with your actual credentials

## Usage

Run the script:
```bash
python main.py
```

When prompted, enter a date in `YYYY-MM-DD` format (e.g., `2015-06-15`).

The script will:
1. Fetch the UK Singles Chart for that date
2. Search for each track on Spotify
3. Create a new playlist named "MYI YYYY-MM-DD"
4. Add the tracks to your Spotify account

## Project Structure
```
uk-charts-spotify-playlist/
│
├── main.py                 # Main script
├── keys.env.example        # Template for environment variables
├── keys.env                # Your actual keys (NOT in git)
├── requirements.txt        # Python dependencies
├── .gitignore             # Files to ignore in git
└── README.md              # This file
```

## Dependencies

- `requests` - For HTTP requests to Official Charts
- `beautifulsoup4` - For parsing HTML
- `spotipy` - Spotify API wrapper
- `python-dotenv` - For loading environment variables

## Troubleshooting

**"Track not found on Spotify"**
- Some older tracks may not be available on Spotify
- The script will skip unavailable tracks

**Authentication errors**
- Verify your Spotify credentials in `keys.env`
- Ensure redirect URI matches your Spotify app settings
- Check that your app has the correct scopes enabled

**Date not found on Official Charts**
- Verify the date format is YYYY-MM-DD
- Check that the date is valid (charts may not exist for very old dates)

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments
- UK Official Charts Company for chart data
- Spotify Web API for music streaming integration

## Disclaimer
This project is for educational purposes. Please respect the terms of service for both the Official Charts website and Spotify API.
