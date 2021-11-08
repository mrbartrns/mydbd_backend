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
    is_modified = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    user_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Killer
        fields = "__all__"

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    def get_is_modified(self, obj):
        return obj.dt_created == obj.dt_modified

    def get_like_count(self, obj):
        return obj.category.likes.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.category.likes.filter(dislike=True).count()

    def get_user_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, like=True)
        if query.exists():
            return True
        return False

    def get_user_disliked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, dislike=True)
        if query.exists():
            return True
        return False


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
    is_modified = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    user_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Survivor
        fields = "__all__"

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    def get_is_modified(self, obj):
        return obj.dt_created == obj.dt_modified

    def get_like_count(self, obj):
        return obj.category.likes.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.category.likes.filter(dislike=True).count()

    def get_user_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, like=True)
        if query.exists():
            return True
        return False

    def get_user_disliked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, dislike=True)
        if query.exists():
            return True
        return False


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
    is_modified = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    user_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Perk
        fields = "__all__"

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    def get_is_modified(self, obj):
        return obj.dt_created == obj.dt_modified

    def get_like_count(self, obj):
        return obj.category.likes.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.category.likes.filter(dislike=True).count()

    def get_user_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, like=True)
        if query.exists():
            return True
        return False

    def get_user_disliked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, dislike=True)
        if query.exists():
            return True
        return False


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
    is_modified = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    user_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    def get_is_modified(self, obj):
        return obj.dt_created == obj.dt_modified

    def get_like_count(self, obj):
        return obj.category.likes.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.category.likes.filter(dislike=True).count()

    def get_user_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, like=True)
        if query.exists():
            return True
        return False

    def get_user_disliked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, dislike=True)
        if query.exists():
            return True
        return False


class ItemAddonListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    item_category = ItemCategorySerializer(read_only=True)

    class Meta:
        model = ItemAddon
        fields = "__all__"

    def get_images(self, obj):
        images = obj.category.photo.all()
        return ImageSerializer(images, many=True).data


class ItemAddonDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    item_category = ItemCategorySerializer(read_only=True)
    is_modified = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    user_disliked = serializers.SerializerMethodField()

    class Meta:
        model = ItemAddon
        fields = "__all__"

    def get_images(self, obj):
        image = obj.category.photo.all()
        return ImageSerializer(image, many=True).data

    def get_is_modified(self, obj):
        return obj.dt_created == obj.dt_modified

    def get_like_count(self, obj):
        return obj.category.likes.filter(like=True).count()

    def get_dislike_count(self, obj):
        return obj.category.likes.filter(dislike=True).count()

    def get_user_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, like=True)
        if query.exists():
            return True
        return False

    def get_user_disliked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        query = obj.category.likes.filter(user=user, dislike=True)
        if query.exists():
            return True
        return False


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("image", "dt_created", "dt_modified")
