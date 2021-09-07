from typing import Union

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import apis.models as apis_models
import services.serializers as services_serializers
from backend.permissions import *


# Create your views here.
class CommentRecursiveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = apis_models.Comment.objets.filter(depth=0)
        return Response(
            services_serializers.CommentRecursiveSerializer(comments, many=True).data,
            status=status.HTTP_200_OK,
        )


class CommentListAndCreateView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, category_name, obj_id):
        comments = None
        if category_name == "killer":
            comments = apis_models.Killer.objects.get(
                id=obj_id
            ).category.comments.filter(depth=0)
        elif category_name == "survivor":
            comments = apis_models.Survivor.objects.get(
                id=obj_id
            ).category.comments.filter(depth=0)
        elif category_name == "perk":
            comments = apis_models.Perk.objects.get(id=obj_id).category.comments.filter(
                depth=0
            )
        elif category_name == "item":
            comments = apis_models.Item.objects.get(id=obj_id).category.comments.filter(
                depth=0
            )
        elif category_name == "addon":
            comments = apis_models.ItemAddon.objects.get(
                id=obj_id
            ).category.comments.filter(depth=0)

        if comments:
            paginator = Paginator(comments, 10)
            page_number = request.GET.get("page", 1)
            page = paginator.get_page(page_number)
            return Response(
                services_serializers.CommentRecursiveSerializer(page, many=True).data,
                status=status.HTTP_200_OK,
            )
        return Response({"error": "잘못된 접근입니다."}, status=status.HTTP_400_BAD_REQUEST)

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
                services_serializers.CommentRecursiveSerializer(comment).data,
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
