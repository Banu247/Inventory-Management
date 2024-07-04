from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from inventoryapp.views import Inventory_details,Sales_info,SalesInventory,Getreturndetails,CreateReturn

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register('inventory', Inventory_details, basename='Inventory')
router.register('sales',Sales_info,basename='sales')
router.register('salesinfo',SalesInventory,basename='sales')
router.register('getreturn',Getreturndetails,basename='returns')
router.register('postreturn',CreateReturn,basename='returns')

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
    path('', include(router.urls)),  # Include DRF router URLs

    # Endpoint for Swagger UI using DRF-Spectacular
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
   path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
