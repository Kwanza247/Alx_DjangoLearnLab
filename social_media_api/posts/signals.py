from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from .models import Like, Comment
try:
    from notifications.models import Notification
except Exception:
    Notification = None

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if not created or Notification is None:
        return
    post = instance.post
    if post.author != instance.user:
        Notification.objects.create(
            recipient=post.author,
            actor=instance.user,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.pk
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if not created or Notification is None:
        return
    post = instance.post
    if post.author != instance.author:
        Notification.objects.create(
            recipient=post.author,
            actor=instance.author,
            verb='commented on your post',
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.pk
        )
