from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=10, default=0.00)
    brand = models.TextField()
    image = models.URLField()
    url = models.URLField()
    supplier = models.CharField(max_length=255, default="kingship")
    decimal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field


    class Meta:
        ordering = ["brand", "name", "-price"]

    def __str__(self):
        return self.name
