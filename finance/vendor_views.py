import decimal
from django.shortcuts import get_object_or_404, redirect, render
from finance.models import Item, PurchaseInvoice, PurchaseTransaction, Vendor
from django.contrib import messages

def view_vendors(request):
    vendors = Vendor.objects.all()
    return render(request,"hod/view_vendor.html",{
        "vendors":vendors
    })

def view_vendors_id(request,id):
    vendor = Vendor.objects.get(id=id)
    return  render(request,"hod/view_vendor_id.html",{
        "elem":vendor
    })

def add_vendor(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gstin = request.POST.get('gstin')
        current_balance = request.POST.get('balance')
        company = request.POST.get('company')
        website = request.POST.get('website')

        vendor = Vendor(
            name=name,
            email=email,
            phone=phone,
            address=address,
            gstin=gstin,
            current_balance = current_balance,
            company=company,
            website=website
        )
        
        vendor.save()
        messages.success(request,"Vendor Saved Successfully")
    return render(request,"hod/add_vendor.html")

def edit_vendor(request,id):
    elem = Vendor.objects.get(id=id)
    if request.method == "POST":
        elem.name = request.POST.get('name')
        elem.email = request.POST.get('email')
        elem.phone = request.POST.get('phone')
        elem.address = request.POST.get('address')
        elem.gstin = request.POST.get('gstin')
        elem.current_balance = request.POST.get('balance')
        elem.company = request.POST.get('company')
        elem.website = request.POST.get('website')

        elem.save()
        messages.success(request,"Vendor Updated Successfully")

    
    return render(request,"hod/edit_vendor.html",{
        "elem":elem
    })

def delete_vendor(request,id):
    elem = Vendor.objects.get(id=id)
    
    elem.delete()
    return redirect("view_vendors")


def view_purchase_invoices(request):
    purchase_invoices = PurchaseInvoice.objects.all()
    return render(request,"hod/view_purchase.html",{
        "purchase_invoices":purchase_invoices
    })



def add_purchase_invoice(request):
    vendors = Vendor.objects.all()
    items = Item.objects.all()
    if request.method == "POST":
        purchase_invoice_no = request.POST.get('purchase_invoice_no')
        date = request.POST.get('date')
        vendor_id = request.POST.get('vendor_id')
        vendor = Vendor.objects.get(id=vendor_id)
        
        
        return redirect("view_purchase_invoices")
    
    return render(request,"hod/add_purchase.html",{
        "vendors":vendors,
        "items":items
    })

def delete_purchase_invoice(request,id):
    purchase_invoice = PurchaseInvoice.objects.get(id=id)
    if purchase_invoice.valid:
        purchase_invoice.vendor.current_balance -= purchase_invoice.total_amount
        purchase_invoice.vendor.save()
        for tr in purchase_invoice.purchasetransaction_set.all():
            tr.item.current_stock += tr.quantity
            tr.item.save()

    purchase_invoice.delete()
    return redirect("view_purchase_invoices")

def edit_purchase_invoice(request,id):
    vendors = Vendor.objects.all()
    items = Item.objects.all()
    #get purchase_invoice
    current_purchase_invoice = PurchaseInvoice.objects.get(id=id)
    transactions = current_purchase_invoice.purchasetransaction_set.all()
    if request.method == "POST":
        current_purchase_invoice.purchase_invoice_no = request.POST.get('purchase_invoice_no')
        current_purchase_invoice.date = request.POST.get('date')
        vendor_id = request.POST.get('vendor_id')
        vendor = Vendor.objects.get(id=vendor_id)
        current_purchase_invoice.vendor = vendor
        current_purchase_invoice.valid = True
        current_purchase_invoice.save()
        return redirect("view_purchase_invoices")
    day = str(current_purchase_invoice.date.day).rjust(2,"0")
    month = str(current_purchase_invoice.date.month).rjust(2,"0")
    year = str(current_purchase_invoice.date.year).rjust(4,"0")
    return render(request,"hod/edit_purchase.html",{
        "vendors":vendors,
        "items":items,
        "purchase_invoice":current_purchase_invoice,
        "day":day,
        "month":month,
        "year":year,
        "transactions":transactions
    })


def save_transaction(request):
    if request.method == "POST":
        purchase_invoice_id = request.POST.get("purchase_invoice_id")
        purchase_invoice = PurchaseInvoice.objects.get(id=purchase_invoice_id)
        item_id = request.POST.get('item')
        item = get_object_or_404(Item,id=int(item_id))

        qnt = decimal.Decimal(request.POST.get('qnt'))
        rate = decimal.Decimal(request.POST.get('rate'))
        taxable_value = decimal.Decimal(request.POST.get('taxable_value'))
        discount_percent = decimal.Decimal(request.POST.get('discount_percent'))
        discount_amount = decimal.Decimal(request.POST.get('discount_amount'))
        state_tax = (taxable_value-discount_amount) * item.state_tax_rate/100
        central_tax = state_tax 
        total_amount = decimal.Decimal(request.POST.get('total_amount'))

        
        

        transaction = PurchaseTransaction(
            purchase_invoice = purchase_invoice,
            item = item,
            quantity = qnt,
            rate = rate,
            taxable_value = taxable_value,
            discount_percent = discount_percent,
            discount_amount = discount_amount,
            state_tax = state_tax,
            central_tax = central_tax,
            amount = total_amount
        )

        transaction.save()
        purchase_invoice.total_taxable_amount += transaction.taxable_value
        purchase_invoice.total_tax_amount += transaction.state_tax + transaction.central_tax
        purchase_invoice.total_amount += transaction.amount 
        purchase_invoice.save()

    return redirect("add_purchase_invoices")

def save_edit_transaction(request,id):
    if request.method == "POST":
        purchase_invoice_id = request.POST.get("purchase_invoice_id")
        purchase_invoice = PurchaseInvoice.objects.get(id=purchase_invoice_id)
        item_id = request.POST.get('item')
        item = get_object_or_404(Item,id=int(item_id))

        qnt = decimal.Decimal(request.POST.get('qnt'))
        amount = decimal.Decimal(request.POST.get('amount'))
        discount = request.POST.get('discount')
        rate = amount / qnt
        taxable_amount = amount / (1 + decimal.Decimal(item.state_tax_rate*2) / 100)
        tax_amount = taxable_amount * decimal.Decimal(item.state_tax_rate) / 100 * 2


        transaction = PurchaseTransaction(
            purchase_invoice = purchase_invoice,
            item = item,
            quantity = qnt,
            rate = rate,
            discount = discount,
            tax = tax_amount,
            amount = amount

        )

        transaction.save()
        purchase_invoice.total_amount += transaction.amount 
        purchase_invoice.save()

    return redirect("edit_purchase_invoice",id)

def delete_transaction(request,id):
    elem = PurchaseTransaction.objects.get(id=id)
    elem.purchase_invoice.total_amount -= elem.amount
    elem.purchase_invoice.save()
    elem.delete()

    return redirect("add_purchase_invoices")
