from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth routes
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Email verification
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),

    # Dashboards
    path('dashboard/tutee/', views.dashboard_tutee, name='dashboard_tutee'),
    path('dashboard/tutor/', views.dashboard_tutor, name='dashboard_tutor'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Booking
    path('book/', views.booking_form, name='booking_form'),

    # Sessions
    path('sessions/manage/', views.session_manage, name='session_manage'),
]
