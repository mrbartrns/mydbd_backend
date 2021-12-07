from datetime import datetime
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
    page_query_param = "page"
    page_size = 10


class ArticlePagination(PageNumberPagination):
    page_query_param = "page"
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
    ]  # 댓글에 좋아요 눌렀는지 알기 위하여 authenticate 필요

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


# TODO: post 후 답글 까지도 생각해야 하기 때문에 pagination 방식을 변경해야 할 수도 있다.
class ArticleCommentListView(APIView, ArticleCommentPagination):
    serializer_class = services_serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        comments = article.comments.all()
        if comments is not None:
            comments = comments.annotate(
                sort_order_true=Case(When(parent=not None, then="parent"), default="id")
            ).order_by("sort_order_true")
        # 이미 정렬되어 있는 상태다. cursor based pagination은 마지막으로 불러온 id 기준으로 불러온다.
        page = self.paginate_queryset(comments, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True, context={"request": request}).data
        )
        return response


class ArticleCommentCreateView(APIView):
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
                services_serializers.CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateAndDeleteView(APIView):
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
                self.serializer_class(like).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    # TODO: sort by query 만들기
    def get(self, request):
        articles = services_models.Article.objects.all()
        page = self.paginate_queryset(articles, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, context={"request": request}, many=True).data
        )
        return response


class ArticleCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = services_serializers.ArticlePostSerializer

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
class ArticleDetailView(APIView, ArticleCommentPagination):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = services_serializers.ArticleSerializer

    def get(self, request, pk):
        article = get_object_or_404(services_models.Article, id=pk)
        # TODO: ip를 기준으로 5번 이하로 클릭했다면 조회수가 증가 -> 날짜가 바뀌면 초기화
        client_ip = get_client_ip(request)
        ip_list = services_models.SaveIp.objects.filter(
            article=pk, ip_address=client_ip
        )
        if ip_list.exists():
            client = ip_list[0]
            if client.counts < 5:
                client.counts += 1
                client.save()
                article.hit += 1
                article.save()
            # FIXME: Can't subtract offset-naive and offset-aware datetimes
            # else:
            #     date_diff = datetime.now() - client.dt_modified
            #     if date_diff >= 1:
            #         client.counts = 0
            #         client.counts += 1
            #         client.save()
            #         article.hit += 1
            #         article.save()
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
        article.delete()  # TODO: 지우지 말고 비활성화로 바꾸기
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


# TODO: 최근 검색된 순서대로 정렬하는 것으로 바꾸기, 아무것도 입력 되지 않았을 때 처리
class TagSearchView(APIView):
    """
    TagListView는 오직 Article을 post하기 전 Frontend에서
    이미 있는 List들을 검색하는데 사용되는 view 입니다.
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
