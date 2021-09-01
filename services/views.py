from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


# Create your views here.
class KillerCommentRecursiveListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        comments = Comment.objects.filter(category__killer__isnull=False, depth=0)
        return Response(CommentRecursiveSerializer(comments, many=True).data, status=status.HTTP_200_OK)


class KillerCommentListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        comments = Comment.objects.filter(category__killer__isnull=False, depth=0)
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)


class CreateOrModifyKillerCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, killer_id):
        serializer = CommentPostSerializer(data=request.data)
        category = Category.objects.get(killer=killer_id)
        if serializer.is_valid():
            print(serializer.validated_data)
            comment = Comment.objects.create(author=request.user, category=category, **serializer.validated_data)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
