# core/admin.py
from django.contrib import admin
from .models import Slot, Booking

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'date', 'time', 'is_booked')
    list_filter = ('tutor', 'date', 'is_booked')
    search_fields = ('title', 'tutor__username')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('slot_title', 'tutor_name', 'tutee', 'booked_at')
    list_filter = ('booked_at',)
    search_fields = ('slot__title', 'tutee__username', 'slot__tutor__username')

    def slot_title(self, obj):
        return obj.slot.title
    slot_title.short_description = 'Slot Title'

    def tutor_name(self, obj):
        return obj.slot.tutor.username
    tutor_name.short_description = 'Tutor'
