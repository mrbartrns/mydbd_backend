from django.urls import path

from .views import *

urlpatterns = [
    path('list/killers', KillerListView.as_view(), name="killer-list-view"),
    path('list/survivors', SurvivorListView.as_view(), name='survivor-list-view'),
    path('list/perks', PerkListView.as_view(), name='perk-list-view'),
    path('list/items', ItemListView.as_view(), name='item-list-view'),
    # path('list/addons', ItemAddonListView.as_view(), name='item-addon-list-view'),

]
