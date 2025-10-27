# core/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, SessionBooking
from django.urls import reverse
from datetime import date, time, timedelta

class RegistrationLoginTests(TestCase):
    def test_register_creates_profile(self):
        resp = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 't@example.com',
            'role': 'tutee',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertEqual(resp.status_code, 302)  # redirect to login
        user = User.objects.get(username='testuser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.role, 'tutee')

class BookingCollisionTests(TestCase):
    def setUp(self):
        self.tutor = User.objects.create_user('tutor1', password='pass12345')
        Profile.objects.create(user=self.tutor, full_name='Tutor One', role='tutor')
        self.tutee = User.objects.create_user('tutee1', password='pass12345')
        Profile.objects.create(user=self.tutee, full_name='Tutee One', role='tutee')

    def test_prevent_double_booking(self):
        d = date.today() + timedelta(days=1)
        t = time(10, 0)
        SessionBooking.objects.create(tutor=self.tutor, tutee=self.tutee, subject='Math', date=d, time=t)
        # attempt duplicate
        with self.assertRaises(Exception):
            SessionBooking.objects.create(tutor=self.tutor, tutee=self.tutee, subject='Math', date=d, time=t)
