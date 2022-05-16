from django.contrib import admin
from .models import Item, Shipment, ItemForShipment, Weather, Location

# Register your models here.
admin.site.register(Item)
admin.site.register(Shipment)
admin.site.register(ItemForShipment)
admin.site.register(Weather)
admin.site.register(Location)