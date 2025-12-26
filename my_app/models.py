from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=25, unique=True,null=False,blank=False)
class Product(models.Model):
    product_name=models.CharField(max_length=25, unique=True,null=False,blank=False)
    barcode = models.BigIntegerField( unique=True, null=False, blank=False)
    sell_price = models.FloatField(max_length=25,null=False, blank=False)
    unit_in_stock = models.IntegerField(null=False, blank=False)
    photo = models.ImageField(upload_to="media/",null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)