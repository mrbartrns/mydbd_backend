from django.urls import path

from .views import *

# TODO: make clean url pattern
urlpatterns = [
    path("comments", CommentRecursiveView.as_view()),
    path("comment/update/<int:pk>", CommentUpdateAndDeleteView.as_view()),
    path(
        "comment/create/<str:category_name>/<int:obj_id>",
        CommentListAndCreateView.as_view(),
    ),
]
