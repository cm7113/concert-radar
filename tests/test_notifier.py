"""Tests for the notifier module."""

from concert_radar.notifier import build_concert_email_html


def test_empty_events_returns_friendly_message():
    """With no events, the email body should say so."""
    html = build_concert_email_html([])
    assert "No new concerts" in html


def test_email_includes_event_details():
    """The generated HTML should contain each event's details."""
    events = [{
        "name": "Test Concert",
        "matched_artist": "Test Artist",
        "date": "2026-09-01",
        "time": "20:00",
        "venue": "Test Venue",
        "city": "Test City",
        "state": "NY",
        "price": "$50-$100",
        "url": "https://example.com/tickets",
    }]

    html = build_concert_email_html(events)

    assert "Test Concert" in html
    assert "Test Artist" in html
    assert "Test Venue" in html
    assert "https://example.com/tickets" in html


def test_multiple_events_all_appear():
    """When passed multiple events, all should appear in the HTML."""
    events = [
        {"name": "Show A", "matched_artist": "Artist 1", "date": "2026-01-01",
         "time": "20:00", "venue": "V1", "city": "C1", "state": "NY",
         "price": "$50", "url": "https://a.com"},
        {"name": "Show B", "matched_artist": "Artist 2", "date": "2026-02-02",
         "time": "21:00", "venue": "V2", "city": "C2", "state": "CA",
         "price": "$75", "url": "https://b.com"},
    ]

    html = build_concert_email_html(events)
    assert "Show A" in html
    assert "Show B" in html