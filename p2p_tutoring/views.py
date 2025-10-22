from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def dashboard_tutor(request):
    # Sample data for demonstration
    context = {
        'upcoming_sessions': [
            {'id': 1, 'subject': 'Mathematics', 'date': '2025-10-25', 'time': '10:00 AM', 'tutee': 'John Doe', 'duration': '1 hour'},
            {'id': 2, 'subject': 'Physics', 'date': '2025-10-26', 'time': '2:00 PM', 'tutee': 'Jane Smith', 'duration': '1.5 hours'},
            {'id': 3, 'subject': 'Chemistry', 'date': '2025-10-27', 'time': '4:00 PM', 'tutee': 'Mike Johnson', 'duration': '1 hour'},
        ]
    }
    return render(request, 'dashboard_tutor.html', context)

def dashboard_tutee(request):
    # Sample data for demonstration
    context = {
        'tutors': [
            {
                'id': 1, 
                'name': 'Dr. Sarah Williams', 
                'subject': 'Mathematics', 
                'rating': 4.8, 
                'available_slots': [
                    {'date': 'Oct 25', 'time': '10:00 AM'},
                    {'date': 'Oct 25', 'time': '2:00 PM'},
                    {'date': 'Oct 26', 'time': '11:00 AM'},
                ]
            },
            {
                'id': 2, 
                'name': 'Prof. David Chen', 
                'subject': 'Physics', 
                'rating': 4.9, 
                'available_slots': [
                    {'date': 'Oct 25', 'time': '11:00 AM'},
                    {'date': 'Oct 26', 'time': '3:00 PM'},
                ]
            },
            {
                'id': 3, 
                'name': 'Ms. Emily Brown', 
                'subject': 'Chemistry', 
                'rating': 4.7, 
                'available_slots': [
                    {'date': 'Oct 25', 'time': '9:00 AM'},
                    {'date': 'Oct 26', 'time': '1:00 PM'},
                    {'date': 'Oct 27', 'time': '10:00 AM'},
                ]
            },
        ],
        'booked_sessions': [
            {'id': 1, 'tutor': 'Dr. Sarah Williams', 'subject': 'Mathematics', 'date': '2025-10-24', 'time': '10:00 AM'},
        ]
    }
    return render(request, 'dashboard_tutee.html', context)

def booking_form(request):
    # Sample available time slots for demonstration
    context = {
        'tutor_id': request.GET.get('tutor', 1),
        'tutor_name': 'Dr. Sarah Williams',
        'tutor_subject': 'Mathematics',
        'tutor_rating': 4.8,
        'hourly_rate': 25,
        'available_slots': [
            {
                'id': 1, 
                'date': 'Friday, October 25, 2025', 
                'time': '10:00 AM', 
                'end_time': '11:00 AM',
                'duration': '1 hour',
                'day_of_week': 'Friday'
            },
            {
                'id': 2, 
                'date': 'Friday, October 25, 2025', 
                'time': '2:00 PM', 
                'end_time': '3:00 PM',
                'duration': '1 hour',
                'day_of_week': 'Friday'
            },
            {
                'id': 3, 
                'date': 'Saturday, October 26, 2025', 
                'time': '11:00 AM', 
                'end_time': '12:00 PM',
                'duration': '1 hour',
                'day_of_week': 'Saturday'
            },
            {
                'id': 4, 
                'date': 'Saturday, October 26, 2025', 
                'time': '3:00 PM', 
                'end_time': '4:30 PM',
                'duration': '1.5 hours',
                'day_of_week': 'Saturday'
            },
            {
                'id': 5, 
                'date': 'Monday, October 28, 2025', 
                'time': '9:00 AM', 
                'end_time': '10:00 AM',
                'duration': '1 hour',
                'day_of_week': 'Monday'
            },
        ]
    }
    return render(request, 'booking_form.html', context)

def session_manage(request):
    # Sample data for demonstration
    context = {
        'upcoming_sessions': [
            {'id': 1, 'subject': 'Mathematics', 'date': '2025-10-25', 'time': '10:00 AM', 'participant': 'John Doe', 'status': 'Confirmed'},
            {'id': 2, 'subject': 'Physics', 'date': '2025-10-26', 'time': '2:00 PM', 'participant': 'Jane Smith', 'status': 'Confirmed'},
        ],
        'past_sessions': [
            {'id': 3, 'subject': 'Chemistry', 'date': '2025-10-15', 'time': '4:00 PM', 'participant': 'Mike Johnson', 'status': 'Completed'},
        ],
        'cancelled_sessions': [
            {'id': 4, 'subject': 'Biology', 'date': '2025-10-20', 'time': '11:00 AM', 'participant': 'Sarah Lee', 'status': 'Cancelled'},
        ]
    }
    return render(request, 'session_manage.html', context)

def profile(request):
    return render(request, 'profile.html')
