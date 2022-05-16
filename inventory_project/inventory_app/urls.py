from django.urls import path

from .views import index, detail, catalog, create, new_shipment, shipment_detail, shipments

app_name = 'inventory'

urlpatterns = [
    # path('', index, name='index'),
    path('', catalog, name='catalog'),
    path('product/<int:item_id>/', detail, name='detail'),
    path('add/', create, name='add'),
    path('shipments/<int:shipment_id>/', shipment_detail, name='shipments'),
    path('shipments/', shipments, name='all_shipments'),
    path('shipments/new/', new_shipment, name='new_shipment')
]
