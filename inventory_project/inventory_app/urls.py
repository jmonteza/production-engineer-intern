from django.urls import path

from .views import detail, catalog, create, new_shipment, shipment_detail, shipments

app_name = 'inventory'

urlpatterns = [
    path('', catalog, name='catalog'),
    path('products/<int:item_id>/', detail, name='detail'),
    path('products/new/', create, name='add'),
    path('shipments/<int:shipment_id>/', shipment_detail, name='shipments'),
    path('shipments/', shipments, name='all_shipments'),
    path('shipments/new/', new_shipment, name='new_shipment'),
]
