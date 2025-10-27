from django.core.mail import send_mail
from django.conf import settings

def send_booking_email(booking):
    subject = f"New session booked by {booking.tutee.username}"
    message = f"You have a new session booked on {booking.booked_at}."
    recipient_list = [booking.tutor.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
