from django.urls import path

from apis import views

urlpatterns = [
    path('killers/list', views.KillerListView.as_view(), name="killer-list"),
    path('survivors/list', views.SurvivorListView.as_view(), name='survivor-list'),
    path('perks/list', views.PerkListView.as_view(), name='perk-list'),
    path('items/list', views.ItemListView.as_view(), name='item-list'),
    path('addons/list', views.ItemAddonListView.as_view(), name='item-addon-list-view'),
    path('killer/<int:killer_id>/detail', views.KillerDetailView.as_view(), name='killer-detail'),
    path('survivor/<int:survivor_id>/detail', views.SurvivorDetailView.as_view(), name='survivor-detail'),
    path('perk/<int:perk_id>/detail', views.PerkDetailView.as_view(), name='perk-detail'),
    path('item/<int:item_id>/detail', views.ItemDetailView.as_view(), name='item-detail'),
    path('addon/<int:addon_id>/detail', views.ItemAddonDetailView.as_view(), name='item_addon-detail')
]
