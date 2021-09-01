from django.urls import path

from .views import *

urlpatterns = [
    path('comment/list/killer/recursive', KillerCommentRecursiveListView.as_view(),
         name='killer-comment-list-recursive'),
    path('comment/list/killer', KillerCommentListView.as_view(), name='killer-comment-list'),
    path('comment/create/killer/<int:killer_id>', CreateOrModifyKillerCommentView.as_view(),
         name='killer-comment-post')
]
