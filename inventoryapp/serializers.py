from inventoryapp.models import Product,Inventory,Sales,Invoice,Returns,Transaction
from rest_framework import serializers

class Inventory_serializer(serializers.ModelSerializer):
    class Meta:
        model =Inventory
        fields='__all__'

class Sales_serializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields=['transcation','product','quantity_sold']

class Returns_serializer(serializers.ModelSerializer):
    class Meta:
        model = Returns
        fields='__all__'