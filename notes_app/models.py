from django.db import models
from django.contrib.auth.models import User
import os

class Note(models.Model):
    CATEGORY_CHOICES = [
        ('Personal', 'Personal'),
        ('Work', 'Work'),
        ('Ideas', 'Ideas'),
        ('Study', 'Study'),
        ('Code', 'Code'),
        ('General', 'General'),
    ]

    COLOR_CHOICES = [
        ('default', 'Default White / Slate'),
        ('lemon', 'Soft Yellow'),
        ('mint', 'Soft Green'),
        ('sky', 'Soft Blue'),
        ('lavender', 'Soft Purple'),
        ('peach', 'Soft Orange'),
        ('rose', 'Soft Pink'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='default')
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Study', 'Study'),
        ('Finance', 'Finance'),
        ('General', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/')
    file_type = models.CharField(max_length=10, blank=True)
    file_size = models.BigIntegerField(default=0)  # stored in bytes
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def formatted_size(self):
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"
