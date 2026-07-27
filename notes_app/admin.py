from django.contrib import admin
from .models import Note, Document

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'is_pinned', 'color', 'created_at', 'updated_at')
    list_filter = ('category', 'is_pinned', 'color', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    list_editable = ('is_pinned',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'file_type', 'formatted_size', 'created_at')
    list_filter = ('category', 'file_type', 'created_at')
    search_fields = ('title', 'description', 'user__username')
