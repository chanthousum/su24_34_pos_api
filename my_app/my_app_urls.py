
from django.contrib import admin
from django.urls import path

from my_app import views
from my_app.controllers import category_views, product_views
from my_app.swagger import schema_view

urlpatterns = [
    path('',views.home),
    #----------------route category-------------
    path("api/v1/category/",category_views.index),
    path("api/v1/category",category_views.create_category),
    path("api/v1/category/find_by_id/<id>",category_views.find_by_id),
    path("api/v1/category/find_by_name",category_views.find_by_name),
    path("api/v1/category/paginated",category_views.paginated),
    path("api/v1/category/delete_by_id/<id>",category_views.delete_category),
    path("api/v1/category/update_by_id/<id>",category_views.update_category),
    #----------------route product-------------
    path("api/v1/product/",product_views.index),
    path("api/v1/product", product_views.create_product),
    path("api/v1/product/find_by_id/<id>",product_views.find_by_id),
    path("api/v1/product/find_by_name",product_views.find_by_name),
    path("api/v1/product/paginated",product_views.paginated),
    path("api/v1/product/delete_by_id/<id>", product_views.delete_by_id),
    path("api/v1/product/update_by_id/<id>", product_views.update_by_id),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),

]
