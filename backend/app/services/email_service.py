import smtplib
from email.message import EmailMessage
from app.core.config import get_settings

settings = get_settings()


# ------------------------------------------------
# ADMIN EMAIL (used in admin panel)
# ------------------------------------------------
def send_admin_email(recipient_email: str, subject: str, message_body: str):

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.ADMIN_EMAIL
    msg["To"] = recipient_email

    msg.set_content(message_body)

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.ADMIN_EMAIL, settings.ADMIN_EMAIL_PASSWORD)
        server.send_message(msg)


# ------------------------------------------------
# PASSWORD RESET EMAIL
# ------------------------------------------------
def send_reset_email(recipient_email: str, reset_link: str):

    msg = EmailMessage()

    msg["Subject"] = "Reset Your Password"
    msg["From"] = settings.ADMIN_EMAIL
    msg["To"] = recipient_email

    msg.set_content(f"""
Hello,

We received a request to reset your password.

Click the link below to reset it:

{reset_link}

This link will expire in 1 hour.

If you did not request a password reset, you can safely ignore this email.

Best regards,
AI Hiring System
""")

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.ADMIN_EMAIL, settings.ADMIN_EMAIL_PASSWORD)
        server.send_message(msg)