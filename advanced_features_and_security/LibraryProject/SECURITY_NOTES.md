# Security Best Practices Implemented

1. **Settings Hardening**
   - DEBUG = False
   - SECURE_BROWSER_XSS_FILTER, SECURE_CONTENT_TYPE_NOSNIFF, X_FRAME_OPTIONS
   - CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE
   - CSP configured with django-csp

2. **CSRF Protection**
   - All forms include `{% csrf_token %}`.

3. **Safe Database Access**
   - Django ORM used for queries to prevent SQL injection.
   - No raw SQL string concatenation.

4. **Content Security Policy**
   - Restricts scripts/styles to `'self'`.

5. **Testing**
   - Verified forms reject requests without CSRF token.
   - Verified inputs are sanitized in search functionality.
