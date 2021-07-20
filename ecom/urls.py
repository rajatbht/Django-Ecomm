
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from product.views import UserView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth1/', include('auth1.urls')),
    path('product/', UserView.getProduct),
]
