"""
URL configuration for the notes_app_project Django backend.

This file defines all API routes exposed by the Django application.
The backend is API-only and is designed to be consumed by a Next.js frontend.

Included endpoints:
- Authentication APIs (login, register)
- CSRF cookie endpoint for secure session-based auth
- Note APIs (create, read, update, delete)
- Django admin panel

All endpoints return JSON responses.
No Django template-rendered (HTML) views are used in this project.
"""

from django.contrib import admin
from django.urls import path
from document.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', api_login, name='api-login'),
    path('api/register/', api_register, name='api-register'),
    path('csrf-cookie/', csrf, name='csrf-cookie'),
    path('api/notes/', api_notes, name='api-notes'),
    path('api/add-note/', api_add_note, name='api-add-note'),
    path('api/update-note/<int:note_id>/', update_note, name='update_note'),
    path('api/delete-note/<int:note_id>/', api_delete_note, name='api_delete_note'),
   
]
