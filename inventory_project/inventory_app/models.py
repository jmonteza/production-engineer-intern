from pyexpat import model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Location(models.Model):
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    country = models.CharField(max_length=64)

    def __str__(self):
        return "{}, {}, {}".format(self.city, self.province, self.country)


class Weather(models.Model):
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, primary_key=True)
    temperature = models.FloatField(validators=[MinValueValidator(0.0)])
    pressure = models.IntegerField(validators=[MinValueValidator(0)])
    humidity = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return "{} | {} | Temp: {}, Pressure: {}, Humidity: {}".format(self.location.id, self.location, self.temperature, self.pressure, self.humidity)


class Shipment(models.Model):
    first_name = models.CharField(max_length=32)

    last_name = models.CharField(max_length=32)

    company = models.CharField(max_length=32)

    street_address = models.CharField(max_length=64)

    city = models.CharField(max_length=32)

    state_province_region = models.CharField(max_length=32)

    postal_code = models.CharField(max_length=32)

    country = models.CharField(max_length=32)

    ship_code = models.CharField(max_length=20)

    tracking_number = models.CharField(max_length=20)

    def __str__(self):
        return "{} | {}".format(self.id, self.ship_code)


class Item(models.Model):
    name = models.CharField(max_length=255)

    price = models.FloatField(validators=[MinValueValidator(0.0)])

    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    # Price x Quantity
    total = models.FloatField(validators=[MinValueValidator(0.0)])

    # 13 for International Article Number (European Article Number or EAN)
    upc = models.CharField(max_length=13)

    # City + Weather
    weather = models.ForeignKey(
        Weather, default=1, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} | {}".format(self.id, self.name)


class ItemForShipment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return "{} | {}".format(self.item.name, self.shipment.ship_code)
