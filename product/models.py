from django.db import models
from ecom.__audit__ import YourBaseClass


class Category(YourBaseClass):
    name = models.CharField(max_length=70, blank=False)

    def __str__(self):
        return str(self.id) + " : " + self.name


class Product(YourBaseClass):
    name = models.CharField(max_length=70, blank=False)
    description = models.TextField(max_length=200, blank=False)
    price = models.DecimalField(max_digits=30, decimal_places=2, blank=False)
    quantity = models.IntegerField(blank=False)
    # image = models.ImageField(upload_to='images/')
    # image = models.BinaryField(editable=True)
    category_id = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='categories', related_query_name='category')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id) + " : " + self.name
