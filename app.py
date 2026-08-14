"""Concert Radar — main entry point.

Fetches upcoming concerts for your favorite artists in your target city,
then emails you a formatted summary.
"""

from concert_radar import config
from concert_radar.ticketmaster import search_events_for_artists
from concert_radar.notifier import build_concert_email_html, send_email


def main():
    """Run the full Concert Radar pipeline once."""
    # Fail if any required config is missing
    config.validate_config()

    print(" Concert Radar starting...")
    location=config.TARGET_CITY or config.TARGET_STATE or "anywhere in the US"
    print(f" Watching {len(config.FAVORITE_ARTISTS)} artists in {location}")

    # Fetch concerts across all favorite artists
    events = search_events_for_artists(
        config.FAVORITE_ARTISTS,
        config.TICKETMASTER_API_KEY,
        city=config.TARGET_CITY,
        state_code=config.TARGET_STATE,
    )

    print(f"   Found {len(events)} matching show(s)")

    if not events:
        print("   No shows to email — done.")
        return

    # Build and send the email (cap at 10 events for readability)
    email_html = build_concert_email_html(events[:10])
    #include target location in subject line so it's clear at glance where the shows are
    location=config.TARGET_CITY or config.TARGET_STATE or "your area"
    subject = f"Concert Radar: {len(events)} show(s) in {location}"

    success = send_email(
        to_address=config.NOTIFICATION_TO_ADDRESS,
        subject=subject,
        html_body=email_html,
        from_address=config.GMAIL_ADDRESS,
        app_password=config.GMAIL_APP_PASSWORD,
    )

    print("Email sent!" if success else "Email failed.")


if __name__ == "__main__":
    main()
