from django.contrib.auth.models import User
from django.db import models

from apis.models import Category


# Create your models here.
# comment can be deleted by author, admin or staff
class Comment(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='author')
    parent_comment = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name='parent-comment')
    category = models.OneToOneField(Category, on_delete=models.CASCADE, verbose_name='comment-category')
    content = models.TextField(verbose_name='content')
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    dt_modified = models.DateTimeField(auto_now=True, verbose_name='수정일')
