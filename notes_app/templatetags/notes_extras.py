from django import template
import os

register = template.Library()

@register.filter
def file_icon(ext_or_name):
    if not ext_or_name:
        return 'fa-file'
    ext = ext_or_name.lower()
    if '.' in ext:
        ext = os.path.splitext(ext)[1]
    
    ext = ext.replace('.', '')
    
    icons = {
        'pdf': 'fa-file-pdf text-danger',
        'doc': 'fa-file-word text-primary',
        'docx': 'fa-file-word text-primary',
        'txt': 'fa-file-lines text-secondary',
        'png': 'fa-file-image text-info',
        'jpg': 'fa-file-image text-info',
        'jpeg': 'fa-file-image text-info',
    }
    return icons.get(ext, 'fa-file text-muted')

@register.filter
def category_badge(category):
    badges = {
        'Personal': 'bg-purple-subtle text-purple border-purple-subtle',
        'Work': 'bg-primary-subtle text-primary border-primary-subtle',
        'Ideas': 'bg-warning-subtle text-warning border-warning-subtle',
        'Study': 'bg-info-subtle text-info border-info-subtle',
        'Code': 'bg-success-subtle text-success border-success-subtle',
        'Finance': 'bg-emerald-subtle text-emerald border-emerald-subtle',
        'General': 'bg-secondary-subtle text-secondary border-secondary-subtle',
    }
    return badges.get(category, 'bg-light text-dark')

@register.filter
def filesize_format(size_in_bytes):
    try:
        size = float(size_in_bytes)
        if size < 1024:
            return f"{int(size)} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"
    except (ValueError, TypeError):
        return "0 B"
