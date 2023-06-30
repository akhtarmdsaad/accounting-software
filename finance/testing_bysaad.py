import datetime
import random
from finance.models import *

def create_groups(n):
    names = "Shoe Veg Non-veg Glue Book Copy Pen Bag".split(" ")
    for i in range(n):
        print("     ",i,end="\r")
        ItemGroup.objects.create(
            name=random.choice(names),
            brand = str(i)
        )

def create_items(n):
    item_groups = ItemGroup.objects.all()
    names = "Model-A Model-B Model-C Model-D Model-E Model-F Model-G Model-H".split(" ")
    for i in range(n):
        print("     ",i,end="\r")
        Item.objects.create(
            name = random.choice(names),
            item_group = random.choice(item_groups),
            hsn_code = random.randint(10000,99999),
            unit = "pc",
            unit_plural = "pcs",
            state_tax_rate = "10",
            current_stock = random.randint(100,9000),
            min_stock =  0
        )
def create_customers(n):
    names = "Akhil Nikhil Sikhil Dukhil Sera Mera Tera Kora Gora Kala lal Pila Hara Jigra".split(" ")
    for i in range(n):
        name = random.choice(names)
        Customer.objects.create(
            name = name,
            email = f"{name}@gmail.com",
            phone = f"{random.randint(1000000000,9999999999)}",
            address = f"{name}Pur , Dist:{name}, pin:{random.randint(100000,999999)}",
            gstin = "",
            current_balance = random.randint(0,100000)
        )
def create_invoices(n):
    customers = Customer.objects.all()
    for i in range(n):
        print("     ",i,end="\r")
        Invoice.objects.create(
            invoice_no = str(i),
            customer = random.choice(customers),
            date = datetime.datetime.now(),
            total_taxable_amount = random.randint(0,100000),
            total_tax_amount = random.randint(0,10000),
            total_amount = random.randint(0,1000000),
            valid = True
        )

def create_transactions(n):
    invoices = Invoice.objects.all()
    items = Item.objects.all()
    for i in range(n):
        print("     ",i,end="\r")
        Transaction.objects.create(
            invoice = random.choice(invoices),
            item = random.choice(items),
            quantity = random.randint(0,50000),
            rate = random.randint(0,800),
            taxable_value = random.randint(0,8000000),
            discount_percent = 0,
            discount_amount = 0,
            state_tax =random.randint(0,80000),
            central_tax = random.randint(0,80000),
            amount = random.randint(0,8000000)
        )

def delete_items(n):
    items = Item.objects.all()
    for i in items:
        print(i,end="\r")
        if i.id > n:
            i.delete()

print("Started")
# create_invoices(2000)
print("Item Group completed")
# create_transactions(4000)
print("End")