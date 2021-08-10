from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nickname if self.nickname else self.user.username


# error occurs when updating profile
# when user attempt to create user model with nickname occurs error
# TODO: Try to use just Views or unregister user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # user(object).profile.save()
    instance.profile.save()
