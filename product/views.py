from rest_framework import generics, viewsets
from django_request_mapping import request_mapping
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.parsers import JSONParser
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from ecom.tokens import checkToken


class UserView(viewsets.ViewSet):
    @api_view(["GET"])
    def getProduct(request):
        try:
            productId = request.GET.get("id")
            if productId is None:
                existingProduct = Product.objects.all()
                product = ProductSerializer(existingProduct, many=True)
            else:
                existingProduct = Product.objects.filter(id=productId).first()
                product = ProductSerializer(existingProduct)
            if existingProduct is None:
                return JsonResponse({"message": "No Products"}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(product.data, safe=False)
        except Exception as ex:
            return JsonResponse({"error": "Internal server error"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR,)

    # @api_view(["POST"])
    # @checkToken("admin")
    # def createProduct(request, hhh):
    #     try:
    #         request = JSONParser().parse(request)
    #         product = ProductSerializer(data=request)
    #         product.is_valid(raise_exception=True)
    #         product.save()
    #         return JsonResponse(product.data, safe=False, status=status.HTTP_201_CREATED)
    #     except ValidationError:
    #         return JsonResponse(product.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    #     except ParseError:
    #         return JsonResponse({"error": "Invalid format for the request"}, status=status.HTTP_400_BAD_REQUEST,)
    #     except Exception as ex:
    #         return JsonResponse({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
