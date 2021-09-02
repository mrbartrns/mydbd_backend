from django.core.paginator import Paginator
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


# All comments of killer
class AllKillerCommentListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        comments = Comment.objects.filter(category__killer__isnull=False, depth=0)
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)


# All comments of killer=killer_id
class KillerCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, killer_id):
        self.permission_classes = [AllowAny]
        self.authentication_classes = []
        comments = Comment.objects.filter(category__killer=killer_id, depth=0)
        paginator = Paginator(comments, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(CommentRecursiveSerializer(page, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, killer_id):
        serializer = CommentPostSerializer(data=request.data)
        category = Category.objects.get(killer=killer_id)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, category=category)
            return Response(CommentRecursiveSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KillerCommentDetailView(APIView):
    def put(self, request, pk):
        comment = Comment.objects.get(id=pk)
        serializer = CommentPostSerializer(comment, data=request.data)
        # check is_staff option in future
        if comment.author != request.user:
            return Response({'author': '본인 또는 관리자만 수정이 가능합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            comment = serializer.save()
            return Response(CommentRecursiveSerializer(comment).data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # check is_staff option in future
        comment = Comment.objects.get(id=pk)
        comment.delete()
        return Response({'success': 'successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
