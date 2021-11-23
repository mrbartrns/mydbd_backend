from django.urls import path

from .views import *

# TODO: make clean url pattern
urlpatterns = [
    path(
        "list/<str:category_name>/<int:obj_id>/comments",
        CommentListView.as_view(),
    ),
    path(
        "list/<str:category_name>/<int:obj_id>/comments/create",
        CommentCreateView.as_view(),
    ),
    path("forum/<int:pk>/comment/create", ArticleCommentCreateView.as_view()),
    path("comment/<int:pk>", CommentUpdateAndDeleteView.as_view()),
    path("comment/<int:pk>/like", CommentLikeView.as_view()),
    path("search/tag", TagSearchView.as_view()),
    path("forum/<int:pk>/like", ArticleLikeView.as_view()),
    path("forum/list", ArticleListView.as_view()),
    path("forum/article/create", ArticleCreateView().as_view()),
    path("forum/<int:pk>", ArticleDetailView.as_view()),
    path(
        "<str:category_name>/<int:obj_id>/like", DetailLikeView.as_view()
    ),  # <str:category> 에 forum이 매칭될 수 있으므로 항상 맨 뒤에 위치
]
