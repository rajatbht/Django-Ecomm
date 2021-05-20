from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import Cart, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password',
                  'age', 'is_active', 'is_admin', 'gender']

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'user_id','product_id','product_quantity']
