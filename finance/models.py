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
    gstin = models.CharField(_("gstin"), max_length=15)
    current_balance = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    amount = models.IntegerField(_("amount"))
    customer = models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount}"
    

class Invoice(models.Model):
    invoice_no = models.CharField(_("invoice_no"), max_length=50)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    
class Transaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)



    