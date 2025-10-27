from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm, BookingForm
from .models import Booking
from .utils import send_booking_email
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard_tutee')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard_tutee')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_tutee(request):
    bookings = Booking.objects.filter(tutee=request.user)
    return render(request, 'dashboard_tutee.html', {'bookings': bookings})

@login_required
def dashboard_tutor(request):
    bookings = Booking.objects.filter(tutor=request.user)
    return render(request, 'dashboard_tutor.html', {'bookings': bookings})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def book_session(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tutee = request.user
            booking.save()
            send_booking_email(booking)  # send email to tutor
            messages.success(request, "Booking successful!")
            return redirect('dashboard_tutee')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})

@login_required
def manage_sessions(request):
    if request.user.is_staff:
        bookings = Booking.objects.all()
        return render(request, 'session_manage.html', {'bookings': bookings})
    return redirect('dashboard_tutee')
