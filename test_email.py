import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p2p_tutoring.settings')  # replace tutorapp with your project folder
django.setup()

from django.core.mail import send_mail

def send_test_email():
    send_mail(
    'Test Subject',
    'This is a test message.',
    'mailmejoe.momo@gmail.com',   # <-- must exactly match EMAIL_HOST_USER
    ['erinjoseph.ej@gmail.com'],
    fail_silently=False,
)

    
    print("Email sent!")

if __name__ == "__main__":
    send_test_email()

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2PTutorFrontend.settings')  # change to your settings module
django.setup()

from django.core.mail import send_mail

def send_test_email():
    try:
        send_mail(
            subject='Test Email from Django',
            message='This is a test email to check if Django can send emails.',
            from_email='mailmejoe.momo@gmail.com',  # your Gmail
            recipient_list=['recipient@gmail.com'],  # test recipient
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

send_test_email()
