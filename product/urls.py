# from django_request_mapping import UrlPattern
# from .views import UserView

# urlpatterns = UrlPattern()
# urlpatterns.register(UserView)


from django.contrib import admin
from django.urls import path
from .views import UserView

urlpatterns = [
    # path('get', UserView.getProduct),
    # path('add', UserView.createProduct)
]
