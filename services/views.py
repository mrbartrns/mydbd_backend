from django.db.models import Case, When
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

import apis.models as apis_models
import services.models as services_models
import services.serializers as services_serializers
from backend.permissions import *


# Comment Pagination
class CommentPagination(PageNumberPagination):
    # TODO: change page_query_param page -> cp
    page_query_param = "page"
    page_size = 10


# Create your views here.
class CommentListByQueryAndCreateView(APIView, CommentPagination):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, category_name, obj_id):
        """
        query_string에 따라 depth를 나누어주는 view
        """
        serializer = services_serializers.CommentSerializer
        parent = request.GET.get("parent", "")
        # TODO: 추후에 like를 모델에 추가한다. 현재는 등록순으로 추가
        sortby = request.GET.get("sortby", "id")
        comments = None
        if category_name == "killer":
            comments = apis_models.Killer.objects.get(id=obj_id).category.comments.all()
        elif category_name == "survivor":
            comments = apis_models.Survivor.objects.get(
                id=obj_id
            ).category.comments.all()
        elif category_name == "perk":
            comments = apis_models.Perk.objects.get(id=obj_id).category.comments.all()
        elif category_name == "item":
            comments = apis_models.Item.objects.get(id=obj_id).category.comments.all()
        elif category_name == "addon":
            comments = apis_models.ItemAddon.objects.get(
                id=obj_id
            ).category.comments.all()

        if parent != "":
            comments = comments.filter(parent=parent)
        else:
            comments = comments.filter(depth=0)

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
        serializer = services_serializers.CommentPostSerializer(data=request.data)
        category = None

        if category_name == "killer":
            category = apis_models.Killer.objects.get(id=obj_id).category
        elif category_name == "survivor":
            category = apis_models.Survivor.objects.get(id=obj_id).category
        elif category_name == "item":
            category = apis_models.Item.objects.get(id=obj_id).category
        elif category_name == "addon":
            category = apis_models.ItemAddon.objects.get(id=obj_id).category

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


class CommentListAndCreateView(APIView, CommentPagination):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, category_name, obj_id):
        serializer = services_serializers.CommentSerializer
        comments = None
        if category_name == "killer":
            comments = apis_models.Killer.objects.get(id=obj_id).category.comments
        elif category_name == "survivor":
            comments = apis_models.Survivor.objects.get(
                id=obj_id
            ).category.comments.all()
        elif category_name == "perk":
            comments = apis_models.Perk.objects.get(id=obj_id).category.comments
        elif category_name == "item":
            comments = apis_models.Item.objects.get(id=obj_id).category.comments.all()
        elif category_name == "addon":
            comments = apis_models.ItemAddon.objects.get(
                id=obj_id
            ).category.comments.all()
        if comments is not None:
            comments = comments.annotate(
                sort_order_true=Case(When(parent=not None, then="parent"), default="id")
            ).order_by("sort_order_true")
            page = self.paginate_queryset(comments, request, view=self)
            response = self.get_paginated_response(serializer(page, many=True).data)
            return response

    def post(self, request, category_name, obj_id):
        serializer = services_serializers.CommentPostSerializer(data=request.data)
        category = None

        if category_name == "killer":
            category = apis_models.Killer.objects.get(id=obj_id).category
        elif category_name == "survivor":
            category = apis_models.Survivor.objects.get(id=obj_id).category
        elif category_name == "item":
            category = apis_models.Item.objects.get(id=obj_id).category
        elif category_name == "addon":
            category = apis_models.ItemAddon.objects.get(id=obj_id).category

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

    def put(self, request, pk):
        comment = apis_models.Comment.objects.get(id=pk)
        serializer = services_serializers.CommentRecursiveSerializer(
            comment, data=request.data
        )
        self.check_object_permissions(request, comment)

        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                services_serializers.CommentRecursiveSerializer(comment).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # check is_staff option in future
        comment = apis_models.Comment.objects.get(id=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(
            {"success": "successfully deleted."}, status=status.HTTP_204_NO_CONTENT
        )
