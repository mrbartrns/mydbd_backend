from django.urls import path

from .views import *

# TODO: make clean url pattern
urlpatterns = [
    path(
        "list/<str:category_name>/<int:obj_id>/comments",
        CommentListByQueryAndCreateView.as_view(),
    ),
    path("comment/<int:pk>", CommentUpdateAndDeleteView.as_view()),
    path("comment/<int:pk>/like", CommentLikeView.as_view()),
]
