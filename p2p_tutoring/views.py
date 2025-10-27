# p2p_tutoring/views.py
from django.shortcuts import redirect
# simple redirects — actual logic is in core.views
def home(request):
    from django.shortcuts import redirect
    return redirect('home_core')

def login_view(request):
    from django.shortcuts import redirect
    return redirect('login_core')

def register(request):
    from django.shortcuts import redirect
    return redirect('register_core')

def dashboard_tutor(request):
    from django.shortcuts import redirect
    return redirect('dashboard_tutor_core')

def dashboard_tutee(request):
    from django.shortcuts import redirect
    return redirect('dashboard_tutee_core')

def booking_form(request):
    from django.shortcuts import redirect
    return redirect('booking_form_core')

def session_manage(request):
    from django.shortcuts import redirect
    return redirect('session_manage_core')

def profile(request):
    from django.shortcuts import redirect
    return redirect('profile_core')# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, SessionBookingForm
from .models import Profile, SessionBooking
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                messages.error(request, 'Profile missing; contact admin.')
                return redirect('login')

            # enforce role selection if provided
            if role and profile.role != role and profile.role != 'both':
                messages.error(request, 'You cannot log in as this role.')
                return redirect('login')

            login(request, user)
            if profile.role == 'tutor':
                return redirect('dashboard_tutor')
            return redirect('dashboard_tutee')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_tutor(request):
    profile = request.user.profile
    if profile.role not in ('tutor', 'both'):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_tutee')
    sessions = SessionBooking.objects.filter(tutor=request.user).order_by('date', 'time')
    return render(request, 'dashboard_tutor.html', {'upcoming_sessions': sessions})


@login_required
def dashboard_tutee(request):
    profile = request.user.profile
    # simple tutors list for search (you can replace with filtering)
    tutors = Profile.objects.filter(role__in=['tutor', 'both'])
    booked = SessionBooking.objects.filter(tutee=request.user).order_by('date', 'time')
    return render(request, 'dashboard_tutee.html', {'tutors': tutors, 'booked_sessions': booked})


@login_required
def booking_form(request):
    # booking via form POST
    if request.method == 'POST':
        form = SessionBookingForm(request.POST)
        if form.is_valid():
            try:
                # atomic block to avoid race conditions on unique_together
                with transaction.atomic():
                    booking = form.save()
                messages.success(request, 'Booking successful.')
                return redirect('dashboard_tutee')
            except IntegrityError:
                form.add_error(None, 'Selected time slot is no longer available.')
    else:
        # prefill form if tutor param provided
        initial = {}
        tutor_id = request.GET.get('tutor')
        if tutor_id:
            initial['tutor'] = tutor_id
        form = SessionBookingForm(initial=initial)
    return render(request, 'booking_form.html', {'form': form})


@login_required
def session_manage(request):
    # show sessions for the logged-in user (tutor or tutee)
    if request.user.profile.role in ('tutor', 'both'):
        upcoming = SessionBooking.objects.filter(tutor=request.user).order_by('date', 'time')
    else:
        upcoming = SessionBooking.objects.filter(tutee=request.user).order_by('date', 'time')
    return render(request, 'session_manage.html', {'upcoming_sessions': upcoming})


@login_required
def profile(request):
    # minimal profile view/edit placeholder
    if request.method == 'POST':
        profile = request.user.profile
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.subjects = request.POST.get('subjects', profile.subjects)
        profile.save()
        messages.success(request, 'Profile updated.')
        return redirect('profile')
    return render(request, 'profile.html')
