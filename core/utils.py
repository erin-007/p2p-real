# core/utils.py
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Configure Brevo API
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')

# Function to send email through Brevo
def send_email(to_email, subject, html_content):
    try:
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        sender = {"name": "P2P Tutoring Scheduler", "email": "noreply@p2ptutor.com"}  # customize sender
        to = [{"email": to_email}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("✅ Email sent:", api_response)
        return True
    except ApiException as e:
        print("❌ Email sending failed:", e)
        return False

# Send welcome email
def send_welcome_email(user):
    subject = "Welcome to P2P Tutoring Scheduler"
    html_content = f"""
    <html>
    <body>
        <h2>Hi {user.username},</h2>
        <p>Thanks for signing up for <b>P2P Tutoring Scheduler</b>!</p>
        <p>We’re excited to have you onboard.</p>
    </body>
    </html>
    """
    send_email(user.email, subject, html_content)

# Send booking email
def send_booking_email(booking, topic="", meeting_type="online", notes=""):
    tutor_email = booking.slot.tutor.email
    tutee_email = booking.tutee.email
    subject = f"Booking confirmed: {booking.slot.title}"

    html_content = f"""
    <html>
    <body>
        <h3>Booking Confirmed</h3>
        <p><b>Tutor:</b> {booking.slot.tutor.username}</p>
        <p><b>Tutee:</b> {booking.tutee.username}</p>
        <p><b>Date:</b> {booking.slot.date} {booking.slot.time}</p>
        <p><b>Topic:</b> {topic}</p>
        <p><b>Meeting Type:</b> {meeting_type}</p>
        <p><b>Notes:</b> {notes}</p>
        <p>Please be on time.</p>
    </body>
    </html>
    """

    send_email(tutor_email, subject, html_content)
    send_email(tutee_email, subject, html_content)

from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    """
    Sends a dummy verification email (console-based since no Gmail or SMTP is used).
    """
    verification_link = f"http://localhost:8000/verify/{user.profile.verification_token}/"
    subject = "Verify Your Email"
    message = f"Hello {user.username},\n\nPlease verify your account by clicking the link below:\n{verification_link}\n\nThank you!"
    
    # If email backend is console, this just prints in the terminal
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
