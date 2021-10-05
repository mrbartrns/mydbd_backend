"""
All List of game props do in api.serializer
"""
from rest_framework import serializers

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

    class Meta:
        model = Comment
        fields = "__all__"

    def get_children_count(self, obj):
        return obj.children.count()

    def get_is_modified(self, obj):
        return obj.dt_created == obj.dt_modified


# serializer.Serializer를 이용하여 사용하지 않아도 ModelSerializer를 불러와 원하는 field만 입력받도록 하면 된다.
class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("parent", "content")

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.parent = validated_data.get("parent", instance.parent)
