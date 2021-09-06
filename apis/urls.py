from django.urls import path

from apis import views

urlpatterns = [
    path('list/killers', views.KillerListView.as_view(), name="killer-list"),
    path('list/survivors', views.SurvivorListView.as_view(), name='survivor-list'),
    path('list/perks', views.PerkListView.as_view(), name='perk-list'),
    path('list/items', views.ItemListView.as_view(), name='item-list'),
    path('list/addons', views.ItemAddonListView.as_view(), name='item-addon-list-view'),
    path('detail/killer/<int:killer_id>', views.KillerDetailView.as_view(), name='killer-detail'),
    path('detail/survivor/<int:survivor_id>', views.SurvivorDetailView.as_view(), name='survivor-detail'),
    path('detail/perk/<int:perk_id>', views.PerkDetailView.as_view(), name='perk-detail'),
    path('detail/item/<int:item_id>', views.ItemDetailView.as_view(), name='item-detail'),
    path('detail/addon/<int:addon_id>', views.ItemAddonDetailView.as_view(), name='item_addon-detail')
]
