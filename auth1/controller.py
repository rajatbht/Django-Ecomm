from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from . import views
from rest_framework import status
from ecom.tokens import checkToken


@api_view(['POST'])
def register(request):
    return views.createUser(request)


@api_view(['POST'])
def login(request):
    return views.loginUser(request)


@api_view(['GET'])
@checkToken("user")
def profile(request, CurrentUser):
    return views.getUser(request, CurrentUser['email'])

@api_view(['GET'])
@checkToken("admin")
def onlyForAdmins(request,userData):
    return JsonResponse({"ok":1}, safe=False, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@checkToken("user")
def cartDetail(request, CurrentUser):
    return views.addCart(request, CurrentUser['id'])
