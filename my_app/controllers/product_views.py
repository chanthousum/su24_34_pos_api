from http import HTTPStatus
from itertools import product

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from yaml import serialize

from my_app.models import Category, Product
from my_app.my_serailizers.category_serializer import CategorySerializer
from my_app.my_serailizers.product_serializer import ProductSerializer


@api_view(["GET"])
def index(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products, many=True)
    return JsonResponse(serializer.data,safe=False)
@swagger_auto_schema(method='post', request_body=ProductSerializer)
@api_view(["POST"])
def create_product(request):
    product=Product()
    product.product_name=request.data['product_name']
    product.barcode = request.data['barcode']
    product.sell_price = request.data['sell_price']
    product.unit_in_stock = request.data['unit_in_stock']
    file_name=request.data['photo']
    category_id=request.data['category']
    if file_name is not None:
        product.photo=file_name
        data = {
            "product_name": product.product_name,
            "barcode": product.barcode,
            "sell_price": product.sell_price,
            "unit_in_stock": product.unit_in_stock,
            "photo": product.photo,
            "category": category_id
        }
        serializer = ProductSerializer(data=data)
    else:
        data = {
            "product_name": product.product_name,
            "barcode": product.barcode,
            "sell_price": product.sell_price,
            "unit_in_stock": product.unit_in_stock,
            "category": category_id
        }
        serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message":f"Product created successfully","data":serializer.data},status=HTTPStatus.CREATED)
    return JsonResponse(serializer.errors,status=HTTPStatus.BAD_REQUEST)
@api_view(["GET"])
def find_by_id(request,id):
    product=Product.objects.filter(id=id).first()
    if product is None:
        return JsonResponse({"message":f"Product not found with id:{id}"}, status=HTTPStatus.NOT_FOUND)
    serializer=ProductSerializer(product)
    return JsonResponse(serializer.data,status=HTTPStatus.OK)

name = openapi.Parameter('name',openapi.IN_QUERY,description="Search categories by name (like)",type=openapi.TYPE_STRING)
@swagger_auto_schema(method='get',manual_parameters=[name],responses={200: ProductSerializer(many=True)})
@api_view(["GET"])
def find_by_name(request):
    name=request.query_params.get('name')
    if name is None:
        return Response({"message":"product name is required"}, status=HTTPStatus.BAD_REQUEST)
    product=Category.objects.filter(product_name__icontains=name)
    if product is None:
        return Response({"message":"product not found"}, status=HTTPStatus.NOT_FOUND)
    serializer=ProductSerializer(product,many=True)
    return JsonResponse(serializer.data,safe=False,status=HTTPStatus.OK)
@api_view(["GET"])
def paginated(request):
    paginator =PageNumberPagination()
    paginator.page_size=5
    category=Category.objects.all()
    result_page=paginator.paginate_queryset(category,request)
    serializer=CategorySerializer(result_page,many=True)
    return paginator.get_paginated_response(serializer.data)
@api_view(["DELETE"])
def delete_by_id(request, id):
    product=Product.objects.filter(id=id).first()
    if product is None:
        return Response({"message":f"product not found with :{id}"}, status=HTTPStatus.NOT_FOUND)
    if product.photo:
        product.photo.delete()
    product.delete()
    return JsonResponse({"message":"Product deleted successfully"},status=HTTPStatus.OK)
@swagger_auto_schema(method='put', request_body=ProductSerializer)
@api_view(["PUT"])
def update_by_id(request, id):
    product_existing=Product.objects.filter(id=id).first()
    if product_existing is None:
        return Response({"message":f"product not found with id{id}"}, status=HTTPStatus.NOT_FOUND)

    product_existing.product_name=request.data['product_name']
    product_existing.barcode = request.data['barcode']
    product_existing.sell_price = request.data['sell_price']
    product_existing.unit_in_stock = request.data['unit_in_stock']
    file_name=request.data['photo']
    product_existing.category_id=request.data['category']

    if product_existing.photo is not None:
        if file_name is not None:
            product_existing.photo=file_name
            data = {
                "product_name": product_existing.product_name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "photo": product_existing.photo,
                "category": product_existing.category_id
            }
            serializer = ProductSerializer(product_existing, data=data)
        else:
            data = {
                "product_name": product_existing.product_name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "category": product_existing.category_id
            }
            serializer = ProductSerializer(product_existing, data=data)
    else:
        if file_name is not None:
            product.photo=file_name
            data = {
                "product_name": product_existing.product_name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "photo": product_existing.photo,
                "category": product_existing.category_id
            }
            serializer = ProductSerializer(product_existing, data=data)
        else:
            data = {
                "product_name": product_existing.product_name,
                "barcode": product_existing.barcode,
                "sell_price": product_existing.sell_price,
                "unit_in_stock": product_existing.unit_in_stock,
                "category": product_existing.category_id
            }
            serializer = ProductSerializer(product_existing, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message":f"Product updated successfully","data":serializer.data},status=HTTPStatus.OK)
    else:
        return JsonResponse(serializer.errors,status=HTTPStatus.BAD_REQUEST)


