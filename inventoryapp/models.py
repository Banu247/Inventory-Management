from django.db import models
from django.conf import settings
import io
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=60)
    description =models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
class Inventory(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,primary_key=True)
    quantity=models.IntegerField(default=0)



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('sale', 'Sale'),
        ('return', 'Return'),
    )
    type = models.CharField(max_length=10,choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)


class Sales(models.Model):
    transcation=models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold =models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Returns(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_returned = models.IntegerField()
    reason= models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)

