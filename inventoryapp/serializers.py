from inventoryapp.models import Product,Inventory,Sales,Invoice,Returns,Transaction
from rest_framework import serializers

class Inventory_serializer(serializers.ModelSerializer):
    class Meta:
        model =Inventory
        fields='__all__'

class Sales_serializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields=['product_id','quantity_sold']

class Returns_serializer(serializers.ModelSerializer):
    class Meta:
        model = Returns
        fields=['product_id','quantity_returned','reason']


class Invoice_serializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields='__all__'



class Product_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'