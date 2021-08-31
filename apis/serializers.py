from rest_framework import serializers

from .models import *


class KillerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Killer
        fields = '__all__'

    def get_image(self, obj):
        images = Photo.objects.filter(photo_category__killer=obj)
        return ImageSerializer(images, many=True).data


class SurvivorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Survivor
        fields = '__all__'

    def get_image(self, obj):
        images = Photo.objects.filter(photo_category__survivor=obj)
        return ImageSerializer(images, many=True).data


class PerkSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Perk
        fields = '__all__'

    def get_image(self, obj):
        images = Photo.objects.filter(photo_category__perk=obj)
        return ImageSerializer(images, many=True).data


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    def get_image(self, obj):
        images = Photo.objects.filter(photo_category__item=obj)
        return ImageSerializer(images, many=True).data


class ItemAddonSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ItemAddon
        fields = '__all__'

    def get_image(self, obj):
        images = Photo.objects.filter(photo_category__item_addon=obj)
        return ImageSerializer(images, many=True).data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'dt_created', 'dt_modified')
