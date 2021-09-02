from django.urls import path

from .views import *

# TODO: make clean url pattern
urlpatterns = [
    path('comment/killer/list/<int:killer_id>', KillerCommentListView.as_view()),
    path('comment/killer/detail/<int:pk>', KillerCommentDetailView.as_view()),
]
