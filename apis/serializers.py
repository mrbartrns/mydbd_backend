from services.serializers import *
from .models import *


class KillerSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Killer
        fields = '__all__'

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data

    def get_comments(self, obj):
        comments = obj.category.comments.filter(depth=0)
        return CommentRecursiveSerializer(comments, many=True).data


class SurvivorSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Survivor
        fields = '__all__'

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class PerkSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Perk
        fields = '__all__'

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class ItemSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    def get_images(self, obj):
        # images = Photo.objects.filter(photo_category__item=obj)
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class ItemAddonSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ItemAddon
        fields = '__all__'

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'dt_created', 'dt_modified')
