from django.contrib import admin
from finance.models import *
# Register your models here.

admin.site.register(ItemGroup)
admin.site.register(Item)
admin.site.register(InventoryAdjustments)
admin.site.register(Customer)
admin.site.register(Payment)
admin.site.register(Invoice)
admin.site.register(Transaction)
admin.site.register(SaleReturn)
admin.site.register(Vendor)
admin.site.register(PurchaseInvoice)
admin.site.register(PurchaseTransaction)