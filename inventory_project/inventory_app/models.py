from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=255)

    price = models.FloatField(validators=[MinValueValidator(0.0)])

    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    # Price x Quantity
    total = models.FloatField(validators=[MinValueValidator(0.0)])

    # 13 for International Article Number (European Article Number or EAN)
    upc = models.CharField(max_length=13)


    def __str__(self):
        return "{} | {}".format(self.id, self.name)