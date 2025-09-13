# Permissions & Groups Setup

We added custom permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) to the `Book` model.

Groups created automatically:
- **Viewers** → can_view
- **Editors** → can_view, can_create, can_edit
- **Admins** → can_view, can_create, can_edit, can_delete

Views are protected using `@permission_required`.

Assign users to groups in Django Admin to test access restrictions.

