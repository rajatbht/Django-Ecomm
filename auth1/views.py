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
    recieve_pswd = request['password']
    print("PasswordMatch? : " + str(check_password(recieve_pswd, existingPassword)))
    if check_password(recieve_pswd, existingPassword):
        payload = {
            'email': request['email'],
            'id' : existingUser['id'].value
        }
        token = createToken(payload)
        response = {'message': 'login success',
                    'token': token}
        return JsonResponse(response, safe=False, status=status.HTTP_202_ACCEPTED)
    else:
        return JsonResponse({'message': 'password doesnt match'}, safe=False, status=status.HTTP_400_BAD_REQUEST)


def getUser(request, email):
    user = User.objects.filter(email=email)
    response = UserSerializer(user, many=True)
    return JsonResponse(data=response.data, safe=False, status=status.HTTP_202_ACCEPTED)

def addCart(request, user_id):
    try:
        request = JSONParser().parse(request)
        request["user_id"]=user_id
        user = User.objects.get(id=user_id)
        print(user)
        cart = Cart.objects.get(user_id=user)
        print(cart)
        # print(cart['id'])
        # print(cart.product_id)

        
        productId = request['product_id']
        product = Product.objects.get(id=productId)
        print(product)
        cart.product_id.add(product)
        print(1)
        cart = CartSerializer(data=cart)
        print(cart)
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
    # products = Product.objects.filter(id=request['product_id'])
    # request['product_id'] = products
    # P_id = CartSerializer(data=request)
    # print(P_id)
    # if P_id.is_valid():
    #     print("in valid")
    #     # P_id.save()
    #     return JsonResponse("HIIIIIIIII", safe=False, status=status.HTTP_202_ACCEPTED)
    # else:
    #     return JsonResponse(P_id.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

# def getAllUsers():
#     all_users=User.objects.all()
#     all_users_Json=UserSerializer(all_users)
#     return JsonResponse(data=all_users_Json.data,status=status.HTTP_202_ACCEPTED)


# def deleteAllUsers():
#     all_deleted_users=User.objects.all().delete()
#     return JsonResponse({'message':'{} Users deleted successfully!'.format(all_deleted_users)} ,status=status.HTTP_204_NO_CONTENT)

# def deleteByID(id):
#     current_deleted_user=User.objects.filter(id=id).delete()
#     return JsonResponse({'message':'{} User deleted successfully!'.format(current_deleted_user)} ,status=status.HTTP_204_NO_CONTENT)
