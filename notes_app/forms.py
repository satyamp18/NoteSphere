from django import forms
from .models import Note, Document
import os

ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt']
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

class NoteForm(forms.ModelForm):
    title = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Title'})
    )
    content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Start typing your note here...'})
    )
    category = forms.ChoiceField(
        choices=Note.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    color = forms.ChoiceField(
        choices=Note.COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    is_pinned = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'color', 'is_pinned']

class DocumentUploadForm(forms.ModelForm):
    title = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document Title'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional document description...'})
    )
    category = forms.ChoiceField(
        choices=Document.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.txt'})
    )

    class Meta:
        model = Document
        fields = ['title', 'description', 'category', 'file']

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f"Unsupported file format '{ext}'. Allowed formats: PDF, DOC, DOCX, TXT."
                )
            if uploaded_file.size > MAX_FILE_SIZE_BYTES:
                raise forms.ValidationError(
                    f"File size exceeds limit of {MAX_FILE_SIZE_MB}MB. Current file size: {uploaded_file.size / (1024*1024):.2f}MB."
                )
        return uploaded_file

class DocumentEditForm(forms.ModelForm):
    title = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document Title'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional document description...'})
    )
    category = forms.ChoiceField(
        choices=Document.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Document
        fields = ['title', 'description', 'category']
