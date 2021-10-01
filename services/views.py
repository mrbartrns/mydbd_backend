from django.core.paginator import Paginator
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
class CommentRecursiveView(APIView, CommentPagination):
    permission_classes = [IsAuthenticated]
    serializer_class = services_serializers.CommentRecursiveSerializer

    def get(self, request):
        comments = services_models.Comment.objects.filter(depth=0)
        page = self.paginate_queryset(comments, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True).data
        )
        # return Response(
        #     services_serializers.CommentRecursiveSerializer(comments, many=True).data,
        #     status=status.HTTP_200_OK,
        # )
        return response


class CommentsListView(APIView, CommentPagination):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_classes = services_serializers.CommentSerializer

    def get(self, request, category_name, obj_id):
        comments = None
        depth = request.GET.get("depth", 0)
        parent = request.GET.get("parent", None)
        # TODO: align order request
        order = request.GET.get("order", "")
        if category_name == "killer":
            comments = apis_models.Killer.objects.get(
                id=obj_id
            ).category.comments.filter(depth=depth, parent=parent)
        if comments:
            page = self.paginate_queryset(comments, request, view=self)
            print(page)
            response = self.get_paginated_response(
                self.serializer_classes(page, many=True).data
            )
            return response
        return Response({"detail": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


class CommentListAndCreateView(APIView, CommentPagination):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, category_name, obj_id):
        serializer = services_serializers.CommentSerializer
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
        if comments is not None:
            comments = comments.order_by("group", "seq")
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
