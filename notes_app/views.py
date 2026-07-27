from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.http import FileResponse, Http404, HttpResponseForbidden
from .models import Note, Document
from .forms import NoteForm, DocumentUploadForm, DocumentEditForm
import os

@login_required
def dashboard(request):
    notes = Note.objects.filter(user=request.user)
    documents = Document.objects.filter(user=request.user)

    total_notes = notes.count()
    total_documents = documents.count()

    storage_bytes = documents.aggregate(total=Sum('file_size'))['total'] or 0
    storage_mb = round(storage_bytes / (1024 * 1024), 2)
    storage_quota_mb = 100.0  # 100 MB default quota
    storage_percent = min(100, int((storage_mb / storage_quota_mb) * 100))

    recent_notes = notes[:6]
    recent_documents = documents[:5]

    context = {
        'total_notes': total_notes,
        'total_documents': total_documents,
        'storage_bytes': storage_bytes,
        'storage_mb': storage_mb,
        'storage_quota_mb': storage_quota_mb,
        'storage_percent': storage_percent,
        'recent_notes': recent_notes,
        'recent_documents': recent_documents,
    }
    return render(request, 'notes_app/dashboard.html', context)

# --- NOTES MANAGEMENT ---

@login_required
def note_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category:
        notes = notes.filter(category=category)

    pinned_notes = notes.filter(is_pinned=True)
    unpinned_notes = notes.filter(is_pinned=False)

    paginator = Paginator(unpinned_notes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pinned_notes': pinned_notes,
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'categories': [c[0] for c in Note.CATEGORY_CHOICES],
    }
    return render(request, 'notes_app/note_list.html', context)

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes_app/note_detail.html', {'note': note})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('notes_app:note_detail', pk=note.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        initial_category = request.GET.get('category', 'General')
        form = NoteForm(initial={'category': initial_category})
    return render(request, 'notes_app/note_form.html', {'form': form, 'title': 'Create Note'})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('notes_app:note_detail', pk=note.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes_app/note_form.html', {'form': form, 'note': note, 'title': 'Edit Note'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes_app:note_list')
    return render(request, 'notes_app/note_confirm_delete.html', {'note': note})

@login_required
def note_toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    status = "pinned" if note.is_pinned else "unpinned"
    messages.success(request, f'Note "{note.title}" has been {status}.')
    return redirect(request.META.get('HTTP_REFERER', 'notes_app:note_list'))


# --- DOCUMENT MANAGEMENT ---

@login_required
def document_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    documents = Document.objects.filter(user=request.user)

    if query:
        documents = documents.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        documents = documents.filter(category=category)

    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Storage calculation
    total_bytes = Document.objects.filter(user=request.user).aggregate(total=Sum('file_size'))['total'] or 0
    storage_mb = round(total_bytes / (1024 * 1024), 2)

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'categories': [c[0] for c in Document.CATEGORY_CHOICES],
        'storage_mb': storage_mb,
    }
    return render(request, 'notes_app/document_list.html', context)

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            file_obj = request.FILES['file']
            doc.file_size = file_obj.size
            ext = os.path.splitext(file_obj.name)[1].lower().replace('.', '')
            doc.file_type = ext
            doc.save()
            messages.success(request, f'Document "{doc.title}" uploaded successfully!')
            return redirect('notes_app:document_list')
        else:
            messages.error(request, 'Failed to upload document. Please check the validation errors.')
    else:
        form = DocumentUploadForm()
    return render(request, 'notes_app/document_form.html', {'form': form, 'title': 'Upload Document'})

@login_required
def document_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    return render(request, 'notes_app/document_detail.html', {'document': doc})

@login_required
def document_edit(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DocumentEditForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully!')
            return redirect('notes_app:document_detail', pk=doc.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DocumentEditForm(instance=doc)
    return render(request, 'notes_app/document_form.html', {'form': form, 'document': doc, 'title': 'Edit Document Details'})

@login_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        if doc.file and os.path.isfile(doc.file.path):
            os.remove(doc.file.path)
        doc.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('notes_app:document_list')
    return render(request, 'notes_app/document_confirm_delete.html', {'document': doc})

@login_required
def document_download(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if not doc.file or not os.path.exists(doc.file.path):
        raise Http404("Requested file does not exist on the server.")
    
    response = FileResponse(open(doc.file.path, 'rb'), as_attachment=True, filename=doc.filename)
    return response


# --- UNIVERSAL SEARCH ---

@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()

    notes = []
    documents = []

    if query:
        notes = Note.objects.filter(
            user=request.user
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(category__icontains=query)
        )

        documents = Document.objects.filter(
            user=request.user
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(file_type__icontains=query) | Q(category__icontains=query)
        )

    context = {
        'query': query,
        'notes': notes,
        'documents': documents,
        'total_results': len(notes) + len(documents),
    }
    return render(request, 'notes_app/search_results.html', context)


# --- CUSTOM ERROR VIEWS ---

def custom_404_view(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def custom_403_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)
