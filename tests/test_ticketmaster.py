"""Tests for the ticketmaster module."""

from concert_radar.ticketmaster import extract_event_info, search_events_for_artist


# A minimal fake event that matches Ticketmaster's response shape
SAMPLE_EVENT = {
    "name": "Taylor Swift | The Eras Tour",
    "url": "https://www.ticketmaster.com/event/12345",
    "dates": {"start": {"localDate": "2026-08-15", "localTime": "20:00:00"}},
    "priceRanges": [{"min": 89.5, "max": 899.0, "currency": "USD"}],
    "_embedded": {
        "venues": [{
            "name": "MetLife Stadium",
            "city": {"name": "East Rutherford"},
            "state": {"stateCode": "NJ"},
        }],
    },
}


def test_extract_event_info_pulls_all_fields():
    """extract_event_info should return all expected fields from a full event."""
    result = extract_event_info(SAMPLE_EVENT)

    assert result["name"] == "Taylor Swift | The Eras Tour"
    assert result["date"] == "2026-08-15"
    assert result["time"] == "20:00:00"
    assert result["venue"] == "MetLife Stadium"
    assert result["city"] == "East Rutherford"
    assert result["state"] == "NJ"
    assert result["price"] == "$89.5-$899.0"
    assert result["url"] == "https://www.ticketmaster.com/event/12345"


def test_extract_event_info_handles_missing_price():
    """When priceRanges is missing, price should say 'Price TBA'."""
    event_no_price = {k: v for k, v in SAMPLE_EVENT.items() if k != "priceRanges"}
    result = extract_event_info(event_no_price)
    assert result["price"] == "Price TBA"


def test_extract_event_info_handles_missing_venue():
    """When venues list is empty, venue fields should have safe defaults."""
    event_no_venue = {**SAMPLE_EVENT, "_embedded": {"venues": []}}
    result = extract_event_info(event_no_venue)
    assert result["venue"] == "Unknown Venue"
    assert result["city"] == "Unknown City"
    assert result["state"] == ""


def test_extract_event_info_handles_missing_dates():
    """When dates are missing, date/time should be 'TBA'."""
    event_no_dates = {**SAMPLE_EVENT, "dates": {}}
    result = extract_event_info(event_no_dates)
    assert result["date"] == "TBA"
    assert result["time"] == "TBA"


def test_search_returns_empty_on_api_error(mocker):
    """When the API returns a non-200 status, we should get an empty list.
    Uses pytest-mock to fake the requests.get call — no real network hit."""
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mocker.patch("concert_radar.ticketmaster.requests.get", return_value=mock_response)

    result = search_events_for_artist("Anyone", "fake_key")
    assert result == []


def test_search_parses_successful_response(mocker):
    """When the API returns 200 with events, we should get parsed dicts back."""
    fake_api_response = {"_embedded": {"events": [SAMPLE_EVENT]}}

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_api_response
    mocker.patch("concert_radar.ticketmaster.requests.get", return_value=mock_response)

    result = search_events_for_artist("Taylor Swift", "fake_key")
    assert len(result) == 1
    assert result[0]["name"] == "Taylor Swift | The Eras Tour"