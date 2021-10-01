from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def check_comment_depth(sender, instance, created, **kwargs):
    if created and instance.parent:
        # instance.depth = instance.parent.depth + 1
        instance.depth = 1
        instance.save()


# @receiver(post_save, sender=Comment)
# def set_comment_sequence(sender, instance, created, **kwargs):
#     if created and instance.parent:
#         seq = instance.parent.children.order_by("-seq").first().seq
#         instance.seq = seq + 1
#         instance.save()


# @receiver(post_save, sender=Comment)
# def set_group(sender, instance, created, **kwargs):
#     if created:
#         group = instance.id
#         if instance.parent:
#             group = instance.parent.group
#         instance.group = group
#         instance.save()
