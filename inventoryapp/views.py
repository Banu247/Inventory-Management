from django.shortcuts import render
from rest_framework import viewsets
from inventoryapp.models import Inventory
from inventoryapp.serializers import Inventory_serializer

# Create your views here.

class Inventory_details(viewsets.ModelViewSet):
    serializer_class = Inventory_serializer
    queryset = Inventory.objects.all()


