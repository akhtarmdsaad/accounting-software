from django.db.models.signals import post_save, post_delete
from finance.models import Invoice, Transaction, SaleReturn
from django.dispatch import receiver
import json,decimal

@receiver(post_save, sender=Invoice) 
def update_invoice(sender, instance, created, **kwargs):
    if created:
        pass
    
    # calculation
    total_taxable_amount = 0
    total_state_tax_amount = 0
    total_central_tax_amount = 0
    total_integrated_tax_amount = 0
    total_invoice_amount = 0

    for t in instance.transaction_set.all():
        total_taxable_amount += decimal.Decimal(t.taxable_value - t.discount_amount) 
        if instance.tax_type == 1:
            total_state_tax_amount += decimal.Decimal((t.item.state_tax_rate / 100) * float(t.taxable_value))
            total_central_tax_amount += decimal.Decimal((t.item.central_tax_rate / 100) * float(t.taxable_value))
        else:
            total_integrated_tax_amount += decimal.Decimal((t.item.integrated_tax_rate / 100) * float(t.taxable_value))
    
    total_invoice_amount = total_taxable_amount + total_state_tax_amount + total_central_tax_amount + total_integrated_tax_amount

    if instance.extra_details:
        # calculating extra details
        for val in json.loads(instance.extra_details).values():
            total_invoice_amount += int(val)
        
    instance.total_taxable_amount = total_taxable_amount
    instance.total_state_tax_amount = total_state_tax_amount
    instance.total_central_tax_amount = total_central_tax_amount
    instance.total_integrated_tax_amount = total_integrated_tax_amount
    instance.total_amount = total_invoice_amount
    instance.valid = True
    print("From signal:",instance, instance.total_amount)
    # instance.save()


# @receiver(post_delete, sender=Transaction)
# def add_to_inventory(sender, instance, **kwargs):
#     inventory_item = Inventory.objects.get(id=instance.inventory_item.id)
#     inventory_item.quantity = inventory_item.quantity + instance.quantity

#     inventory_item.save()

# @receiver(post_save, sender=SaleReturn)
# def add_sale_return(sender,instance, created,**kwargs):
#     if created:
#         pass 
    
#     # add amount to customer
#     customer = instance.customer
#     customer.current_balance += instance.amount

#     # add quantity to item
#     item = instance.item
#     item.current_stock += instance.quantity
#     item.save()
