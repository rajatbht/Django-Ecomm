from django.urls import path, include
from . import controller
urlpatterns = [
    path('register', controller.register),
    path('login', controller.login),
    path('profile', controller.profile),
    path('admin', controller.onlyForAdmins),
    path('cart', controller.cartDetail)
]
