from django.contrib import admin
from inventoryapp.models import Product,Inventory,Sales,Invoice,Returns,Transaction

# Register your models here.
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Sales)
admin.site.register(Invoice)
admin.site.register(Returns)
admin.site.register(Transaction)