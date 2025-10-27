# core/models.py (keep what you have)
from django.db import models
from django.contrib.auth.models import User

class Slot(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slots')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.tutor.username} - {self.date} {self.time}"

class Booking(models.Model):
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    tutee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.slot.title} booked by {self.tutee.username}"
