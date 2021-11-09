from django.contrib.auth.models import User
from django.db import models

from apis.models import Category


# Create your models here.
# comment can be deleted by author, admin or staff
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="parent-comment",
        related_name="children",
    )
    # group = models.PositiveIntegerField(default=1)
    depth = models.PositiveIntegerField(default=0)
    # seq = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="comment-category",
        related_name="comments",
    )
    content = models.TextField(verbose_name="content", max_length=500)
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    dt_modified = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        ordering = ["dt_created"]

    def __str__(self):
        return f"Comment by {self.author}"


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="user", related_name="likes"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="like-category",
        related_name="likes",
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        verbose_name="like-comment",
        related_name="likes",
        null=True,
    )
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    dt_modified = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.user.username} likes comment id  {self.comment if self.comment else self.category.id}"


class ArticleCategory(models.Model):
    name = models.CharField(max_length=20)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Article(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="author",
        related_name="articles",
        null=True,
    )
    article_category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        verbose_name="article category",
        related_name="articles",
        null=True,
    )  # TODO: modify after creatng articleCategory
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000)
    tags = models.ManyToManyField(
        Tag, through="ArticleTag", related_name="articles", blank=True
    )
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    dt_modified = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self) -> str:
        return self.title


class ArticleTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Article object with tag name {self.tag.name if self.tag else 'None'}, article title {self.article.title if self.article else 'None'}"
