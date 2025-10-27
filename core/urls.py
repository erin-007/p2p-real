from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/tutee/', views.dashboard_tutee, name='dashboard_tutee'),
    path('dashboard/tutor/', views.dashboard_tutor, name='dashboard_tutor'),
    path('profile/', views.profile_view, name='profile'),
    path('book/', views.book_session, name='book_session'),
    path('sessions/manage/', views.manage_sessions, name='manage_sessions'),
]
