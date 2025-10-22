"""
URL configuration for p2p_tutoring project.
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/tutor/', views.dashboard_tutor, name='dashboard_tutor'),
    path('dashboard/tutee/', views.dashboard_tutee, name='dashboard_tutee'),
    path('booking/', views.booking_form, name='booking_form'),
    path('sessions/', views.session_manage, name='session_manage'),
    path('profile/', views.profile, name='profile'),
]
