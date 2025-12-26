from http import HTTPStatus

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from yaml import serialize

from my_app.models import Category
from my_app.my_serailizers.category_serializer import CategorySerializer


@api_view(["GET"])
def index(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories, many=True)
    return JsonResponse(serializer.data,safe=False)
@swagger_auto_schema(method='post', request_body=CategorySerializer)
@api_view(["POST"])
def create_category(request):
    category=Category()
    category.name=request.data['category_name']
    data={
        "category_name":category.name,
    }
    serializer=CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message":f"Category created successfully","data":serializer.data},status=HTTPStatus.CREATED)
    return JsonResponse(serializer.errors,status=HTTPStatus.BAD_REQUEST)
@api_view(["GET"])
def find_by_id(request,id):
    category=Category.objects.filter(id=id).first()
    if category is None:
        return JsonResponse({"message":f"Category not found with id:{id}"}, status=HTTPStatus.NOT_FOUND)
    serializer=CategorySerializer(category)
    return JsonResponse(serializer.data,status=HTTPStatus.OK)

name = openapi.Parameter('name',openapi.IN_QUERY,description="Search categories by name (like)",type=openapi.TYPE_STRING)
@swagger_auto_schema(method='get',manual_parameters=[name],responses={200: CategorySerializer(many=True)})
@api_view(["GET"])
def find_by_name(request):
    name=request.query_params.get('name')
    if name is None:
        return Response({"message":"category name is required"}, status=HTTPStatus.BAD_REQUEST)
    category=Category.objects.filter(category_name__icontains=name)
    if category is None:
        return Response({"message":"category not found"}, status=HTTPStatus.NOT_FOUND)
    serializer=CategorySerializer(category,many=True)
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
def delete_category(request,id):
    category=Category.objects.filter(id=id).first()
    if category is None:
        return Response({"message":f"category not found with :{id}"}, status=HTTPStatus.NOT_FOUND)
    category.delete()
    return JsonResponse({"message":"Category deleted successfully"},status=HTTPStatus.OK)
@swagger_auto_schema(method='put', request_body=CategorySerializer)
@api_view(["PUT"])
def update_category(request,id):
    category_existing=Category.objects.filter(id=id).first()
    if category_existing is None:
        return Response({"message":f"category not found with id{id}"}, status=HTTPStatus.NOT_FOUND)
    category_existing.category_name=request.data['category_name']
    data={
        "category_name":category_existing.category_name,
    }
    serializer=CategorySerializer(category_existing, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message":f"Category updated successfully","data":serializer.data},status=HTTPStatus.OK)
    else:
        return JsonResponse(serializer.errors,status=HTTPStatus.BAD_REQUEST)


