from django.db import models
from django.contrib.auth.models import User
 

"""
Defines the Note model for the Note-Taking application.

Fields:
- user: Links the note to a specific user (ForeignKey to Django's User model).
- title: The title of the note (max 255 characters).
- content: The main text/content of the note (optional).
- category: The category of the note, with predefined choices 
  ('random', 'personal', 'school', 'drama'); defaults to 'personal'.
- created_at: Timestamp automatically set when the note is created.
- modified_at: Timestamp automatically updated whenever the note is modified.

Meta:
- Orders notes by title by default when querying the database.

This model is the core data structure for storing and managing notes 
for each user in the application.
"""


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('random', 'Random Thoughts'),
        ('personal', 'Personal'),
        ('school', 'School'),
        ('drama', 'Drama Categories'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='personal'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
 
    class Meta:
        ordering = ('title',)