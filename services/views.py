from django.db.models import Case, When
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

import apis.models as apis_models
import services.models as services_models
import services.serializers as services_serializers
from backend.permissions import *

CATEGORY_DICT = {
    "KILLER": "killer",
    "SURVIVOR": "survivor",
    "PERK": "perk",
    "ITEM": "item",
    "ADDON": "addon",
}


# Comment Pagination
class CommentPagination(PageNumberPagination):
    # TODO: change page_query_param page -> cp
    page_query_param = "page"
    page_size = 10


# comment object functions
def get_comments_by_category_name_and_object_id(category_name, obj_id):
    comments = None
    category = get_category_object(category_name, obj_id)
    if not category:
        return comments
    comments = category.comments.all()
    return comments


def get_category_object(category_name, obj_id):
    category = None
    if category_name == CATEGORY_DICT["KILLER"]:
        category = apis_models.Killer.objects.get(id=obj_id).category
    elif category_name == CATEGORY_DICT["SURVIVOR"]:
        category = apis_models.Survivor.objects.get(id=obj_id).category
    elif category_name == CATEGORY_DICT["PERK"]:
        category = apis_models.Perk.objects.get(id=obj_id).category
    elif category_name == CATEGORY_DICT["ITEM"]:
        category = apis_models.Item.objects.get(id=obj_id).category
    elif category_name == CATEGORY_DICT["ADDON"]:
        category = apis_models.ItemAddon.objects.get(id=obj_id).category
    return category


# Create your views here.
class CommentListByQueryAndCreateView(APIView, CommentPagination):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = services_serializers.CommentSerializer

    def get(self, request, category_name, obj_id):
        """
        query_string에 따라 depth를 나누어주는 view
        """
        serializer = self.serializer_class
        parent = request.GET.get("parent", None)
        # TODO: 추후에 like를 모델에 추가한다. 현재는 등록순으로 추가
        sortby = request.GET.get("sortby", "recent")
        comments = get_comments_by_category_name_and_object_id(category_name, obj_id)

        # root 댓글 또는 child 댓글을 불러온다.
        if parent:
            comments = comments.filter(parent=parent)
        else:
            comments = comments.filter(depth=0)

        # 댓글의 정렬방식을 결정한다.
        if sortby == "id":
            comments = comments.order_by("id")
        elif sortby == "recent":
            comments = comments.order_by("-id")
        elif sortby == "like":
            pass
        page = self.paginate_queryset(comments, request, view=self)
        response = self.get_paginated_response(serializer(page, many=True).data)
        return response

    def post(self, request, category_name, obj_id):
        serializer = self.serializer_class(data=request.data)

        category = get_category_object(category_name, obj_id)

        if category and serializer.is_valid():
            data = serializer.validated_data
            parent = data.get("parent", None)
            if parent and parent.parent:
                return Response(
                    {"detail": "bad request"}, status=status.HTTP_403_FORBIDDEN
                )
            comment = serializer.save(author=request.user, category=category)
            return Response(
                services_serializers.CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateAndDeleteView(APIView):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = services_serializers.CommentSerializer

    # for test
    def get(self, request, pk):
        comment = services_models.Comment.objects.get(id=pk)
        serializer = services_serializers.CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment = services_models.Comment.objects.get(id=pk)
        serializer = self.serializer_class(comment, data=request.data)
        self.check_object_permissions(request, comment)

        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                services_serializers.CommentSerializer(comment).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = services_models.Comment.objects.get(id=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(
            {"success": "successfully deleted."}, status=status.HTTP_202_ACCEPTED
        )


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = services_serializers.LikeSerializer

    def get(self, request, pk):
        likes = services_models.Like.objects.filter(user=request.user, comment=pk)
        if likes.exists():
            like = likes[0]
            return Response(
                self.serializer_class(like).data,
                status=status.HTTP_200_OK,
            )
        return Response({"detail": "You have not been liked comment."})

    # TODO: like를 클릭 후 dislike를 누른 뒤 문제 없게 해야 함 -> 프론트에서 처리
    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            comment = services_models.Comment.objects.get(id=pk)
            likes = services_models.Like.objects.filter(
                comment=comment, user=request.user
            )
            if likes.exists():
                like = likes[0]
                like.like = False
                like.dislike = False
                # True, False 결정은 Frontend에서 처리
                if serializer.validated_data.get("like"):
                    like.like = True
                elif serializer.validated_data.get("dislike"):
                    like.dislike = True
                like.save()
                return Response(
                    self.serializer_class(like).data, status=status.HTTP_202_ACCEPTED
                )
            like = serializer.save(comment=comment, user=request.user)
            return Response(
                # services_serializers.LikeSerializer(like).data,
                self.serializer_class(like).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = services_serializers.LikeSerializer

    def get(self, request, category_name, obj_id):
        pass
