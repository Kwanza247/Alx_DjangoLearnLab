# Permissions & Groups Setup

We added custom permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) to the `Book` model.

Groups created automatically:
- **Viewers** → can_view
- **Editors** → can_view, can_create, can_edit
- **Admins** → can_view, can_create, can_edit, can_delete

Views are protected using `@permission_required`.

Assign users to groups in Django Admin to test access restrictions.

#steps in implementing HTTPPS and secure Redirects in Django

Forced HTTPS with SECURE_SSL_REDIRECT.

Set HSTS (SECURE_HSTS_*).

Secured cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE).

Added headers (X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF, SECURE_BROWSER_XSS_FILTER).

Configured web server with SSL/TLS (mention Let’s Encrypt or your cert provider).