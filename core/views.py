from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
import secrets

from .forms import RegisterForm
from .models import Slot, Booking, Profile
from .utils import send_booking_email, send_welcome_email, send_verification_email


# -----------------------------
# Home Page
# -----------------------------
def home(request):
    slots = Slot.objects.filter(is_booked=False).order_by('date', 'time')[:20]
    return render(request, 'home.html', {'slots': slots})


# -----------------------------
# Registration with Email Verification
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['full_name'].split(" ")[0],
                last_name=" ".join(form.cleaned_data['full_name'].split(" ")[1:]),
            )

            # ⚠️ DO NOT manually create Profile here if your post_save signal already does it
            # If your signal creates profile automatically, skip this:
            # Profile.objects.create(user=user)

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



# -----------------------------
# Email Verification View
# -----------------------------
def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
        profile.is_verified = True
        profile.verification_token = None
        profile.save()
        return render(request, "email_verified.html", {"success": True})
    except Profile.DoesNotExist:
        return render(request, "email_verified.html", {"success": False})


# -----------------------------
# Login / Logout
# -----------------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Skip email verification check
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard_tutee')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')

    return render(request, 'login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# -----------------------------
# Tutee Dashboard
# -----------------------------
@login_required
def dashboard_tutee(request):
    bookings = Booking.objects.filter(tutee=request.user).order_by('-booked_at')
    tutors = User.objects.exclude(id=request.user.id)[:20]
    return render(request, 'dashboard_tutee.html', {
        'bookings': bookings,
        'tutors': tutors,
    })


# -----------------------------
# Tutor Dashboard
# -----------------------------
@login_required
def dashboard_tutor(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description', '')

        if subject and date and time:
            try:
                Slot.objects.create(
                    tutor=request.user,
                    title=subject,
                    description=description,
                    date=date,
                    time=time,
                )
                messages.success(request, "Session added.")
                return redirect('dashboard_tutor')
            except Exception as e:
                messages.error(request, f"Could not add session: {e}")
        else:
            messages.error(request, "Please provide subject, date, and time.")

    upcoming_bookings = Booking.objects.filter(slot__tutor=request.user).order_by('slot__date', 'slot__time')
    upcoming_sessions = [{
        'subject': b.slot.title,
        'date': b.slot.date,
        'time': b.slot.time,
        'duration': '1 hour',
        'tutee': b.tutee.username,
        'id': b.id,
    } for b in upcoming_bookings]

    my_slots = Slot.objects.filter(tutor=request.user).order_by('date', 'time')

    return render(request, 'dashboard_tutor.html', {
        'upcoming_sessions': upcoming_sessions,
        'my_slots': my_slots,
    })


# -----------------------------
# Profile View
# -----------------------------
@login_required
def profile_view(request):
    return render(request, 'profile.html')


# -----------------------------
# Booking Flow
# -----------------------------
@login_required
def booking_form(request):
    tutor_id = request.GET.get('tutor') or request.POST.get('tutor') or None
    if tutor_id:
        tutor = get_object_or_404(User, id=int(tutor_id))
    else:
        tutor = User.objects.exclude(id=request.user.id).first()

    available_slots = Slot.objects.filter(tutor=tutor, is_booked=False).order_by('date', 'time')
    slots_context = [{
        'id': s.id,
        'date': s.date.strftime('%A, %B %d, %Y'),
        'time': s.time.strftime('%I:%M %p'),
        'duration': '1 hour',
        'day_of_week': s.date.strftime('%A'),
    } for s in available_slots]

    if request.method == 'POST':
        slot_id = request.POST.get('time_slot')
        topic = request.POST.get('topic', '')
        meeting_type = request.POST.get('meeting_type', 'online')
        notes = request.POST.get('notes', '')
        if not slot_id:
            messages.error(request, "Please pick a time slot.")
            return redirect(request.path + f"?tutor={tutor.id}")

        slot = get_object_or_404(Slot, id=int(slot_id))

        try:
            with transaction.atomic():
                slot_ref = Slot.objects.select_for_update().get(id=slot.id)
                if slot_ref.is_booked:
                    messages.error(request, "Sorry, this slot was just booked by someone else.")
                    return redirect('booking_form')
                booking = Booking.objects.create(slot=slot_ref, tutee=request.user)
                slot_ref.is_booked = True
                slot_ref.save(update_fields=['is_booked'])
        except Exception as e:
            messages.error(request, f"Booking failed: {e}")
            return redirect('booking_form')

        try:
            send_booking_email(booking, topic=topic, meeting_type=meeting_type, notes=notes)
        except Exception:
            pass

        messages.success(request, "Booking confirmed — emails sent.")
        return redirect('dashboard_tutee')

    return render(request, 'booking_form.html', {
        'available_slots': slots_context,
        'tutor_id': tutor.id if tutor else None,
        'tutor_name': f"{tutor.first_name} {tutor.last_name}".strip() or tutor.username if tutor else 'Tutor',
        'tutor_subject': 'Subject',
        'tutor_rating': 4.8,
        'hourly_rate': 25,
    })


# -----------------------------
# Session Management
# -----------------------------
@login_required
def session_manage(request):
    upcoming = Booking.objects.filter(tutee=request.user, slot__date__gte=datetime.today().date()).order_by('slot__date')
    past = Booking.objects.filter(tutee=request.user, slot__date__lt=datetime.today().date()).order_by('-slot__date')

    upcoming_sessions = [{
        'id': b.id,
        'subject': b.slot.title,
        'date': b.slot.date,
        'time': b.slot.time,
        'participant': b.slot.tutor.username,
        'status': 'Confirmed'
    } for b in upcoming]

    past_sessions = [{
        'id': b.id,
        'subject': b.slot.title,
        'date': b.slot.date,
        'time': b.slot.time,
        'participant': b.slot.tutor.username,
        'status': 'Completed'
    } for b in past]

    return render(request, 'session_manage.html', {
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
        'cancelled_sessions': [],
    })
