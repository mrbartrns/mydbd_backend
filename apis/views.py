from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

import apis.serializers as apis_serializers
from apis.models import Killer, Survivor, Item, ItemAddon, Perk


# Create your views here.
class KillerListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        killers = Killer.objects.all()
        paginator = Paginator(killers, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(apis_serializers.KillerListSerializer(page, many=True).data, status=HTTP_200_OK)


class SurvivorListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        survivors = Survivor.objects.all()
        paginator = Paginator(survivors, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(apis_serializers.SurvivorListSerializer(page, many=True).data, status=HTTP_200_OK)


class PerkListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        perks = Perk.objects.all()
        paginator = Paginator(perks, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(apis_serializers.PerkListSerializer(page, many=True).data, status=HTTP_200_OK)


class ItemListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        items = Item.objects.all()
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(apis_serializers.ItemListSerializer(page, many=True).data, status=HTTP_200_OK)


class ItemAddonListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        item_addons = ItemAddon.objects.all()
        paginator = Paginator(item_addons, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(apis_serializers.ItemAddonListSerializer(page, many=True).data, status=HTTP_200_OK)


class KillerDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, killer_id):
        killer = Killer.objects.get(id=killer_id)
        return Response(apis_serializers.KillerDetailSerializer(killer).data, status=HTTP_200_OK)


class SurvivorDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, survivor_id):
        survivor = Survivor.objects.get(id=survivor_id)
        return Response(apis_serializers.SurvivorDetailSerializer(survivor).data, status=HTTP_200_OK)


class PerkDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, perk_id):
        perk = Perk.objects.get(id=perk_id)
        return Response(apis_serializers.PerkDetailSerializer(perk).data, status=HTTP_200_OK)


class ItemDetailView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        return Response(apis_serializers.ItemDetailSerializer(item).data, status=HTTP_200_OK)


class ItemAddonDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, addon_id):
        addon = ItemAddon.objects.get(id=addon_id)
        return Response(apis_serializers.ItemAddonDetailSerializer(addon).data, status=HTTP_200_OK)
