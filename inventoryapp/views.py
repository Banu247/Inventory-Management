from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets
from inventoryapp.models import Inventory,Sales,Product,Transaction,Returns,Invoice
from inventoryapp.serializers import Inventory_serializer,Sales_serializer,Returns_serializer,Invoice_serializer,Product_serializer
from drf_spectacular.views import extend_schema
from rest_framework.response import Response
from io import BytesIO
from rest_framework import status
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.views import APIView
import os


@extend_schema(request=Inventory_serializer,responses=Inventory_serializer, tags=['inventory'])
class Inventory_details(viewsets.ModelViewSet):
    '''API to Get,Retrive,Update,Delete,Patch,Create Inventory'''
    serializer_class = Inventory_serializer
    queryset = Inventory.objects.all()

class Sales_info(viewsets.ViewSet):
    '''API to fetch sales details'''
    serializer_class = Sales_serializer
    @extend_schema( tags=['sales'])

    def list(self,request):
        all_data =Sales.objects.all()
        serialiser= Sales_serializer(all_data,many=True)

        return Response(serialiser.data)

@extend_schema(request=Sales_serializer,responses=Sales_serializer, tags=['sales'])

class SalesInventory(viewsets.ViewSet):
    '''API to create sales'''
    def create(self,request):
        product_id = request.data.get('product_id') 
        quantity_sold= request.data.get('quantity_sold')
        if not product_id or not quantity_sold:
            return Response({'Message': 'Fields Required.'})

        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return Response({'Message': 'Product not found.'})
        
        total_amount = quantity_sold*product.price
        transaction = Transaction.objects.create(type='sale')

    
        sales = Sales.objects.create(
            transcation=transaction,
            product_id=product,
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
        response_data['date'] = datetime.now()


        return Response(response_data)



class Getreturndetails(viewsets.ViewSet):
    '''API to fetch Return details'''
    serializer_class = Returns_serializer
    @extend_schema( tags=['Return'])

    def list(self,request):
        returns= Returns.objects.all()
        serialiser =Returns_serializer(returns,many=True)

        return Response(serialiser.data)
    
@extend_schema(request=Returns_serializer,responses=Returns_serializer, tags=['returns'])
class CreateReturn(viewsets.ViewSet):
    '''API for initiating returns'''
    serializer_class =Returns_serializer
    @extend_schema( tags=['Return'])


    def create(self,request):
        transaction = Transaction.objects.create(type='return')
        product_id = request.data.get('product_id')
        quantity_return = request.data.get('quantity_returned')
        reason =request.data.get('reason')

        if product_id<=0 or  quantity_return<=0 or reason=="string":
            return Response({"Message":"Fields Required!!!"})
        
        product =Product.objects.filter(pk=product_id).first()

        if not product:
            return Response({'Message': 'Product not found.'})
        
        returns=Returns.objects.create(

        transaction=transaction,
        product_id=product,
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
        field=serialiser.data
        data={
            "product_name": product.product_name,
            "Product_id":field['product_id'],
            "quantity_returned":field['quantity_returned'],
            "reason":field["reason"],
            "transaction_id":transaction.id,
            "return_date":datetime.now()
        }
            
        return Response(data)


class Invoice_details(APIView):
    '''API to generate Invoice based on transaction_id'''
    serializer_class = Sales_serializer  
    @extend_schema(
        tags=['Invoices']  
    )

    def get(self, request, transaction_id=None):
        transaction = Transaction.objects.filter(pk=transaction_id).first()
        if not transaction:
            return Response({"Message": "Details not found"})

    
        sales = Sales.objects.filter(transcation=transaction)
        if not sales.exists():
            return Response({"Message": "No sales found for this transaction"})
        
        product_name =None
        total_amount=None
        for i in sales:

            product_name = i.product_id.product_name
            total_amount= i.total_amount
        serializer = self.serializer_class(sales, many=True)

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 750, "Invoice Details")
        pdf.drawString(100, 730, f"Transaction ID: {transaction_id}")
        pdf.drawString(100, 710, "Sales Details:")

        # pdf.setFont("Helvetica-Bold", 12)
        y_position = 690
        line_height = 20

        for sale in serializer.data:
            pdf.drawString(120, y_position, f"Product_Name:{product_name} ")
            pdf.drawString(320, y_position, f"Quantity Sold: {sale['quantity_sold']}")
            pdf.drawString(450, y_position, f"Total Amount: {total_amount}")
            y_position -= line_height 
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 100, f"Total Amount: {total_amount}")

        pdf.showPage()
        pdf.save()

        file_name = f"invoice_{transaction_id}.pdf"
        file_directory = 'invoices'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_directory):
            os.makedirs(file_directory)

        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        invoice, created = Invoice.objects.get_or_create(
            transaction=transaction,
            amount=total_amount,
            pdf_file=file_path
        )

        # Serve the PDF as a response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response


class ListInvoices(APIView):
    '''API to fetch  list all the invoices made for a specific product'''
    serializer_class = Invoice_serializer
    @extend_schema(
        tags=['Invoices']
    )

    def get(self,request,product_id=None):
        try:
             data = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'Message': 'Product not found.'})

        query_set = data.sales_set.all()



        transaction_id=None
        for i in query_set:
            transaction_id =i.transcation

        try:
            realated_id = Invoice.objects.get(transaction=transaction_id)
        except Invoice.DoesNotExist:
            return Response({'Message':"No Invoice generated f0r the above product"})
        serialiser =Invoice_serializer(realated_id,many =False)

        return Response(serialiser.data)


class GetProduct(APIView):
    '''API to fetch the details of product'''
    serializer_class =Product_serializer
    @extend_schema(tags=['Products'])
    def get(self,request):
        query_set =Product.objects.all()
        serialiser=Product_serializer(query_set,many=True)

        return Response(serialiser.data)

class Createproduct(APIView):
    '''API to create product'''
    serializer_class =Product_serializer
    @extend_schema(request=Product_serializer,tags=['Products'])

    def post(self,request):
        pro_name =request.data.get('product_name')
        descrip =request.data.get('description')
        price =request.data.get('price')
        if pro_name == 'string'  or  descrip == 'string' or int(price)<=0:
            return Response({'Message':'Required fields are not provided'})
        
        serializer = Product_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Product created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FetchTranscationId(APIView):
    '''API to fetch all the transaction_id related to sales'''
    @extend_schema(request=Product_serializer,tags=['Invoices'])

    def get(self,request):
        transcation =Transaction.objects.filter(type='sale').all()
        data=[]

        for i in transcation:
            data.append({
                "transcation_id":i.id
            })
        return Response({"info":data})
    


