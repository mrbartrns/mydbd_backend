from django.db import models


# Create your models here.
class Killer(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="영문 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 이름")
    speed = models.FloatField(verbose_name="이동 속도(m/s)", default=4.6)
    terror_radius = models.PositiveIntegerField(verbose_name="공포범위(m/s)")
    img_url = models.URLField(verbose_name="이미지 url", blank=True)
    note = models.TextField(verbose_name='비고', blank=True)
    dt_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="date modified", auto_now=True)

    def __str__(self):
        return self.name


class Survivor(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="영문 이름")
    name_kor = models.CharField(max_length=256, unique=True, verbose_name="한글 이름")
    speed = models.FloatField(verbose_name='이동 속도(m/s)', default=4.0)
    img_url = models.URLField(verbose_name="이미지 url", blank=True)
    dt_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="date modified", auto_now=True)

    def __str__(self):
        return self.name


class Owner(models.Model):
    killer = models.OneToOneField(Killer, on_delete=models.CASCADE, null=True)
    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.killer is not None:
            return self.killer.name
        return self.survivor.name
