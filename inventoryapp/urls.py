from rest_framework.routers import DefaultRouter
from inventoryapp.views import Inventory_details
router =DefaultRouter()


router.register('inventory',Inventory_details,basename="Inventory")
urlpatterns = router.urls
