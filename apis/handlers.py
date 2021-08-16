from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Killer)
def create_killer_owner_and_category(sender, instance, created, **kwargs):
    if created:
        # create Owner object
        Owner.objects.create(killer=instance)
        # create Category object
        Category.objects.create(killer=instance)


@receiver(post_save, sender=Survivor)
def create_survivor_owner_and_category(sender, instance, created, **kwargs):
    if created:
        # create Owner object
        Owner.objects.create(survivor=instance)
        # create Category object
        Category.objects.create(survivor=instance)


@receiver(post_save, sender=Perk)
def create_perk_category(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(perk=instance)


@receiver(post_save, sender=Item)
def create_item_category(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(item=instance)


@receiver(post_save, sender=ItemAddon)
def create_item_category(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(item_addon=instance)
