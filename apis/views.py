from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


import apis.serializers as apis_serializers
from apis.models import Killer, Survivor, Item, ItemAddon, Perk
from backend.permissions import IsAuthenticatedOrReadOnly


class APIPagination(PageNumberPagination):
    page_query_param = "page"
    page_size = 10


# Create your views here.
class KillerListView(APIView, APIPagination):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = apis_serializers.KillerListSerializer

    def get(self, request):
        killers = Killer.objects.all()
        page = self.paginate_queryset(killers, request, view=self)
        # print(page)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True).data
        )
        return response


class SurvivorListView(APIView, APIPagination):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = apis_serializers.SurvivorListSerializer

    def get(self, request):
        survivors = Survivor.objects.all()
        page = self.paginate_queryset(survivors, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True).data
        )
        return response


class PerkListView(APIView, APIPagination):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = apis_serializers.PerkListSerializer

    def get(self, request):
        perks = Perk.objects.all()
        page = self.paginate_queryset(perks, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True).data
        )
        return response


class ItemListView(APIView, APIPagination):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = apis_serializers.ItemListSerializer

    def get(self, request):
        items = Item.objects.all()
        page = self.paginate_queryset(items, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True).data
        )
        return response


class ItemAddonListView(APIView, APIPagination):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = apis_serializers.ItemAddonListSerializer

    def get(self, request):
        item_addons = ItemAddon.objects.all()
        page = self.paginate_queryset(item_addons, request, view=self)
        response = self.get_paginated_response(
            self.serializer_class(page, many=True).data
        )
        return response


class KillerDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = apis_serializers.KillerDetailSerializer

    def get(self, request, killer_id):
        killer = Killer.objects.get(id=killer_id)
        return Response(
            self.serializer_class(killer, context={"request": request}).data,
            status=HTTP_200_OK,
        )


class SurvivorDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = apis_serializers.SurvivorDetailSerializer

    def get(self, request, survivor_id):
        survivor = Survivor.objects.get(id=survivor_id)
        return Response(self.serializer_class(survivor).data, status=HTTP_200_OK)


class PerkDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = apis_serializers.PerkDetailSerializer

    def get(self, request, perk_id):
        perk = Perk.objects.get(id=perk_id)
        return Response(self.serializer_class(perk).data, status=HTTP_200_OK)


class ItemDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = apis_serializers.ItemAddonListSerializer

    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        return Response(self.serializer_class(item).data, status=HTTP_200_OK)


class ItemAddonDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = apis_serializers.ItemAddonDetailSerializer

    def get(self, request, addon_id):
        addon = ItemAddon.objects.get(id=addon_id)
        return Response(self.serializer_class(addon).data, status=HTTP_200_OK)
