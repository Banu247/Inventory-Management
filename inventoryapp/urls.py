from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from inventoryapp.views import Inventory_details,Sales_info,SalesInventory,Getreturndetails,CreateReturn,Invoice_details,ListInvoices,GetProduct,Createproduct,FetchTranscationId

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register('inventory', Inventory_details, basename='Inventory')
router.register('Get-Sales-Details',Sales_info,basename='sales')
router.register('Sale-product',SalesInventory,basename='sales')
router.register('Get-return-details',Getreturndetails,basename='returns')
router.register('Return-product',CreateReturn,basename='returns')
# router.register('All-products',GetProduct,basename='Products')
# router.register(r'invoicelist',ListInvoices,basename='Invoice')

# Define the schema view for DRF-Spectacular
schema_view = get_schema_view(
    openapi.Info(
        title="CRUD OPERATIONS",
        default_version="v1",
        description="Sample app",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

# Define the urlpatterns
urlpatterns = [
    path('', include(router.urls)),  
    path('Generate-Invoice/<int:transaction_id>/',Invoice_details.as_view(),name='Invoice'),
    path('invoicelist/<int:product_id>/',ListInvoices.as_view(),name='Invoice'),
    path('Get-Transaction-id',FetchTranscationId.as_view(),name='Invoice'),
    # Endpoint for Swagger UI using DRF-Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('GetProduct/', GetProduct.as_view(), name='Products'),
    path('Create-Product/', Createproduct.as_view(), name='Products'),
   path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
