from django.db import models

# Create your models here.
class FuelStation(models.Model):
    opis_id = models.IntegerField(unique=True)

    name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=10)

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    retail_price = models.DecimalField(
        max_digits=6,
        decimal_places=3
    )

    class Meta:
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['retail_price'])
        ]