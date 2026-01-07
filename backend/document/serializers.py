from rest_framework import serializers
from .models import Note

"""
This serializer defines how Note model instances are converted to and from JSON 
for the API using Django REST Framework.

- Serializes Note objects so they can be sent as JSON responses to the frontend.
- Deserializes incoming JSON data from API requests into Note model instances 
  for creating or updating notes in the database.
- Specifies the fields to include: id, title, content, category, created_at, and modified_at.

In short, it ensures proper validation, conversion, and communication of Note data 
between the backend and frontend.
"""

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'category', 'created_at', 'modified_at']
