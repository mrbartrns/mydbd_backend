from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


# Register your models here.


class OwnerModelInline(admin.StackedInline):
    model = Owner
    can_delete = False


class KillerAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']
    inlines = (OwnerModelInline,)


class SurvivorAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']
    inlines = (OwnerModelInline,)


admin.site.register(Killer, KillerAdmin)
admin.site.register(Survivor, SurvivorAdmin)
