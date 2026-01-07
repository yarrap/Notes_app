"""
URL configuration for the notes_app_project Django project.

This file maps URLs to their corresponding views for both:
1. Web-based views (rendered HTML pages)
2. API endpoints (JSON responses) used by the frontend (Next.js)

It also includes authentication endpoints and a CSRF endpoint for secure API requests.
"""

from django.contrib import admin
from django.urls import path
from document.views import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json


def api_login(request):
    """
    Handles API login requests.
    - Accepts POST with 'username' and 'password'.
    - Authenticates user and returns JSON success status.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return JsonResponse({'success': False, 'error': 'POST request required'})


def api_register(request):
    """
    Handles API registration requests.
    - Accepts POST with 'username' and 'password'.
    - Creates a new user if the username is not taken.
    - Returns JSON success or error message.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'POST request required'})


@ensure_csrf_cookie
def csrf(request):
    """
    Simple endpoint to set a CSRF cookie for secure API requests.
    """
    return JsonResponse({'csrfToken': 'CSRF cookie set'})

# ------------------- URL PATTERNS -------------------

urlpatterns = [
    # ------------------- Web Views -------------------
    path('login/' , login_page, name='login'),
    path('register/', register_page, name='register'),
    path('custom_logout/' ,custom_logout, name='logout'),
    path('', editor, name='editor'),
    path('delete_note/<int:docid>/', delete_note, name='delete_note'),
    path('admin/', admin.site.urls),
    
    # ------------------- API Endpoints -------------------
    path('api/login/', api_login, name='api-login'),
    path('api/register/', api_register, name='api-register'),
    path('csrf-cookie/', csrf, name='csrf-cookie'),
    path('api/notes/', api_notes, name='api-notes'),
    path('api/add-note/', api_add_note, name='api-add-note'),
    path('api/update-note/<int:note_id>/', update_note, name='update_note'),
    path('api/delete-note/<int:note_id>/', api_delete_note, name='api_delete_note'),
   
]
