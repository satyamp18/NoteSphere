from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from notes_app.models import Note, Document

class NotesAppTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client = Client()

    def test_note_creation_and_user_isolation(self):
        note = Note.objects.create(
            user=self.user1,
            title="User 1 Note",
            content="Private content",
            category="Personal"
        )
        self.assertEqual(note.title, "User 1 Note")
        
        # Log in as user2 and attempt to view user1's note -> Should return 404
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('notes_app:note_detail', kwargs={'pk': note.pk}))
        self.assertEqual(response.status_code, 404)

    def test_document_upload_and_download_security(self):
        dummy_file = SimpleUploadedFile("sample.txt", b"Hello NoteSphere", content_type="text/plain")
        doc = Document.objects.create(
            user=self.user1,
            title="Test Doc",
            file=dummy_file,
            file_type="txt",
            file_size=16,
            category="General"
        )

        # Log in as user1 and download file -> Should return 200
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('notes_app:document_download', kwargs={'pk': doc.pk}))
        self.assertEqual(response.status_code, 200)

        # Log in as user2 and attempt download -> Should return 404
        self.client.login(username='user2', password='password123')
        response_user2 = self.client.get(reverse('notes_app:document_download', kwargs={'pk': doc.pk}))
        self.assertEqual(response_user2.status_code, 404)
