from django.urls import path

from .views import index, detail, catalog, create

app_name = 'inventory'

urlpatterns = [
    # path('', index, name='index'),
    path('', catalog, name='catalog'),
    path('product/<int:item_id>/', detail, name='detail'),
    path('add/', create, name='add'),
]
