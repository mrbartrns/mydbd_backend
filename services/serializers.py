from accounts.serializers import *
from .models import *


class CommentRecursiveSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'children', 'content', 'category', 'depth', 'dt_created', 'dt_modified')

    def get_fields(self):
        fields = super().get_fields()
        fields['children'] = CommentRecursiveSerializer(many=True)
        return fields
