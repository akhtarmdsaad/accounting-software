from django.core.validators import MaxValueValidator
import decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser

#state name entry
from finance.common import state_names

# Create your models here.
TAX_TYPE = (
    (1,'CGST/SGST'),
    (2,'IGST')
)

TAX_PREFERENCE = (
    (1,'Taxable'),
    (2,'Non Taxable')
)

INVENTORY_TYPE = (
    (1,'Yes'),
    (2,'No')
)


class ItemGroup(models.Model):
    name = models.CharField(_("name"), max_length=50)
    brand = models.CharField(_("brand"), max_length=50)
    tax_preference = models.IntegerField(choices=TAX_PREFERENCE,default=1)
    inventory = models.IntegerField(choices=INVENTORY_TYPE,default=1)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self) -> str:
        return self.name + " - " + self.brand

RATE_CHANGE_CHOICES = (
    (1,"Fixed"),
    (2,"Last Rate"),
)

class Item(models.Model):
    name = models.CharField(_("name"), max_length=50)
    image = models.ImageField(upload_to="media/item_images",null=True)
    item_group = models.ForeignKey(ItemGroup,on_delete=models.CASCADE)
    hsn_code = models.IntegerField()
    unit = models.CharField(max_length=10)
    unit_plural = models.CharField(max_length=10)
    state_tax_rate = models.IntegerField()
    central_tax_rate = models.IntegerField(default=0)
    integrated_tax_rate = models.IntegerField(default=0)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2)
    rate_change_system = models.IntegerField(choices=RATE_CHANGE_CHOICES,default=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    min_stock = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self) -> str:
        return self.name + " - " + str(self.item_group)

ADJUSTMENT_TYPE = (
    (1,"Increase"),
    (2,"Decrease")
)
class InventoryAdjustments(models.Model):
    date = models.DateField()
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reason_title = models.CharField(max_length=100)
    reason_desc = models.TextField() 
    ADJUSTMENT_TYPE = models.IntegerField(choices=ADJUSTMENT_TYPE,default=2)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return str(self.item.name) + " - " + str(self.reason_title)

YES_NO = (
    (1,"Yes"),
    (2, "No")
)
STATES = []
for i,j in enumerate(state_names,start=1):
    STATES.append((i,j))
STATES = tuple(STATES)

class Customer(models.Model):
    name = models.CharField(_("name"), max_length=50)
    email = models.EmailField(_("email"), max_length=254,null=True)
    phone = models.CharField(_("phone"), max_length=50, null=True)
    address = models.TextField()
    state = models.IntegerField(choices=STATES,default=1)
    gstin = models.CharField(_("gstin"), max_length=15,null=True)
    pancard = models.CharField(_("pancard"), max_length=15,null=True)
    save_last_rate = models.IntegerField(choices=YES_NO,default=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,on_delete=models.PROTECT,null=True)
    

    def __str__(self):
        return self.name
    
MODE = (
    (1,'CASH'),
    (2,'BANK')
)
class Payment(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    description = models.TextField(default="")
    customer = models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    mode = models.IntegerField(choices=MODE,default=1)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return f"{self.customer.name}-{self.amount}"
    

class ShippingDetail(models.Model):
    name = models.CharField(_("name"),max_length=70)
    address = models.CharField(_("address"), max_length=50)
    state = models.IntegerField(choices=STATES,default=1)

    class Meta:
        verbose_name = _("ShippingDetail")
        verbose_name_plural = _("ShippingDetails")

    def __str__(self):
        return self.name



class Invoice(models.Model):
    invoice_no = models.CharField(_("invoice_no"), max_length=50)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True)
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    total_taxable_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_state_tax_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_central_tax_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_integrated_tax_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    extra_details = models.JSONField(null=True)
    shipping_details = models.ForeignKey(ShippingDetail,on_delete=models.CASCADE,null=True)
    valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return self.invoice_no
    

    
class Transaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_value = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return self.invoice.invoice_no

STATUS = (
    (1,"Available"),
    (2,"Redeemed")
)

class SaleReturn(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS,default = 1)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    
    
    def __str__(self):
        return str(self.customer.name) + " - " + str(self.amount)

class Vendor(models.Model):
    name = models.CharField(_("name"), max_length=50)
    company = models.CharField(_("company"), max_length=50)
    email = models.EmailField(_("email"), max_length=254,null=True)
    phone = models.CharField(_("phone"), max_length=50)
    address = models.TextField()
    website = models.CharField(_("website"), max_length=50,null=True)
    gstin = models.CharField(_("gstin"), max_length=15,null=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return self.company

class PurchaseInvoice(models.Model):
    invoice_no = models.CharField(_("invoice_no"), max_length=50)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    file_invoice = models.FileField(_("invoice_file"), upload_to="media/invoice_files")
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    total_taxable_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_tax_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid = models.BooleanField(_("valid"),default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return self.invoice_no
    

    
class PurchaseTransaction(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_value = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    state_tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    central_tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return self.invoice.invoice_no

class Reciept(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    description = models.TextField(default="")
    vendor = models.ForeignKey(Vendor,null=True,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    mode = models.IntegerField(choices=MODE,default=1)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return f"{self.vendor.company}-{self.amount}"

class PurchaseReturn(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS,default = 1)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    
    
    def __str__(self):
        return str(self.vendor.name) + " - " + str(self.amount)


class VendorCreditNote(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    description = models.TextField(default="")
    status = models.IntegerField(choices=STATUS,default = 1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)
    

    def __str__(self):
        return str(self.vendor.company) + " - " + str(self.amount)
    
class LastItemRate(models.Model):
    party = models.ForeignKey(Customer,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)
    changed_by_user = models.ForeignKey(CustomUser,null=True,on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.party.name} for {self.item.name} - {self.rate}"