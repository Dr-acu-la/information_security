#!/usr/bin/env python3
"""
notify_owner.py - email a short status note to the server owner (yourself).

Credentials are read from environment variables, NEVER hard-coded, so the
script can be shared or committed safely:

    export SMTP_USER="you@gmail.com"
    export SMTP_PASS="your_app_password"   # a Gmail App Password, not your login
    export OWNER_EMAIL="you@gmail.com"

For Gmail, create an App Password (Google Account -> Security -> App passwords);
a normal account password will not work with SMTP.
"""
import os
import smtplib
import ssl
import datetime
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def main():
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    owner = os.environ.get("OWNER_EMAIL", user)

    if not user or not password:
        raise SystemExit("Set SMTP_USER and SMTP_PASS environment variables first.")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = owner
    msg["Subject"] = f"Server status report - {now}"
    msg.set_content(f"Automated check-in from your server at {now}. All running.")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(user, password)
        server.send_message(msg)

    print(f"Status email sent to {owner} at {now}")


if __name__ == "__main__":
    main()
