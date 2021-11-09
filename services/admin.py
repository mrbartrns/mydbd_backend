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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "article_category",
        "title",
        "content",
        "dt_created",
        "dt_modified",
    )
    list_display_links = ("author", "title")
    list_filter = ("author", "title", "article_category")


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("tag", "article")
    list_display_links = ("tag", "article")
    list_filter = ("tag", "article")
