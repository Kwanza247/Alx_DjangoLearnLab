from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    if sender.name == "bookshelf":
        # Get model permissions
        content_type = apps.get_model("contenttypes.ContentType")
        book_model = apps.get_model("bookshelf", "Book")
        permissions = Permission.objects.filter(content_type__app_label="bookshelf", content_type__model="book")

        # Define groups and their permissions
        group_permissions = {
            "Viewers": ["can_view"],
            "Editors": ["can_view", "can_create", "can_edit"],
            "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
        }

        for group_name, perms in group_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm in perms:
                try:
                    permission = Permission.objects.get(codename=perm, content_type__model="book")
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    pass
