from accounts.serializers import *
from apis.serializers import *
from .models import *

#
# class ParentCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     author = UserSerializer(read_only=True)
#     parent = ParentCommentSerializer(read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = '__all__'
#
#
# class CommentPostSerializer(serializers.Serializer):
#     content = serializers.CharField()
#     parent = CommentSerializer(required=False, allow_null=True)