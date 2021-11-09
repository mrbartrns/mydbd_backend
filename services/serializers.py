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
        except:
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
        except:
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
            "user": {"read_only": True},
        }

    def validate(self, attrs):
        if attrs["like"] and attrs["dislike"]:
            raise ValidationError(
                {"detail": "both like and dislike field must not be all True."}
            )
        return super().validate(attrs)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {
            "author": {"read_only": True}
        }  # view에서  save시 author=request.user 설정
