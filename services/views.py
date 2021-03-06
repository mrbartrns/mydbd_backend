from datetime import datetime
from django.core.paginator import Paginator as DjangoPaginator
from django.db.models import Case, When
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
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

TRUE = "true"
FALSE = "false"

# Comment Pagination
class CommentPagination(PageNumberPagination):
    # TODO: change page_query_param page -> cp
    page_query_param = "cp"
    page_size_query_param = "pagesize"
    page_size = 10


class ArticlePagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pagesize"
    page_size = 30


class ArticleCommentPagination(PageNumberPagination):
    page_query_param = "cp"
    page_size_query_param = "pagesize"
    page_size = 100


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


def get_client_ip(request):
    ip = None
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


# Create your views here.
class CommentListView(APIView, CommentPagination):
    serializer_class = services_serializers.CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # ????????? ????????? ???????????? ?????? ????????? authenticate ??????

    def get(self, request, category_name, obj_id):
        """
        query_string??? ?????? depth??? ??????????????? view
        """
        serializer = self.serializer_class
        parent = request.GET.get("parent", None)
        # TODO: ????????? like??? ????????? ????????????. ????????? ??????????????? ??????
        sortby = request.GET.get("sortby", "recent")
        comments = get_comments_by_category_name_and_object_id(category_name, obj_id)

        # root ?????? ?????? child ????????? ????????????.
        if parent:
            comments = comments.filter(parent=parent)
        else:
            comments = comments.filter(depth=0)

        # ????????? ??????????????? ????????????.
        if sortby == "id":
            comments = comments.order_by("id")
        elif sortby == "recent":
            comments = comments.order_by("-id")
        elif sortby == "like":
            pass
        page = self.paginate_queryset(comments, request, view=self)
        response = self.get_paginated_response(
            serializer(page, many=True, context={"request": request}).data
        )
        return response


class CommentCreateView(APIView):
    serializer_class = services_serializers.CommentPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, category_name, obj_id):
        serializer = self.serializer_class(data=request.data)

        category = get_category_object(category_name, obj_id)

        if category and serializer.is_valid():
            data = serializer.validated_data
            parent = data.get("parent", None)
            if parent and parent.parent:
                return Response(
                    {"detail": "bad request"}, status=status.HTTP_400_BAD_REQUEST
                )
            comment = serializer.save(author=request.user, category=category)
            return Response(
                services_serializers.CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleCommentListView(APIView, ArticleCommentPagination):
    serializer_class = services_serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        comments = article.comments.all()
        if comments is not None:
            comments = comments.annotate(
                sort_order_true=Case(
                    When(parent__isnull=False, then="parent"), default="id"
                )
            ).order_by("sort_order_true")
        page = self.paginate_queryset(comments, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True, context={"request": request}).data
        )
        return response


# ????????? post ??? ????????? ????????? ????????? ???????????? ?????? ????????? ???????????? ???????????? ??????.
# ?????? pagesize??? post??? ?????? ?????? ???, pagesize??? ?????? ??? ?????? ???????????? ???????????? ????????????.
class ArticleCommentCreateView(APIView, ArticleCommentPagination):
    model_class = services_models.Comment
    serializer_class = services_serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        article = get_object_or_404(services_models.Article, id=pk)
        if serializer.is_valid():
            data = serializer.validated_data
            parent = data.get("parent", None)
            if parent and parent.parent:
                return Response(
                    {"detail": "bad request"}, status=status.HTTP_400_BAD_REQUEST
                )
            comment = serializer.save(author=request.user, article=article)
            return Response(
                self.serializer_class(comment).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateView(APIView):
    """
    CommentUpdateAndDeleteView can be used everywhere using comment serializer.
    """

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

    # def delete(self, request, pk):
    #     comment = services_models.Comment.objects.get(id=pk)
    #     self.check_object_permissions(request, comment)
    #     comment.delete()
    #     return Response(
    #         {"success": "successfully deleted."}, status=status.HTTP_202_ACCEPTED
    #     )


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
                # True, False ????????? Frontend?????? ??????
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
                self.serializer_class(like).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    permission_class = [IsOwnerOrStaff]
    serializer_class = services_serializers.CommentSerializer
    model_class = services_models.Comment

    def post(self, request, pk):
        comment = get_object_or_404(self.model_class, id=pk)
        self.check_object_permissions(request, comment)
        comment.is_deleted = True
        comment.save()
        return Response(self.serializer_class(comment).data, status=status.HTTP_200_OK)


class DetailLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = services_serializers.LikeSerializer

    def post(self, request, category_name, obj_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            category = get_category_object(category_name, obj_id)
            likes = services_models.Like.objects.filter(
                category=category, user=request.user
            )
            if likes.exists():
                like = likes[0]
                like.like = False
                like.dislike = False
                if serializer.validated_data.get("like"):
                    like.like = True
                elif serializer.validated_data.get("dislike"):
                    like.dislike = True
                like.save()
                return Response(
                    self.serializer_class(like).data, status=status.HTTP_202_ACCEPTED
                )
            like = serializer.save(category=category, user=request.user)
            return Response(
                self.serializer_class(like).data, status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# service/forum/list
class ArticleListView(APIView, ArticlePagination):
    permission_classes = [AllowAny]
    serializer_class = services_serializers.ArticleSerializer

    # TODO: sort by query ?????????
    def get(self, request):
        articles = services_models.Article.objects.all()
        page = self.paginate_queryset(articles, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, context={"request": request}, many=True).data
        )
        return response


class ArticleCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = services_serializers.ArticleSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            article = serializer.save(author=request.user)
            return Response(
                self.serializer_class(article).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleUpdateView(APIView):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = services_serializers.ArticlePostSerializer

    def get(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        return Response(self.serializer_class(article).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        serializer = self.serializer_class(instance=article, data=request.data)
        self.check_object_permissions(request, article)
        if serializer.is_valid():
            article = serializer.save()
            return Response(
                self.serializer_class(article).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: test post, get, delete first and after put
class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = services_serializers.ArticleSerializer

    def get(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        # TODO: ip??? ???????????? 5??? ????????? ??????????????? ???????????? ?????? -> ????????? ????????? ?????????
        client_ip = get_client_ip(request)
        ip_list = services_models.SaveIp.objects.filter(
            article=pk, ip_address=client_ip
        )
        if ip_list.exists():
            client = ip_list[0]
            # if client.counts < 5:
            client.counts += 1
            client.save()
            article.hit += 1
            article.save()
        else:
            client = services_models.SaveIp.objects.create(
                ip_address=client_ip, article=article
            )
            client.counts += 1
            client.save()
            article.hit += 1
            article.save()
        return Response(
            self.serializer_class(article, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        serializer = self.serializer_class(article, data=request.data)
        self.check_object_permissions(request, article)
        if serializer.is_valid():
            article = serializer.save()
            return Response(
                self.serializer_class(article).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        self.check_object_permissions(request, article)
        article.delete()  # TODO: ????????? ?????? ??????????????? ?????????
        return Response({"detail": _("successfully deleted.")})


class ArticleLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = services_serializers.LikeSerializer
    error_message = _("You have been liked this article.")

    def get(self, request, pk):
        return Response({"here": "here"}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            article = services_serializers.Article.objects.get(id=pk)
            likes = article.likes.filter(user=request.user)
            if likes.exists():
                like = likes[0]
                like.like = False
                like.dislike = False
                if serializer.validated_data.get("like"):
                    like.like = True
                elif serializer.validated_data.get("dislike"):
                    like.dislike = True
                like.save()
                return Response(
                    self.serializer_class(like).data, status=status.HTTP_202_ACCEPTED
                )
                # return Response(
                #     {"detail": self.error_message}, status=status.HTTP_400_BAD_REQUEST
                # )
            like = serializer.save(article=article, user=request.user)
            return Response(
                self.serializer_class(like).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: ?????? ????????? ???????????? ???????????? ????????? ?????????, ???????????? ?????? ?????? ????????? ??? ??????
class TagSearchView(APIView):
    """
    TagListView??? ?????? Article??? post?????? ??? Frontend??????
    ?????? ?????? List?????? ??????????????? ???????????? view ?????????.
    """

    permission_classes = [AllowAny]
    serializer_class = services_serializers.TagSerializer

    def get(self, request):
        name = request.query_params.get("tag_name")
        result = services_models.Tag.objects.filter(name__contains=name).order_by(
            "-id"
        )[:10]
        return Response(
            self.serializer_class(result, many=True).data, status=status.HTTP_200_OK
        )


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = services_serializers.ImageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            return Response(
                self.serializer_class(image).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
