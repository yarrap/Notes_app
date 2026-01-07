from .models import Note
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from django.views.decorators.csrf import ensure_csrf_cookie
import json

"""
API views for the Note-Taking application.

This module exposes JSON-based REST-style endpoints used by a Next.js frontend.
There are no Django template-rendered views in this file.

Features handled here:
- User authentication (register, login) via API
- CRUD operations for notes (create, read, update, delete)
- User-specific note access
- CSRF support for secure frontend-backend communication

All responses are JSON.
Authentication is session-based and enforced where required.
"""

@csrf_exempt
def api_delete_note(request, note_id):
    """
    Deletes a note by its ID.
    - Only accepts DELETE requests.
    - Returns JSON with success or error message.
    """
    if request.method == "DELETE":
        try:
            note = Note.objects.get(id=note_id, user=request.user)
            note.delete()
            return JsonResponse({"success": True})
        except Note.DoesNotExist:
            return JsonResponse({"error": "Note not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=405)


@csrf_exempt
def update_note(request, note_id):
    """
    Updates a note by its ID.
    - Only accepts PUT requests.
    - Parses JSON body from the request to update title, content, or category.
    - Returns the updated note as JSON.
    """
    if request.method == "PUT":
        try:
            # Get the note
            note = Note.objects.get(id=note_id, user=request.user)
            
            # Parse the request body
            data = json.loads(request.body)
            
            # Update the note fields
            note.title = data.get('title', note.title)
            note.content = data.get('content', note.content)
            note.category = data.get('category', note.category)
            note.save()
            
            # Return the updated note
            return JsonResponse({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'category': note.category,
                'modified_at': note.modified_at.isoformat()
            })
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def api_notes(request):
    """
    Returns a list of notes for the logged-in user.
    - Returns JSON data including id, title, content, category, created_at, modified_at.
    """
    notes = Note.objects.filter(user=request.user).values("id", "title", "content", "category", "created_at", "modified_at")
    return JsonResponse(list(notes), safe=False)
 

@csrf_exempt
@login_required
def api_add_note(request):
    """
    Creates a new note for the logged-in user.
    - Only accepts POST requests.
    - Parses JSON data for title, content, and category.
    - Returns JSON with the created note's data.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        note = Note.objects.create(
            user=request.user,
            title=data.get("title", ""),
            content=data.get("content", ""),
            category=data.get("category", "personal")
        )
        return JsonResponse({"id": note.id, "title": note.title, "content": note.content})
    return JsonResponse({"error": "POST request required"}, status=405)
 

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


@ensure_csrf_cookie
def csrf(request):
    """
    Simple endpoint to set a CSRF cookie for secure API requests.
    """
    return JsonResponse({'csrfToken': 'CSRF cookie set'})


