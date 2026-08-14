"""Ticketmaster Discovery API client for Concert Radar."""

import requests

BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def extract_event_info(event):
    """
    Take one raw event dict from the Ticketmaster API and return a clean
    dict with just the fields Concert Radar needs.

    Uses .get() everywhere because not every event has every field.
    """
    name = event.get("name", "Unknown Event")
    ticket_url = event.get("url", "")

    # Date info is nested inside dates.start
    dates = event.get("dates", {}).get("start", {})
    event_date = dates.get("localDate", "TBA")
    event_time = dates.get("localTime", "TBA")

    # Venue info is nested inside _embedded.venues[0]
    venues = event.get("_embedded", {}).get("venues", [])
    if venues:
        venue = venues[0]
        venue_name = venue.get("name", "Unknown Venue")
        city = venue.get("city", {}).get("name", "Unknown City")
        state = venue.get("state", {}).get("stateCode", "")
    else:
        venue_name, city, state = "Unknown Venue", "Unknown City", ""

    # Price range is often missing — handle gracefully
    price_ranges = event.get("priceRanges", [])
    if price_ranges:
        min_price = price_ranges[0].get("min", "?")
        max_price = price_ranges[0].get("max", "?")
        price_str = f"${min_price}-${max_price}"
    else:
        price_str = "Price TBA"

    return {
        "name": name,
        "date": event_date,
        "time": event_time,
        "venue": venue_name,
        "city": city,
        "state": state,
        "price": price_str,
        "url": ticket_url,
    }


def search_events_for_artist(artist_name, api_key, city=None, state_code=None, size=10):
    """
    Search Ticketmaster for upcoming events matching an artist name.
    Optionally filter to a specific city and/or state.
    Returns a list of clean event dictionaries.
    Returns empty list on API error or network failure.
    """
    params = {
        "apikey": api_key,
        "keyword": artist_name,
        "classificationName": "music",
        "size": size,
        "countryCode": "US",
        "sort": "date,asc",
    }
    if city:
        params["city"] = city
    if state_code:
        params["stateCode"] = state_code

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as e:
        print(f"Network error searching for {artist_name}: {e}")
        return []

    if response.status_code != 200:
        print(f"API error for {artist_name}: HTTP {response.status_code}")
        return []

    data = response.json()
    raw_events = data.get("_embedded", {}).get("events", [])
    return [extract_event_info(ev) for ev in raw_events]


def search_events_for_artists(artist_list, api_key, city=None, state_code=None):
    """
    Search for events across a list of artists. Tags each result with
    which artist matched it. Returns a flat list of event dictionaries.
    """
    all_matches = []
    for artist in artist_list:
        events = search_events_for_artist(artist, api_key, city=city, state_code=state_code)
        for event in events:
            event["matched_artist"] = artist
            all_matches.append(event)
    return all_matches