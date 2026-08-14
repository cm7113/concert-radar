"""Configuration loader — reads settings from .env file."""

import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

# API credentials
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

# Email credentials
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
NOTIFICATION_TO_ADDRESS = os.getenv("NOTIFICATION_TO_ADDRESS", GMAIL_ADDRESS)

# parse comma-separated string into a list
_artists_raw = os.getenv("FAVORITE_ARTISTS", "")
FAVORITE_ARTISTS = [a.strip() for a in _artists_raw.split(",") if a.strip()]

TARGET_CITY = os.getenv("TARGET_CITY")
TARGET_STATE = os.getenv("TARGET_STATE")


def validate_config():
    """Raise a helpful error if any required setting is missing."""
    required = {
        "TICKETMASTER_API_KEY": TICKETMASTER_API_KEY,
        "GMAIL_ADDRESS": GMAIL_ADDRESS,
        "GMAIL_APP_PASSWORD": GMAIL_APP_PASSWORD,
    }
    missing = [name for name, val in required.items() if not val]
    if missing:
        raise ValueError(
            f"Missing required env vars: {', '.join(missing)}. "
            "Copy .env.example to .env and fill in your values."
        )
    if not FAVORITE_ARTISTS:
        raise ValueError("FAVORITE_ARTISTS is empty in .env — add at least one artist.")