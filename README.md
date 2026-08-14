# Concert Radar

![Tests](https://github.com/cm7113/concert-radar/workflows/Tests/badge.svg)

A Python application that sends email alerts when your favorite artists announce concerts in your state. Concert Radar queries the Ticketmaster Discovery API for upcoming shows by a user-defined list of artists, filters results by location, and delivers a formatted HTML email summary containing venue details, dates, prices, and direct ticket purchase links.

## Setup

Clone the repo to download it from GitHub. Perhaps onto the Desktop.

Navigate to the repo using the command line.

```
cd ~/Desktop/concert-radar
```

Create a virtual environment:

```
conda create -n concert-radar python=3.11
```

Activate the virtual environment:

```
conda activate concert-radar
```

Install package dependencies:

```
pip install -r requirements.txt
```

## Configuration

The application requires a Ticketmaster API key for fetching concert data, and Gmail credentials for sending email notifications.

Obtain a free [Ticketmaster API key](https://developer.ticketmaster.com/) by signing up, creating a new app, and copying the Consumer Key.

Obtain a 16-character Gmail App Password by enabling 2-Step Verification on your Google account, then generating an app password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

Create a local ".env" file and store your environment variables in there:

```
# this is the ".env" file...

TICKETMASTER_API_KEY="______________"

GMAIL_ADDRESS="______________"
GMAIL_APP_PASSWORD="______________"
NOTIFICATION_TO_ADDRESS="______________"

# comma-separated list of artists to watch
FAVORITE_ARTISTS="Taylor Swift,Olivia Rodrigo,The Weeknd"

# 2-letter state code (recommended for broad metro coverage)
TARGET_STATE="NY"

# optional: exact city name (strict filter)
# TARGET_CITY="New York"
```

## Usage

Run the Concert Radar watcher to fetch upcoming shows and send an email:

```
python app.py
```

The application will print progress to the terminal and send a formatted HTML email to the address specified in `NOTIFICATION_TO_ADDRESS`. Example output:

```
Concert Radar starting...
   Watching 5 artists in NY
   Found 14 matching show(s)
Email sent!
```

## Testing

Run tests:

```
pytest
```

The test suite uses mocked API responses via `pytest-mock`, so tests run instantly without consuming your Ticketmaster rate limit or sending real emails.

## Continuous Integration

Every push to `main` and every pull request automatically triggers the full test suite via GitHub Actions. See `.github/workflows/tests.yml` for the workflow configuration. The build status badge at the top of this README reflects the latest run.