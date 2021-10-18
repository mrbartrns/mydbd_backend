from django.urls import path

from .views import *

# TODO: make clean url pattern
urlpatterns = [
    # path("comments", CommentRecursiveView.as_view()),
    path(
        "list/<str:category_name>/<int:obj_id>/comments",
        CommentListByQueryAndCreateView.as_view(),
    ),
    # path(
    #     "comments/list/<str:category_name>/<int:obj_id>",
    #     CommentListAndCreateView.as_view(),
    # ),
    path("comment/<int:pk>", CommentUpdateAndDeleteView.as_view()),
]
