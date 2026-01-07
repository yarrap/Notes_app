from django.contrib import admin
from .models import Note

"""
Registers the Note model with the Django admin site,
allowing admins to view, add, edit, and delete notes
through the Django admin interface.
"""

admin.site.register(Note)