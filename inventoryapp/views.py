from django.shortcuts import render
from rest_framework import viewsets
from inventoryapp.models import Inventory,Sales,Product,Transaction,Returns
from inventoryapp.serializers import Inventory_serializer,Sales_serializer,Returns_serializer
from drf_spectacular.views import extend_schema
from rest_framework.response import Response

# Create your views here.
@extend_schema(request=Inventory_serializer,responses=Inventory_serializer, tags=['inventory'])

class Inventory_details(viewsets.ModelViewSet):
    serializer_class = Inventory_serializer
    queryset = Inventory.objects.all()

class Sales_info(viewsets.ViewSet):
    def list(self,request):
        all_data =Sales.objects.all()
        serialiser= Sales_serializer(all_data,many=True)

        return Response(serialiser.data)

@extend_schema(request=Sales_serializer,responses=Sales_serializer, tags=['sales'])

class SalesInventory(viewsets.ViewSet):
    print("===================")
    def create(self,request):
        product_id = request.data.get('product') 
        print(product_id)
        quantity_sold= request.data.get('quantity_sold')
        
        if not product_id and  quantity_sold:
            return Response({'Message': 'Product ID and quantity sold are required.'})

        product = Product.objects.filter(pk=product_id).first()

        if not product:
            return Response({'Message': 'Product not found.'})
        
        total_amount = quantity_sold*product.price
        transaction = Transaction.objects.create(type='sale')

        

        sales = Sales.objects.create(
            transcation=transaction,
            product=product,
            quantity_sold=quantity_sold,
            total_amount = total_amount



        )

        inventory, created = Inventory.objects.get_or_create(product=product)
        if created:
            inventory.quantity = quantity_sold
        else:
            inventory.quantity -= quantity_sold
        inventory.save()

        serializer = Sales_serializer(sales)
        response_data = serializer.data
        response_data['total_amount'] = total_amount

        return Response(response_data)



class Getreturndetails(viewsets.ViewSet):
    def list(self,request):
        returns= Returns.objects.all()
        serialiser =Returns_serializer(returns,many=True)

        return Response(serialiser.data)
    
@extend_schema(request=Returns_serializer,responses=Returns_serializer, tags=['returns'])
class CreateReturn(viewsets.ViewSet):
    serializer_class =Returns_serializer
    def create(self,request):
        transaction = Transaction.objects.create(type='return')
        product_id = request.data.get('product')
        print(product_id,"**************************")
        quantity_return = request.data.get('quantity_returned')
        reason =request.data.get('reason')

        product =Product.objects.filter(pk=product_id).first()
        if not product:
            return Response({'Message': 'Product not found.'})
        
        returns=Returns.objects.create(

        transaction=transaction,
        product=product,
        quantity_returned=quantity_return,
        reason =reason

        )

        inventory, created = Inventory.objects.get_or_create(product=product)
        if created:
            inventory.quantity = quantity_return
        else:
            inventory.quantity += quantity_return
        inventory.save()



        serialiser = self.serializer_class(returns)
        return Response(serialiser.data)


