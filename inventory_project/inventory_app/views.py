from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Item, Shipment, ItemForShipment
from django.db.models import Q

# Create your views here.


def index(request):
    return HttpResponse("Hello World!")

# Item Detail


def detail(request, item_id):
    # try:
    #     item = Item.objects.get(pk=item_id)
    # except Item.DoesNotExist:
    #     raise Http404("Item does not exist")
    # return render(request, 'inventory_app/detail.html', {'item': item})
    if request.method == 'GET':
        item = get_object_or_404(Item, pk=item_id)
        return render(request, 'inventory_app/detail.html', {'item': item})
    elif request.method == 'POST':
        print(item_id)
        if request.POST.get("action") == "delete":
            item = Item.objects.get(pk=item_id)
            item.delete()
        else:

            name = request.POST.get("name")
            price = float(request.POST.get("price"))
            quantity = int(request.POST.get("quantity"))
            total = price * quantity
            upc = request.POST.get("upc")

            obj, created = Item.objects.update_or_create(pk=item_id, defaults={
                'name': name,
                'price': price,
                'quantity': quantity,
                'total': total,
                'upc': upc,
            })
        return HttpResponseRedirect(reverse('inventory:catalog'))
        # return HttpResponse("Hello World!")

# Create an inventory item


def create(request):
    if request.method == 'GET':
        return render(request, 'inventory_app/add.html')
    elif request.method == 'POST':
        name = request.POST.get("name")
        price = float(request.POST.get("price"))
        quantity = int(request.POST.get("quantity"))
        total = price * quantity
        upc = request.POST.get("upc")

        item = Item(name=name, price=price,
                    quantity=quantity, total=total, upc=upc)
        item.save()

        return HttpResponseRedirect(reverse('inventory:catalog'))

# List of items


def catalog(request):
    all_items = Item.objects.all()
    # output = ', '.join([i.name for i in all_items])
    context = {'all_items': all_items}
    return render(request, 'inventory_app/index.html', context)
    # return HttpResponse(output)


def shipments(request):
    shipments = Shipment.objects.all()
    print(shipments)
    return render(request, 'inventory_app/shipments.html', {'shipments': shipments})

def shipment_detail(request, shipment_id):

    if request.method == 'GET':

        shipment = get_object_or_404(Shipment, pk=shipment_id)

        items = ItemForShipment.objects.filter(shipment__pk=shipment_id)

        item_ids = [item.item.id for item in items]

        # print(item_ids)

        # for item in items:
            # print(item.item.name)


        catalog = Item.objects.exclude(id__in=item_ids)

        # catalog = Item.objects.all()

        # print(catalog[0].id)

        return render(request, 'inventory_app/shipment.html', {'items': items, 'shipment': shipment, 'catalog': catalog})
    
    else:
        item_id = request.POST.get("dropdown")
        quantity = request.POST.get("quantity")

        item = Item.objects.get(pk=item_id)
        shipment = Shipment.objects.get(pk=shipment_id)
        
        obj, created = ItemForShipment.objects.update_or_create(
            item = item, shipment=shipment, defaults={
                'quantity': quantity
            }
        )

        # print(item)
        # print(quantity)

        return HttpResponseRedirect(reverse('inventory:shipments', kwargs={'shipment_id':1}))
