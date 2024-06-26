from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from finance.models import *
import datetime


class Transaction:
    def __init__(self,no,date,customer="",voucher="",amount=""):
        pass
def home(request):
    table_list = []
    invoices = Invoice.objects.filter(date = datetime.date.today())
    payments = Payment.objects.filter(date = datetime.date.today())
    reciepts = Reciept.objects.filter(date = datetime.date.today())
    purchases = PurchaseInvoice.objects.filter(date = datetime.date.today())
    sale_returns = SaleReturn.objects.filter(date = datetime.date.today())
    purchase_returns = PurchaseReturn.objects.filter(date = datetime.date.today())
    context = {
        "invoices":invoices,
        "payments":payments,
        "reciepts":reciepts,
        "purchases":purchases,
        "salereturns":sale_returns,
        "purchasereturns":purchase_returns
    }
    return render(request,"reports/daybook.html")

def sales_by_customer(request):
    table_list = []
    id = request.GET.get('select_id')

    customers = Customer.objects.all()
    if id:
        customer = Customer.objects.get(id = id)
        invoices = customer.invoice_set.all()
        print(customer)
    else:
        customer = None
        invoices = []
    
    for i,j in enumerate(invoices):
        data = [i+1, j.invoice_no, j.date, j.total_amount]
        table = Table(data)
        table.prepare_td()
        table_list.append(table)



    context = {
        "label":"Customer",
        "models":customers,
        "row_headings":["Sl no", "Invoice no", "Date", "Total Amount"],
        "items":table_list
    }
    return render(request,"hod/reports.html",context)

def sales_by_item(request):
    table_list = []
    id = request.GET.get('select_id')

    items = Item.objects.all()
    if id:
        item = Item.objects.get(id = id)
        invoices = item.transaction_set.all()
        print(item)
    else:
        item = None
        invoices = []
    
    for i,j in enumerate(invoices):
        data = [i+1, j.invoice.invoice_no, j.invoice.date,j.quantity, j.amount]
        table = Table(data)
        table.prepare_td()
        table_list.append(table)



    context = {
        "label":"Item",
        "models":items,
        "row_headings":["Sl no", "Invoice no", "Date", "Quantity" , "Amount"],
        "items":table_list
    }
    return render(request,"hod/reports.html",context)

def sales_by_dates(request):
    return None 

def sales_by_invoice(request):
    return None

def payments_by_customers(request):
    table_list = []
    id = request.GET.get('select_id')

    customers = Customer.objects.all()
    if id:
        customer = Customer.objects.get(id = id)
        payemnts = customer.payment_set.all()
        print(customer)
    else:
        customer = None
        payemnts = []
    
    for i,j in enumerate(payemnts):
        data = [i+1, j.id, j.date, j.mode, j.amount]
        table = Table(data)
        table.prepare_td()
        table_list.append(table)



    context = {
        "label":"Customer",
        "models":customers,
        "row_headings":["Sl no", "Payment id", "Date", "Mode", "Total Amount"],
        "items":table_list
    }
    return render(request,"hod/reports.html",context)

def payments_by_date(request):
    return None

def payments_by_invoices(request):
    return None

def inventory_by_item_group(request):
    return None

def inventory_by_items(request):
    table_list = []
    id = request.GET.get('select_id')

    items = Item.objects.all()
    if id:
        item = Item.objects.get(id = id)
        invoices = item.inventoryadjustments_set.all()
    else:
        item = None
        invoices = []
    
    for i,j in enumerate(invoices):
        data = [i+1, j.id, j.date,j.quantity, "Increase" if j.ADJUSTMENT_TYPE == 1 else "Decrease"]
        table = Table(data)
        table.prepare_td()
        table_list.append(table)



    context = {
        "label":"Item",
        "models":items,
        "row_headings":["Sl no", "Id", "Date", "Quantity" , "Inc/Dec"],
        "items":table_list
    }
    return render(request,"hod/reports.html",context)

def inventory_by_date(request):
    return None

def inventory_by_invoice(request):
    return None

def payables_to_vendor(request):
    return None

def payments_already_made_to_vendor(request):
    return None


