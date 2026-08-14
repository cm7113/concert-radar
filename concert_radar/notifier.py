"""Email notification module for Concert Radar."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def build_concert_email_html(events):
    """
    Take a list of event dictionaries and return a formatted HTML email body.
    """
    if not events:
        return "<p>No new concerts found.</p>"

    html = """
    <html>
      <body style="font-family: Arial, sans-serif; max-width: 600px;">
        <h2 style="color: #6a1b9a;">Concert Radar Alert</h2>
        <p>Here are the upcoming shows for your artists:</p>
        <hr>
    """

    for event in events:
        html += f"""
        <div style="margin-bottom: 20px; padding: 12px; background: #f9f9f9; border-left: 4px solid #6a1b9a;">
          <h3 style="margin: 0; color: #333;">{event['name']}</h3>
          <p style="margin: 4px 0;"><strong>Matched artist:</strong> {event.get('matched_artist', '—')}</p>
          <p style="margin: 4px 0;"> {event['date']} at {event['time']}</p>
          <p style="margin: 4px 0;"> {event['venue']}, {event['city']}, {event['state']}</p>
          <p style="margin: 4px 0;"> {event['price']}</p>
          <p style="margin: 8px 0;">
            <a href="{event['url']}" style="background: #6a1b9a; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px;">Get Tickets</a>
          </p>
        </div>
        """

    html += """
        <hr>
        <p style="font-size: 12px; color: #999;">Sent by Concert Radar.</p>
      </body>
    </html>
    """
    return html


def send_email(to_address, subject, html_body, from_address, app_password):
    """
    Send an HTML email via Gmail SMTP.
    Returns True on success, False on failure.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_address, app_password)
            server.sendmail(from_address, to_address, msg.as_string())
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False
    