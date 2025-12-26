from django.db.models import fields
from rest_framework import serializers

from my_app.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'