from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "parent",
        "depth",
        "category",
        "dt_created",
        "dt_modified",
    )
    list_display_links = ("author",)
    list_filter = ("dt_created", "depth")
    search_fields = ("author", "content")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "comment", "like", "dislike")
    list_display_links = ("user", "category", "comment")
    list_filter = ("category", "comment")
