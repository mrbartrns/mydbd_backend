from django.urls import path

from .views import *

# TODO: make clean url pattern
urlpatterns = [
    path("forum/article/<int:pk>/comment/list", ArticleCommentListView.as_view()),
    path("forum/article/<int:pk>/comment/create", ArticleCommentCreateView.as_view()),
    path("comment/<int:pk>", CommentUpdateView.as_view()),
    path("comment/<int:pk>/like", CommentLikeView.as_view()),
    path("comment/<int:pk>/delete", CommentDeleteView.as_view()),
    path("search/tag", TagSearchView.as_view()),
    path("forum/image/upload", ImageUploadView.as_view()),
    path("forum/article/<int:pk>/like", ArticleLikeView.as_view()),
    path("forum/list", ArticleListView.as_view()),
    path("forum/article/create", ArticleCreateView().as_view()),
    path("forum/article/<int:pk>", ArticleDetailView.as_view()),
    path("forum/article/<int:pk>/edit", ArticleUpdateView.as_view()),
    path(
        "<str:category_name>/<int:obj_id>/comments",
        CommentListView.as_view(),
    ),
    path(
        "<str:category_name>/<int:obj_id>/comment/create",
        CommentCreateView.as_view(),
    ),
    path(
        "<str:category_name>/<int:obj_id>/like", DetailLikeView.as_view()
    ),  # <str:category> 에 forum이 매칭될 수 있으므로 항상 맨 뒤에 위치
]
