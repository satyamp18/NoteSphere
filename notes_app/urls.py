from django.urls import path
from . import views

app_name = 'notes_app'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alt'),

    # Notes CRUD
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:pk>/pin/', views.note_toggle_pin, name='note_toggle_pin'),

    # Documents CRUD & Download
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('documents/<int:pk>/download/', views.document_download, name='document_download'),

    # Search
    path('search/', views.search_view, name='search'),
]
