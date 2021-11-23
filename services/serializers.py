"""
All List of game props do in api.serializer
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import accounts.serializers as accounts_serializers
from .models import *


class CommentRecursiveSerializer(serializers.ModelSerializer):
    author = accounts_serializers.UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "children",
            "content",
            "category",
            "depth",
            "dt_created",
            "dt_modified",
        )

    def get_fields(self):
        # parent에서 child를 불러올 때에는 related_name으로 불러옴, depth 차이가 1일 때에만 가능
        fields = super().get_fields()
        fields["children"] = CommentRecursiveSerializer(many=True)
        return fields


class CommentSerializer(serializers.ModelSerializer):
    children_count = serializers.SerializerMethodField()
    is_modified = serializers.SerializerMethodField()
    author = accounts_serializers.UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    user_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True},
            "depth": {"read_only": True},
            "category": {"read_only": True},
        }

    def get_children_count(self, obj):
        return obj.children.count()

    def get_is_modified(self, obj):
        return obj.dt_created == obj.dt_modified

    def get_like_count(self, obj):
        return obj.likes.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.likes.filter(dislike=True).count()

    def get_user_liked(self, obj, **kwargs):
        try:
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            query = obj.likes.filter(user=user, like=True)
            if query.exists():
                return True
            return False
        except TypeError:
            return False

    def get_user_disliked(self, obj):
        try:
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
            query = obj.likes.filter(user=user, dislike=True)
            if query.exists():
                return True
            return False
        except TypeError:
            return False

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance


# serializer.Serializer를 이용하여 사용하지 않아도 ModelSerializer를 불러와 원하는 field만 입력받도록 하면 된다.
class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("parent", "content")

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        # if not changing parent, lowerline is no longer needed
        # instance.parent = validated_data.get("parent", instance.parent)
        instance.save()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        extra_kwargs = {
            "category": {"read_only": True},
            "comment": {"read_only": True},
            "article": {"read_only": True},
            "user": {"read_only": True},
        }

    def validate(self, attrs):
        if attrs.get("like", False) and attrs.get("dislike", False):
            raise ValidationError(
                {"detail": "both like and dislike field must not be all True."}
            )
        return super().validate(attrs)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


# TODO: Add user_like field and disliked field on serializer
class ArticleSerializer(serializers.ModelSerializer):

    author = accounts_serializers.UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    dislike_count = serializers.SerializerMethodField(read_only=True)
    user_liked = serializers.SerializerMethodField(read_only=True)
    user_disliked = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, required=False)
    comments = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True}
        }  # view에서  save시 author=request.user 설정

    def get_like_count(self, obj):
        return obj.likes.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.likes.filter(dislike=True).count()

    def get_user_liked(self, obj):
        try:
            user = None
            request = self.context.get("request")
            if request.user:
                user = request.user
            likes = obj.likes.filter(user=user, like=True)
            if likes.exists():
                return True
            return False
        except:
            return False

    def get_user_disliked(self, obj):
        try:
            user = None
            request = self.context.get("request")
            if request.user:
                user = request.user
            likes = obj.likes.filter(user=user, like=True)
            if likes.exists():
                return True
            return False
        except:
            return False

    def get_comments(self, obj):
        comments = self.context.get("comments")
        serializer = CommentSerializer(comments, many=True).data
        return serializer

    # article comment count
    def get_count(self, obj):
        return obj.comments.count()

    # TODO: 무결하게 코드 작성
    def create(self, validated_data):
        tags = validated_data.get("tags", [])
        if "tags" in validated_data:
            validated_data.pop("tags")
        article = Article.objects.create(**validated_data)
        for tag in tags:
            # FIXME: 같은 Tag가 계속해서 생기지 않게 수정
            tag = Tag(**tag)
            if not Tag.objects.filter(name=tag.name).exists():
                tag.save()
            else:
                tag = Tag.objects.get(name=tag.name)
            article.tags.add(tag)
        return article

    # TODO: TEST required
    def update(self, instance, validated_data):
        tags = validated_data.get("tags", [])
        if "tags" in validated_data:
            validated_data.pop("tags")
        instance.tags.clear()
        for tag in tags:
            tag = Tag(**tag)
            if not Tag.objects.filter(name=tag).exists():
                tag.save()
            instance.tags.add(tag)
        return super().update(instance, validated_data)
