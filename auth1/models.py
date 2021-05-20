from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from ecom.__audit__ import YourBaseClass
from product.models import Product
# Create your models here.


class User(YourBaseClass):
    name = models.CharField(max_length=254, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    age = models.IntegerField(
        blank=False,
        validators=[MaxValueValidator(100), MinValueValidator(18)]
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        blank=False, max_length=1, choices=GENDER_CHOICES)

    # def __str__(self):
    #     return self.email

class Cart(models.Model):
    user_id=models.IntegerField(default=0)
    product_id=models.IntegerField(default=0)
    product_quantity=models.IntegerField(default=0)
    class Meta:
        unique_together = (('user_id', 'product_id'),)
    
    # def __str__(self):
    #     return str(self.id)
