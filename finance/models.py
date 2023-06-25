import decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

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

    def __str__(self) -> str:
        return self.name + " - " + self.brand

class Item(models.Model):
    name = models.CharField(_("name"), max_length=50)
    image = models.ImageField(upload_to="media/item_images",null=True)
    item_group = models.ForeignKey(ItemGroup,on_delete=models.CASCADE)
    hsn_code = models.IntegerField()
    unit = models.CharField(max_length=10)
    unit_plural = models.CharField(max_length=10)
    state_tax_rate = models.IntegerField()
    current_stock = models.IntegerField()
    min_stock = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self) -> str:
        return self.name + " - " + str(self.item_group)

ADJUSTMENT_TYPE = (
    (1,"Increase"),
    (2,"Decrease")
)
class InventoryAdjustments(models.Model):
    date = models.DateField()
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reason_title = models.CharField(max_length=100)
    reason_desc = models.TextField() 
    ADJUSTMENT_TYPE = models.IntegerField(choices=ADJUSTMENT_TYPE,default=2)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self):
        return str(self.item.name) + " - " + str(self.reason_title)

class Customer(models.Model):
    name = models.CharField(_("name"), max_length=50)
    email = models.EmailField(_("email"), max_length=254,null=True)
    phone = models.CharField(_("phone"), max_length=50)
    address = models.TextField()
    gstin = models.CharField(_("gstin"), max_length=15,null=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2,default=decimal.Decimal(0))
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

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
    amount = models.IntegerField(_("amount"))
    mode = models.IntegerField(choices=MODE,default=1)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self):
        return f"{self.customer.name}-{self.amount}"
    

class Invoice(models.Model):
    invoice_no = models.CharField(_("invoice_no"), max_length=50)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    total_taxable_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_tax_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self):
        return self.invoice_no
    

    
class Transaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_value = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    state_tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    central_tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

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
    quantity = models.IntegerField()
    description = models.TextField(default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS,default = 1)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

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
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self):
        return self.invoice_no
    

    
class PurchaseTransaction(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_value = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    state_tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    central_tax = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self):
        return self.invoice.invoice_no
