from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def check_comment_depth(sender, instance, created, **kwargs):
    if created and instance.parent:
        instance.depth = instance.parent.depth + 1
        instance.save()
