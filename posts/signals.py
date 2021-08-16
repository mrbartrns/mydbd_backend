from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Killer)
def create_killer_owner(sender, instance, created, **kwargs):
    if created:
        Owner.objects.create(killer=instance)


# @receiver(post_save, sender=Killer)
# def save_killer_owner(sender, instance, created, **kwargs):
#     instance.owner.save()


@receiver(post_save, sender=Survivor)
def create_survivor_owner(sender, instance, created, **kwargs):
    if created:
        Owner.objects.create(survivor=instance)

# @receiver(post_save, sender=Survivor)
# def save_survivor_owner(sender, instance, created, **kwargs):
#     instance.owner.save()
