/* ==========================================================================
   NoteSphere - JavaScript Interactivity & Handlers
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Dark Mode Initialization & Switcher
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const storedTheme = localStorage.getItem('notesphere_theme');

    if (storedTheme) {
        document.documentElement.setAttribute('data-bs-theme', storedTheme);
        updateThemeIcon(storedTheme);
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            document.documentElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('notesphere_theme', newTheme);
            updateThemeIcon(newTheme);

            // Sync with backend if user is authenticated
            const csrfToken = getCookie('csrftoken');
            if (csrfToken) {
                fetch('/accounts/toggle-dark-mode/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                }).catch(err => console.log('Dark mode sync skipped:', err));
            }
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (icon) {
            if (theme === 'dark') {
                icon.className = 'fa-solid fa-sun text-warning';
            } else {
                icon.className = 'fa-solid fa-moon text-secondary';
            }
        }
    }

    // Helper to get CSRF Cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 2. Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const appSidebar = document.querySelector('.app-sidebar');

    if (sidebarToggleBtn && appSidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            appSidebar.classList.toggle('show');
        });
    }

    // 3. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // 4. File Drag and Drop Validation & Preview
    const fileInput = document.getElementById('id_file');
    const dropzone = document.getElementById('uploadDropzone');

    if (fileInput && dropzone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => dropzone.classList.add('border-primary', 'bg-light'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => dropzone.classList.remove('border-primary', 'bg-light'), false);
        });

        dropzone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length) {
                fileInput.files = files;
                updateFilePreview(files[0]);
            }
        }

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                updateFilePreview(e.target.files[0]);
            }
        });

        function updateFilePreview(file) {
            const previewText = document.getElementById('filePreviewText');
            if (previewText) {
                const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                previewText.innerHTML = `<i class="fa-solid fa-file-circle-check text-success me-2"></i> Selected: <strong>${file.name}</strong> (${sizeMB} MB)`;
            }
        }
    }

    // 5. Global Copy to Clipboard Helper
    window.copyToClipboard = function(text, buttonElement) {
        navigator.clipboard.writeText(text).then(() => {
            const originalHTML = buttonElement.innerHTML;
            buttonElement.innerHTML = '<i class="fa-solid fa-check text-success me-1"></i> Copied!';
            setTimeout(() => {
                buttonElement.innerHTML = originalHTML;
            }, 2000);
        }).catch(err => {
            console.error('Copy failed:', err);
        });
    };
});
