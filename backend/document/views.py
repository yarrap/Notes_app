from django.shortcuts import render, redirect
from .models import Note
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
import json


"""
This module contains all the views and API endpoints for the Note-Taking application.

It includes:

1. **API Endpoints (JSON-based)**
   - `get_notes`: Returns all notes as JSON, ordered by creation date.
   - `api_notes`: Returns notes for the logged-in user.
   - `api_add_note`: Creates a new note for the logged-in user.
   - `update_note`: Updates an existing note by ID.
   - `api_delete_note`: Deletes a note by ID.

2. **Web Views (HTML-based)**
   - `editor`: Renders the note editor page, supports creating or updating notes.
   - `delete_note`: Deletes a note and redirects to homepage.
   - `login_page`: Handles user login with authentication and error messages.
   - `register_page`: Handles user registration and account creation.
   - `custom_logout`: Logs out the user and redirects to login page.

Overall, this file manages all interactions between the frontend and backend, 
handling note creation, updating, deletion, retrieval, and user authentication.
It ensures both API-based and template-based access to notes while enforcing 
user login where required.
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
            note = Note.objects.get(id=note_id)
            note.delete()
            return JsonResponse({"success": True})
        except Note.DoesNotExist:
            return JsonResponse({"error": "Note not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


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
                'modified_at': note.created_at.isoformat()
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
    return JsonResponse({"error": "POST request required"}, status=400)


@login_required(login_url='/login/')
def editor(request):
    """
    Renders the note editor page.
    - Supports viewing a note if docid is provided.
    - Handles creating new notes or updating existing notes via POST requests.
    - Passes the list of all notes and current note to the template context.
    """
    docid = int(request.GET.get('docid', 0))
    notes = Note.objects.all()
 
    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        category = request.POST.get('category') 
 
        if docid > 0:
            note = Note.objects.get(pk=docid)
            note.title = title
            note.content = content
            note.category = category 
            note.save()
 
            return redirect('/?docid=%i' % docid)
        else:
            note = Note.objects.create(title=title, content=content)
 
            return redirect('/?docid=%i' % note.id)
 
    if docid > 0:
        note = Note.objects.get(pk=docid)
    else:
        note = ''
 
    context = {
        'docid': docid,
        'notes': notes,
        'note': note
    }
 
    return render(request, 'editor.html', context)
 
 
@login_required(login_url='/login/')
def delete_note(request, docid):
    """
    Deletes a note by its primary key (docid).
    - Redirects to the homepage with docid=0 after deletion.
    """
    note = Note.objects.get(pk=docid)
    note.delete()
 
    return redirect('/?docid=0')
 

@api_view(['GET'])
def get_notes(request):
    """
    Returns a list of all notes in the system, ordered by newest first.
    Uses the NoteSerializer to convert Note objects to JSON for API response.
    """
    notes = Note.objects.all().order_by('-created_at')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


def login_page(request):
    """
    Handles user login.
    - POST request authenticates the user.
    - GET request renders the login page.
    - Provides error messages for invalid username or password.
    """
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "Username not found")
                return redirect('/login/')
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('editor')
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    return render(request, "login.html")
 
 
def register_page(request):
    """
    Handles user registration.
    - POST request creates a new user if username is available.
    - GET request renders the registration page.
    - Sets password securely and provides success/error messages.
    """
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")
 
 
def custom_logout(request):
    """
    Logs out the currently logged-in user and redirects to login page.
    """
    logout(request)
    return redirect('login')