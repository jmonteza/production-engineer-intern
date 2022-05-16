from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Item, Shipment, ItemForShipment, Location, Weather
from django.db.models import Q
from .utils import generate_ship_code, generate_tracking_number
from .weather import get_city_weather
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
        locations = Weather.objects.all()
        return render(request, 'inventory_app/detail.html', {'item': item, 'locations': locations})
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

            location_id = request.POST.get("dropdown")

            location = Location.objects.get(pk=location_id)
            weather = Weather.objects.get(location=location)

            obj, created = Item.objects.update_or_create(pk=item_id, defaults={
                'name': name,
                'price': price,
                'quantity': quantity,
                'total': total,
                'upc': upc,
                'weather': weather,
            })
        return HttpResponseRedirect(reverse('inventory:catalog'))
        # return HttpResponse("Hello World!")

# Create an inventory item


def create(request):
    if request.method == 'GET':
        locations = Weather.objects.all()

        return render(request, 'inventory_app/add.html', {'locations':locations})
    elif request.method == 'POST':

        name = request.POST.get("name")
        price = float(request.POST.get("price"))
        quantity = int(request.POST.get("quantity"))
        total = price * quantity
        upc = request.POST.get("upc")
        location_id = request.POST.get("dropdown")

        location = Location.objects.get(pk=location_id)
        weather = Weather.objects.get(location=location)

        item = Item(name=name, price=price,
                    quantity=quantity, total=total, upc=upc, weather=weather)
        item.save()

        return HttpResponseRedirect(reverse('inventory:catalog'))

# List of items


def catalog(request):
    all_items = Item.objects.all()
    # output = ', '.join([i.name for i in all_items])
    context = {'all_items': all_items}
    return render(request, 'inventory_app/index.html', context)
    # return HttpResponse(output)


def new_shipment(request):
    if request.method == 'GET':
        return render(request, 'inventory_app/add_shipment.html')
    elif request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        company = request.POST.get("company")
        street = request.POST.get("street")
        city = request.POST.get("city")
        province = request.POST.get("province")
        postal = request.POST.get("postal")
        country = request.POST.get("country")
        ship_code = generate_ship_code()
        tracking_number = generate_tracking_number()

        Shipment.objects.create(first_name=fname, last_name=lname, company=company, street_address=street, city=city, state_province_region=province, postal_code=postal, country=country, ship_code=ship_code, tracking_number=tracking_number)

        return HttpResponseRedirect(reverse('inventory:all_shipments'))

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
        quantity = int(request.POST.get("quantity"))

        item = Item.objects.get(pk=item_id)
        shipment = Shipment.objects.get(pk=shipment_id)
        
        item.quantity = item.quantity - quantity
     
        item.save()

        obj, created = ItemForShipment.objects.update_or_create(
            item = item, shipment=shipment, defaults={
                'quantity': quantity
            }
        )



        # print(item)
        # print(quantity)

        return HttpResponseRedirect(reverse('inventory:shipments', kwargs={'shipment_id':shipment_id}))


def test_weather(request):
    locations = Location.objects.all()

    for location in locations:
        # print(location.city)
        # print(location.province)
        # print(location.country)

        name, temperature, pressure, humidity = get_city_weather(location.city)

        obj, created = Weather.objects.update_or_create(
            location=location, 
            defaults={'temperature': temperature, 'pressure': pressure, 'humidity': humidity}
        )

        # print(name, temperature, pressure, humidity)

    return HttpResponse("Hello World!")
