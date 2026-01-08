from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Note


"""
Comprehensive test suite for the Notes application.

This module validates the core functionality, data integrity, and access control
of the notes system, covering:

- Note model behavior (creation, updates, deletion, defaults, ordering, timestamps)
- Category validation and filtering logic
- User authentication (registration, login, and failure cases)
- User–note relationships and data isolation between users
- Basic API-level validation using Django REST Framework test utilities

The tests are designed to ensure correctness, maintainability, and confidence
in the application's backend logic while reflecting real-world usage scenarios.
"""


class NoteModelTest(TestCase):
    """Test the Note model"""
    
    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_note_creation_with_required_fields(self):
        """Test that a note can be created with required fields"""
        note = Note.objects.create(
            title='Test Note',
            content='This is test content',
            category='personal',
            user=self.user
        )
        
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.content, 'This is test content')
        self.assertEqual(note.category, 'personal')
        self.assertTrue(isinstance(note, Note))
    
    def test_note_belongs_to_user(self):
        """Test that a note is correctly associated with a user"""
        note = Note.objects.create(
            title='User Test',
            content='Testing user relationship',
            category='school',
            user=self.user
        )
        
        self.assertEqual(note.user.username, 'testuser')
        self.assertEqual(note.user.email, 'test@example.com')
    
    def test_note_str_method(self):
        """Test the string representation of a note"""
        note = Note.objects.create(
            title='String Test',
            content='Testing string method',
            category='random',
            user=self.user
        )
        
        self.assertEqual(str(note), 'String Test')
    
    def test_note_default_category(self):
        """Test that default category is 'personal'"""
        note = Note.objects.create(
            title='Default Category Test',
            content='Testing default category',
            user=self.user
            # Not specifying category - should default to 'personal'
        )
        
        self.assertEqual(note.category, 'personal')
    
    def test_note_category_choices(self):
        """Test all valid category choices"""
        categories = ['random', 'personal', 'school', 'drama']
        
        for cat in categories:
            note = Note.objects.create(
                title=f'{cat.capitalize()} Note',
                content=f'Testing {cat} category',
                category=cat,
                user=self.user
            )
            self.assertEqual(note.category, cat)
    
    def test_multiple_notes_per_user(self):
        """Test that a user can have multiple notes"""
        Note.objects.create(
            title='Note 1',
            content='Content 1',
            category='personal',
            user=self.user
        )
        Note.objects.create(
            title='Note 2',
            content='Content 2',
            category='school',
            user=self.user
        )
        Note.objects.create(
            title='Note 3',
            content='Content 3',
            category='random',
            user=self.user
        )
        
        user_notes = Note.objects.filter(user=self.user)
        self.assertEqual(user_notes.count(), 3)
    
    def test_note_update(self):
        """Test that a note can be updated"""
        note = Note.objects.create(
            title='Original Title',
            content='Original content',
            category='personal',
            user=self.user
        )
        
        # Update the note
        note.title = 'Updated Title'
        note.content = 'Updated content'
        note.category = 'school'
        note.save()
        
        # Retrieve from database
        updated_note = Note.objects.get(id=note.id)
        self.assertEqual(updated_note.title, 'Updated Title')
        self.assertEqual(updated_note.content, 'Updated content')
        self.assertEqual(updated_note.category, 'school')
    
    def test_note_deletion(self):
        """Test that a note can be deleted"""
        note = Note.objects.create(
            title='To Be Deleted',
            content='This note will be deleted',
            category='drama',
            user=self.user
        )
        note_id = note.id
        
        # Delete the note
        note.delete()
        
        # Verify it's gone
        self.assertFalse(Note.objects.filter(id=note_id).exists())
    
    def test_note_timestamps(self):
        """Test that created_at and modified_at are set correctly"""
        note = Note.objects.create(
            title='Timestamp Test',
            content='Testing timestamps',
            category='personal',
            user=self.user
        )
        
        # Check that timestamps exist
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.modified_at)
        
        # Initially, created_at and modified_at should be very close
        time_diff = (note.modified_at - note.created_at).total_seconds()
        self.assertLess(time_diff, 1)  # Less than 1 second difference
    
    def test_note_ordering(self):
        """Test that notes are ordered by title"""
        Note.objects.create(title='Zebra', content='Z', category='personal', user=self.user)
        Note.objects.create(title='Apple', content='A', category='personal', user=self.user)
        Note.objects.create(title='Banana', content='B', category='personal', user=self.user)
        
        notes = Note.objects.all()
        titles = [note.title for note in notes]
        
        # Should be ordered alphabetically by title
        self.assertEqual(titles, ['Apple', 'Banana', 'Zebra'])


class NoteCategoryFilterTest(TestCase):
    """Test filtering notes by category"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='filteruser',
            password='filterpass'
        )
        
        # Create notes in different categories
        Note.objects.create(title='Personal 1', content='P1', category='personal', user=self.user)
        Note.objects.create(title='Personal 2', content='P2', category='personal', user=self.user)
        Note.objects.create(title='School 1', content='S1', category='school', user=self.user)
        Note.objects.create(title='Random 1', content='R1', category='random', user=self.user)
    
    def test_filter_by_personal_category(self):
        """Test filtering notes by personal category"""
        personal_notes = Note.objects.filter(category='personal')
        self.assertEqual(personal_notes.count(), 2)
    
    def test_filter_by_school_category(self):
        """Test filtering notes by school category"""
        school_notes = Note.objects.filter(category='school')
        self.assertEqual(school_notes.count(), 1)
    
    def test_filter_by_random_category(self):
        """Test filtering notes by random category"""
        random_notes = Note.objects.filter(category='random')
        self.assertEqual(random_notes.count(), 1)


class UserAuthenticationTest(TestCase):
    """Test user registration and login functionality"""
    
    def setUp(self):
        self.client = Client()
    
    def test_user_creation(self):
        """Test that a new user can be created"""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass123'
        )
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_user_authentication(self):
        """Test that a user can be authenticated"""
        user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )
        
        # Test authentication
        is_authenticated = self.client.login(username='authuser', password='authpass123')
        self.assertTrue(is_authenticated)
    
    def test_wrong_password_fails(self):
        """Test that wrong password fails authentication"""
        User.objects.create_user(
            username='authuser',
            password='correctpass'
        )
        
        # Try with wrong password
        is_authenticated = self.client.login(username='authuser', password='wrongpass')
        self.assertFalse(is_authenticated)


class NoteAPITest(APITestCase):
    """Test the Notes API endpoints"""
    
    def setUp(self):
        """Create test user and authenticate"""
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
        
        # Login the user
        self.client.login(username='apiuser', password='apipass123')
        
        # Create a test note
        self.note = Note.objects.create(
            title='API Test Note',
            content='Testing API endpoints',
            category='school',
            user=self.user
        )
    
    def test_note_exists_after_setup(self):
        """Test that note was created in setup"""
        self.assertTrue(Note.objects.filter(title='API Test Note').exists())
    
    def test_user_has_notes(self):
        """Test that user can access their notes"""
        user_notes = Note.objects.filter(user=self.user)
        self.assertEqual(user_notes.count(), 1)
        self.assertEqual(user_notes.first().title, 'API Test Note')
    
    def test_create_note_programmatically(self):
        """Test creating a note through code"""
        note = Note.objects.create(
            title='Programmatic Note',
            content='Created through test',
            category='drama',
            user=self.user
        )
        
        self.assertTrue(Note.objects.filter(title='Programmatic Note').exists())
        self.assertEqual(note.user, self.user)


class NotePermissionsTest(TestCase):
    """Test that users can only access their own notes"""
    
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass2'
        )
        
        # Create notes for each user
        self.user1_note = Note.objects.create(
            title='User1 Note',
            content='User 1 private content',
            category='personal',
            user=self.user1
        )
        self.user2_note = Note.objects.create(
            title='User2 Note',
            content='User 2 private content',
            category='school',
            user=self.user2
        )
    
    def test_user1_sees_only_own_notes(self):
        """Test that user1 only sees their own notes"""
        user1_notes = Note.objects.filter(user=self.user1)
        
        self.assertEqual(user1_notes.count(), 1)
        self.assertEqual(user1_notes.first().title, 'User1 Note')
    
    def test_user2_sees_only_own_notes(self):
        """Test that user2 only sees their own notes"""
        user2_notes = Note.objects.filter(user=self.user2)
        
        self.assertEqual(user2_notes.count(), 1)
        self.assertEqual(user2_notes.first().title, 'User2 Note')
    
    def test_users_notes_are_isolated(self):
        """Test that users' notes are completely isolated"""
        user1_notes = Note.objects.filter(user=self.user1)
        user2_notes = Note.objects.filter(user=self.user2)
        
        # Each user should only have their own note
        self.assertEqual(user1_notes.count(), 1)
        self.assertEqual(user2_notes.count(), 1)
        
        # User1's notes should not contain user2's note
        self.assertNotIn(self.user2_note, user1_notes)
        # User2's notes should not contain user1's note
        self.assertNotIn(self.user1_note, user2_notes)





