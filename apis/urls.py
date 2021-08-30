from django.urls import path

from .views import *

urlpatterns = [
    path('list/killers', KillerListView.as_view(), name="killer-list"),
    path('list/survivors', SurvivorListView.as_view(), name='survivor-list'),
    path('list/perks', PerkListView.as_view(), name='perk-list'),
    path('list/items', ItemListView.as_view(), name='item-list'),
    path('list/addons', ItemAddonListView.as_view(), name='item-addon-list-view'),
    path('detail/killer/<int:killer_id>', KillerDetailView.as_view(), name='killer-detail'),
    path('detail/survivor/<int:survivor_id>', SurvivorDetailView.as_view(), name='survivor-detail'),
    path('detail/perk/<int:perk_id>', PerkDetailView.as_view(), name='perk-detail'),
    path('detail/item/<int:item_id>', ItemDetailView.as_view(), name='item-detail'),
    path('detail/item-addon/<int:addon_id>', ItemAddonDetailView.as_view(), name='item_addon-detail')
]
