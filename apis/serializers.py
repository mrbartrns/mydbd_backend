from rest_framework import serializers

import services.serializers as services_serializers
from .models import (
    Killer,
    Survivor,
    Perk,
    Photo,
    Item,
    ItemAddon,
    ItemCategory,
    Category,
)


class KillerListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Killer
        fields = "__all__"

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


# TODO: paginate nested serializers
class KillerDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()

    class Meta:
        model = Killer
        fields = (
            "name",
            "name_kor",
            "speed",
            "images",
            "terror_radius",
            "note",
            "dt_created",
            "dt_modified",
        )

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    # def get_comments(self, obj):
    #     comments = obj.category.comments.filter(depth=0)
    #     return services_serializers.CommentSerializer


class SurvivorListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Survivor
        fields = "__all__"

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class SurvivorDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()

    class Meta:
        model = Survivor
        fields = (
            "name",
            "name_kor",
            "speed",
            "note",
            "images",
            "dt_created",
            "dt_modified",
        )

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    # def get_comments(self, obj):
    #     comments = obj.category.comments.filter(depth=0)
    #     return services_serializers.CommentRecursiveSerializer(comments, many=True).data


class PerkListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Perk
        fields = "__all__"

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class PerkDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()

    class Meta:
        model = Perk
        fields = (
            "name",
            "name_kor",
            "description",
            "images",
            "dt_created",
            "dt_modified",
        )

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    # def get_comments(self, obj):
    #     comments = obj.category.comments.filter(depth=0)
    #     return services_serializers.CommentRecursiveSerializer(comments, many=True).data


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ("name", "name_kor")


class ItemListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def get_images(self, obj):
        # images = Photo.objects.filter(photo_category__item=obj)
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class ItemDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            "name",
            "name_kor",
            "description",
            "durability",
            "rarity",
            "item_category",
            "images",
            # "comments",
            "dt_created",
            "dt_modified",
        )

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    # def get_comments(self, obj):
    #     comments = obj.category.comments.filter(depth=0)
    #     return services_serializers.CommentRecursiveSerializer(comments, many=True).data


class ItemAddonListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    item_category = ItemCategorySerializer(read_only=True)

    class Meta:
        model = ItemAddon
        fields = (
            "name",
            "name_kor",
            "description",
            "dt_created",
            "dt_modified",
            "images",
            "item_category",
        )

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class ItemAddonDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    item_category = ItemCategorySerializer(read_only=True)

    class Meta:
        model = ItemAddon
        fields = (
            "name",
            "name_kor",
            "description",
            "images",
            # "comments",
            "item_category",
            "dt_created",
            "dt_modified",
        )

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    # def get_comments(self, obj):
    #     comments = obj.category.comments.filter(depth=0)
    #     return services_serializers.CommentRecursiveSerializer(comments, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("image", "dt_created", "dt_modified")
