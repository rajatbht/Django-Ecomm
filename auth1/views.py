from django.db.models.fields.related import ManyToManyField
from rest_framework.exceptions import ParseError
from product.models import Product
from django import db
from django.shortcuts import render
from .models import User,Cart
from .serializers import UserSerializer,CartSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http.response import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from ecom.tokens import createToken
from product.serializers import ProductSerializer


def createUser(request):
    try:
        request = JSONParser().parse(request)
    except:
        return JsonResponse({"error": "Invalid format for the request"}, status=status.HTTP_400_BAD_REQUEST)
    user = UserSerializer(data=request)
    if user.is_valid():
        print(user.validated_data['password'])
        hashedPassword = make_password(user.validated_data['password'])
        user.validated_data['password'] = hashedPassword
        user.save()
        return JsonResponse(user.data, status=status.HTTP_202_ACCEPTED)
    else:
        print('Error' + str(user.errors))
        return JsonResponse(user.errors, status=status.HTTP_400_BAD_REQUEST)


def loginUser(request):
    try:
        request = JSONParser().parse(request)
    except:
        return JsonResponse({"error": "Invalid format for the request"}, status=status.HTTP_400_BAD_REQUEST)

    existingUsersList = User.objects.filter(email=request['email'])
    if existingUsersList.count() == 0:
        return JsonResponse({'message': 'No user exist'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
    existingUser = UserSerializer(existingUsersList[0])
    existingPassword = existingUser['password'].value
    print(existingPassword)
    recieve_pswd = request['password']
    print("PasswordMatch? : " + str(check_password(recieve_pswd, existingPassword)))
    if check_password(recieve_pswd, existingPassword):
        payload = {
            'email': request['email'],
            'id' : existingUser['id'].value
        }
        if existingUser['is_active'].value:
            token = createToken(payload)
            response = {'message': 'login success',
                        'token': token}
            return JsonResponse(response, safe=False, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({'message': 'user is not activated pls check the email we sent and activate yourself !!'}, safe=False, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'password doesnt match'}, safe=False, status=status.HTTP_400_BAD_REQUEST)


def getUser(request, email):
    user = User.objects.filter(email=email)
    response = UserSerializer(user, many=True)
    return JsonResponse(data=response.data, safe=False, status=status.HTTP_202_ACCEPTED)

def addCart(request, user_id):
    try:
        request = JSONParser().parse(request)
        print(request)
        request["user_id"]=user_id
        cart_obj=Cart.objects.filter(user_id=user_id, product_id=request["product_id"])
        if cart_obj.count()>0:
            cart = Cart.objects.get(user_id=user_id, product_id=request["product_id"])
            print(f"product quatity before: {cart.product_quantity}")
            cart.product_quantity+=request["product_quantity"]
            print(f"product quatity After: {cart.product_quantity}")
            cart.save()
            return JsonResponse(f"updated product_quantity to {cart.product_quantity}", safe=False, status=status.HTTP_202_ACCEPTED)
        cart = CartSerializer(data=request)
        if cart.is_valid():
            print("if")
            print(cart._validated_data)
            cart.save()
            print("aaaaaaaaaaaaa")
            return JsonResponse(cart.data, safe=False, status=status.HTTP_202_ACCEPTED)
        else:
            print("else")
            print(cart.errors)
            return JsonResponse(cart.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    except ParseError:
        return JsonResponse({"error": "Invalid format for the request"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        print(ex)
        return JsonResponse({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def getCart(request, user_id):
    user = Cart.objects.filter(user_id=user_id)
    response = CartSerializer(user, many=True)
    fullCart=[]
    print(len(response.data))
    for no in range(0,len(response.data)):
        productID=response.data[no]["product_id"]
        productQuantity=response.data[no]["product_quantity"]
        product=Product.objects.filter(id=productID)
        productJson= ProductSerializer(product, many=True)
        print(1)
        # print(productJson.data[0]['name'])
        # mmm = {}
        # mmm['name'] = productJson.data[0]['name']
        # print(mmm)
        mmm = {
                "name":productJson.data[0]['name'],
                "description":productJson.data[0]['description'],
                "price":productJson.data[0]['price'],
                "productQuantity":productQuantity,
        }
        print(2)
        fullCart.append(mmm)
    print(fullCart)
    return JsonResponse(data=fullCart, safe=False, status=status.HTTP_202_ACCEPTED)

def changePswd(request, email):
    try:
        request = JSONParser().parse(request)
    except:
        return JsonResponse({"error": "Invalid format for the request"}, status=status.HTTP_400_BAD_REQUEST)
    if request['new password']==request['confirm password']:
        print(1111111)
        existingUserObj = User.objects.filter(email=email)
        print(existingUserObj[0].password)
        dbPassword = existingUserObj[0].password
        print(dbPassword)
        current_pswd = request['current password']
        print("PasswordMatch? : " + str(check_password(current_pswd, dbPassword)))
        if check_password(current_pswd, dbPassword):
            hashedPassword = make_password(request['new password'])
            print(hashedPassword)
            getExistingUserObj = User.objects.get(email=email)
            getExistingUserObj.password=hashedPassword
            getExistingUserObj.save()
            print(getExistingUserObj.password)
            return JsonResponse("Password Changed Successfully!!", safe=False, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({"error": "Current password incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"error": "New Password does not match with the Confirm Password"}, status=status.HTTP_400_BAD_REQUEST)
    