from django.db import models

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=60)
    description =models.TextField(blank=True)
    price =models.IntegerField(default=0)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold =models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class Returns(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_returned = models.IntegerField()


class Invoice(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
