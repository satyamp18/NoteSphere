import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes_manager.settings')
django.setup()

from django.contrib.auth.models import User
from notes_app.models import Note, Document

# Create Superuser / Admin
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@notesphere.com', 'adminpass123')
    admin_user.first_name = "Alex"
    admin_user.last_name = "Morgan"
    admin_user.save()
    print('Created superuser: admin / adminpass123')
else:
    admin_user = User.objects.get(username='admin')

# Create Sample Notes for Admin
if Note.objects.filter(user=admin_user).count() == 0:
    Note.objects.create(
        user=admin_user,
        title="🚀 Welcome to NoteSphere!",
        content="NoteSphere is your minimal, clean, and production-ready workspace inspired by Notion and Google Keep.\n\nKey features:\n• Universal Search bar at top\n• Color-accented note cards with pinning\n• Secure document upload & storage (PDF, DOCX, TXT)\n• Profile management and Dark Mode toggle",
        category="General",
        color="mint",
        is_pinned=True
    )
    Note.objects.create(
        user=admin_user,
        title="💡 Project Architecture Ideas",
        content="Clean Django modular architecture built with PEP8 compliance:\n1. accounts app for Auth & Profile\n2. notes_app for Notes & Document Management\n3. Custom template tags & error pages (404, 403, 500)\n4. Responsive design for Desktop, Tablet, and Mobile",
        category="Ideas",
        color="sky",
        is_pinned=True
    )
    Note.objects.create(
        user=admin_user,
        title="📝 Weekly Sprint Backlog",
        content="1. Review database queries & indexes\n2. Verify file size validation (10MB max)\n3. Test document download permissions\n4. Check dark mode local persistence",
        category="Work",
        color="peach",
        is_pinned=False
    )
    print("Created sample notes for demo user.")

# Create Sample Document for Admin
if Document.objects.filter(user=admin_user).count() == 0:
    sample_content = b"NoteSphere Document Management System Sample Text File.\nCreated successfully for production verification."
    doc = Document(
        user=admin_user,
        title="NoteSphere Quickstart Guide",
        description="Official quickstart documentation and feature breakdown file.",
        category="General",
        file_type="txt",
        file_size=len(sample_content)
    )
    doc.file.save("quickstart_guide.txt", ContentFile(sample_content), save=True)
    print("Created sample document for demo user.")

print("Setup completed successfully.")
