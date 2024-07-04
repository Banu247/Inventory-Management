from inventoryapp.models import Product,Inventory,Sales,Invoice,Returns,Transaction
from rest_framework import serializers

class Inventory_serializer(serializers.ModelSerializer):
    class Meta:
        model =Inventory
        fields='__all__'