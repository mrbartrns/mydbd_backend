from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from .serializers import *


# Create your views here.
class KillerListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        killers = Killer.objects.all()
        paginator = Paginator(killers, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(KillerSerializer(page, many=True).data, status=HTTP_200_OK)


class SurvivorListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        survivors = Survivor.objects.all()
        paginator = Paginator(survivors, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(SurvivorSerializer(page, many=True).data, status=HTTP_200_OK)


class PerkListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        perks = Perk.objects.all()
        paginator = Paginator(perks, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(PerkSerializer(page, many=True).data, status=HTTP_200_OK)


class ItemListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        items = Item.objects.all()
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(ItemSerializer(page, many=True).data, status=HTTP_200_OK)


class ItemAddonListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        item_addons = ItemAddon.objects.all()
        paginator = Paginator(item_addons, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return Response(ItemAddonSerializer(page, many=True).data, status=HTTP_200_OK)
