from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Item, Shipment, ItemForShipment, Location, Weather
from .utils import generate_ship_code, generate_tracking_number
from .weather import get_city_weather
import threading


def detail(request, item_id):
    '''
    View for a specific inventory item

            Parameters:
                    request (HttpRequest): HttpRequest object that contains metadata about the request
                    item_id (int): ID of the inventory item

            Returns:
                    HttpResponseRedirect: Redirect the response
    '''

    if request.method == 'GET':
        item = get_object_or_404(Item, pk=item_id)
        locations = Weather.objects.all()
        return render(request, 'inventory_app/detail.html', {'item': item, 'locations': locations})

    elif request.method == 'POST':

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


def create(request):
    '''
    View for adding an inventory item

            Parameters:
                    request (HttpRequest): HttpRequest object that contains metadata about the request

            Returns:
                    HttpResponseRedirect: Redirect the response
    '''

    if request.method == 'GET':
        locations = Weather.objects.all()
        return render(request, 'inventory_app/add.html', {'locations': locations})

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


def fetch_weather():
    '''
    View for fetching and updating the weather for 5 cities

            Parameters:
                    None

            Returns:
                    None
    '''

    locations = Location.objects.all()

    for location in locations:
        _, temperature, pressure, humidity = get_city_weather(location.city)

        obj, created = Weather.objects.update_or_create(
            location=location,
            defaults={'temperature': temperature,
                      'pressure': pressure, 'humidity': humidity}
        )

    return None


def catalog(request):
    '''
    View for inventory items

            Parameters:
                    request (HttpRequest): HttpRequest object that contains metadata about the request

            Returns:
                    render (HttpResponse): Returns an HttpResponse object of the given template rendered with the given context.
    '''

    thread = threading.Thread(target=fetch_weather)
    thread.start()
    all_items = Item.objects.filter(quantity__gt=0)
    context = {'all_items': all_items}
    return render(request, 'inventory_app/index.html', context)


def new_shipment(request):
    '''
    View for creating a new shipment

            Parameters:
                    request (HttpRequest): HttpRequest object that contains metadata about the request

            Returns:
                    HttpResponseRedirect: Redirect the response
    '''

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

        Shipment.objects.create(first_name=fname, last_name=lname, company=company, street_address=street, city=city,
                                state_province_region=province, postal_code=postal, country=country, ship_code=ship_code, tracking_number=tracking_number)

        return HttpResponseRedirect(reverse('inventory:all_shipments'))


def shipments(request):
    '''
    View for all shipments

            Parameters:
                    request (HttpRequest): HttpRequest object that contains metadata about the request

            Returns:
                    render (HttpResponse): Returns an HttpResponse object of the given template rendered with the given context.
    '''
    shipments = Shipment.objects.all()
    return render(request, 'inventory_app/shipments.html', {'shipments': shipments})


def shipment_detail(request, shipment_id):
    '''
    View for a specific shipment

            Parameters:
                    request (HttpRequest): HttpRequest object that contains metadata about the request
                    shipment_id: ID for a specific shipment
            Returns:
                    render (HttpResponse): Returns an HttpResponse object of the given template rendered with the given context.
    '''
    if request.method == 'GET':

        shipment = get_object_or_404(Shipment, pk=shipment_id)

        items = ItemForShipment.objects.filter(shipment__pk=shipment_id)

        item_ids = [item.item.id for item in items]

        catalog = Item.objects.exclude(
            id__in=item_ids).exclude(quantity__lte=0)

        return render(request, 'inventory_app/shipment.html', {'items': items, 'shipment': shipment, 'catalog': catalog})

    elif request.method == 'POST' and request.POST.get("delete"):

        id = request.POST.get("delete")
        item = Item.objects.get(pk=id)
        shipment = Shipment.objects.get(pk=shipment_id)
        itemForShipment = ItemForShipment.objects.get(
            item=item, shipment=shipment)

        item.quantity = item.quantity + itemForShipment.quantity
        item.total = item.price * item.quantity

        item.save()

        itemForShipment.delete()

        return HttpResponseRedirect(reverse('inventory:shipments', kwargs={'shipment_id': shipment_id}))

    elif request.method == 'POST' and request.POST.get("delete_shipment"):

        shipment_id = request.POST.get("delete_shipment")

        shipment = Shipment.objects.get(id=shipment_id)

        shipment.delete()

        return HttpResponseRedirect(reverse('inventory:all_shipments'))

    else:
        item_id = request.POST.get("dropdown")
        quantity = int(request.POST.get("quantity"))

        item = Item.objects.get(pk=item_id)
        shipment = Shipment.objects.get(pk=shipment_id)

        item.quantity = item.quantity - quantity
        item.total = item.price * item.quantity

        item.save()

        obj, created = ItemForShipment.objects.update_or_create(
            item=item, shipment=shipment, defaults={
                'quantity': quantity
            }
        )

        return HttpResponseRedirect(reverse('inventory:shipments', kwargs={'shipment_id': shipment_id}))
