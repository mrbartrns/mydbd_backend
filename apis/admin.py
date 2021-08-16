from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


# Register your models here.


class OwnerModelInline(admin.StackedInline):
    model = Owner
    can_delete = False


class CategoryInline(admin.StackedInline):
    model = Category
    can_delete = False


class KillerAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']
    inlines = (OwnerModelInline, CategoryInline)


class SurvivorAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']
    inlines = (OwnerModelInline, CategoryInline)


class PerkAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'owner', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']
    inlines = (CategoryInline,)


class ItemCategoryAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']


class ItemAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'rarity', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']
    inlines = (CategoryInline,)


class ItemAddonAdmin(ModelAdmin):
    list_display = ['id', 'name', 'name_kor', 'dt_created', 'dt_modified']
    list_display_links = ['id', 'name', 'name_kor']
    inlines = (CategoryInline,)


admin.site.register(Killer, KillerAdmin)
admin.site.register(Survivor, SurvivorAdmin)
admin.site.register(Perk, PerkAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(ItemAddon, ItemAddonAdmin)