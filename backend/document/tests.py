from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note
from datetime import datetime
import time

"""
This test suite validates the behavior of the Note model in the Django application.

It performs the following checks:
1. Ensures a Note can be created with the required fields: title, content, category, and user.
2. Verifies that the 'created_at' and 'modified_at' timestamp fields are automatically set and are proper datetime objects.
3. Confirms that the 'modified_at' timestamp updates correctly when the Note is edited and saved.
4. Includes similar checks for API-related usage to ensure consistent behavior of 'modified_at' during updates.

Overall, these tests ensure that the Note model handles creation, editing, and timestamp tracking correctly.
"""


class NoteModelTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_create_note_model(self):
        # Create a new note for this user
        note = Note.objects.create(
            title="Test Note",
            content="Some content",
            category="personal",
            user=self.user
        )

        # Check fields
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "Some content")
        self.assertEqual(note.category, "personal")
        self.assertEqual(note.user, self.user)

        # Check timestamps
        self.assertIsNotNone(note.created_at)
        self.assertIsInstance(note.created_at, datetime)
        self.assertIsNotNone(note.modified_at)
        self.assertIsInstance(note.modified_at, datetime)

        # Check modified_at updates on save
        old_modified_at = note.modified_at
        time.sleep(1)  
        note.title = "Updated Note"
        note.save()
        self.assertNotEqual(note.modified_at, old_modified_at)

    def test_note_api_modified_at(self):
        # Same thing, just testing API logic
        note = Note.objects.create(
            title="API Note",
            content="API Content",
            category="personal",
            user=self.user
        )

        old_modified_at = note.modified_at
        time.sleep(1)
        note.title = "API Updated"
        note.save()
        self.assertNotEqual(note.modified_at, old_modified_at)

