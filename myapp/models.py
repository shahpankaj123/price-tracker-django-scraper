from django.db import models

# Create your models here.
class ProductTrackDetails(models.Model):
    company_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Specify max_digits and decimal_places
    product_img = models.CharField(max_length=250)
    product_desc = models.TextField()

    def __str__(self):
        return f'{self.company_name} {self.product_name}'

