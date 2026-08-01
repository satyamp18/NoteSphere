# 📝 NoteSphere – Smart Notes & Document Management System

NoteSphere is a feature-rich, responsive, and secure **Note & Document Management System** built with **Python, Django, Bootstrap 5, and Vanilla CSS/JS**. Inspired by modern productivity tools like Notion, Google Keep, and OneNote.

---

## ✨ Features

- 🎨 **Modern UI/UX**: Clean dashboard with pastel accent colors, dark mode toggle, and smooth animations.
- 📌 **Notes Management**: Create, edit, view, delete, and pin important notes to top.
- 📁 **Document Uploads**: Upload, preview, and download documents (**PDF**, **DOC/DOCX**, **TXT**) with 10MB file size limits and validation.
- 🔒 **User Authentication**: Secure user registration, login, logout, profile customization, and password updates with complete user data isolation.
- 🔍 **Universal Search**: Fast real-time search across all your saved notes and uploaded files.
- 📊 **Storage Quota & Metrics**: Dynamic visual indicator for personal cloud storage usage.
- 🛡️ **Built-in Security**: CSRF protection, secure media file handling, XSS prevention, and custom error pages (404, 403, 500).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Django 4.2+ (ORM, Views, Forms, Signals)
- **Database**: SQLite (Development) / Configurable to PostgreSQL
- **Frontend**: HTML5, Custom CSS3 Design System, JavaScript, Bootstrap 5, FontAwesome 6
- **Typography**: Google Fonts (Plus Jakarta Sans)

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or higher installed on your machine.
- Git (optional, for version control).

### 2. Clone / Setup Workspace
```bash
cd NoteSphere
```

### 3. Create & Activate Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Demo Admin Account (Optional)
```bash
python create_default_admin.py
```

### 7. Start Development Server
```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/` in your web browser.

---

## 🔑 Demo Account Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| **Demo Admin** | `admin` | `adminpass123` |

---

## 📂 Project Structure

```text
NoteSphere/
├── accounts/               # User authentication, profiles, & settings
├── notes_app/              # Core notes, documents, & search logic
├── notes_manager/          # Django project configuration & settings
├── static/                 # CSS design system, JavaScript, & assets
├── templates/              # HTML layout, dashboard, auth, & detail pages
├── media/                  # User uploaded documents & media files
├── .gitignore              # Git ignore configuration
├── manage.py               # Django management script
├── create_default_admin.py # Script to initialize demo superuser
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
