# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Slot(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slots')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    max_students = models.PositiveSmallIntegerField(default=1)  # future-proofing

    def __str__(self):
        return f"{self.title} - {self.tutor.username} - {self.date} {self.time}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    tutee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='booked')

    def __str__(self):
        return f"{self.slot.title} booked by {self.tutee.username}"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('tutee', 'Tutee'),
        ('tutor', 'Tutor'),
        ('both', 'Both'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tutee')
    is_verified = models.BooleanField(default=False)  # email verification flag
    verification_token = models.CharField(max_length=64, blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# Signals to auto-create/update Profile when User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # ensure profile exists for old users / migrations
        Profile.objects.get_or_create(user=instance)

import secrets

#@receiver(post_save, sender=User)
#def create_or_update_user_profile(sender, instance, created, **kwargs):
    #from core.models import Profile
    #if created:
        #profile = Profile.objects.create(user=instance)
        #profile.verification_token = secrets.token_hex(16)
        #profile.save()
    #else:
        #Profile.objects.get_or_create(user=instance)
