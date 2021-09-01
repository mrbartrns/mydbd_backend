from accounts.serializers import *
from apis.serializers import *
from .models import *


class CommentRecursiveSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'children', 'content', 'category', 'depth', 'dt_created', 'dt_modified')

    def get_fields(self):
        # parent에서 child를 불러올 때에는 related_name으로 불러옴
        fields = super().get_fields()
        fields['children'] = CommentRecursiveSerializer(many=True)
        return fields


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentPostSerializer(serializers.Serializer):
    parent_id = serializers.PrimaryKeyRelatedField(required=False, source='parent',
                                                   queryset=Comment.objects.all())
    content = serializers.CharField()
