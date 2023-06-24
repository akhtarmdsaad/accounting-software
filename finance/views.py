from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from django.contrib import messages
from finance.forms import TransactionForm
from finance.models import Invoice, ItemGroup, Item,InventoryAdjustments,Customer, Transaction
import datetime,decimal
from company_settings import INVOICE_FORMAT,COMPANY_ABBR,get_invoice

# Create your views here.
def test_form(request):
    form = TransactionForm()
    return render(request,"hod/form.html",{
        "form":form
    })

def dashboard(request):
    total_item_groups = ItemGroup.objects.all().count()
    items = Item.objects.all()
    total_items = items.count()
    low_stock_items = 0
    for i in items:
        if i.current_stock <= i.min_stock:
            low_stock_items += 1

    context = {
        "total_item_groups":total_item_groups,
        "total_items":total_items,
        "low_stock_items":low_stock_items
    }
    return render(request,"hod/dashboard.html",context)

def view_item_groups(request):
    item_groups = ItemGroup.objects.all()
    context = {
        "item_groups":item_groups
    }
    return render(request,"hod/view_item_groups.html", context)

def delete_item_groups(request,id):
    item_group = ItemGroup.objects.get(id=id)
    item_group.delete()
    messages.success(request,"Item Group Deleted Successfully")
    return redirect("view_item_groups")


def add_item_groups(request):
    if request.method == "POST":
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        tax = request.POST.get('tax')
        inventory = request.POST.get('inventory')

        elem = ItemGroup(
            name=name,
            brand=brand,
            tax_preference=int(tax),
            inventory=int(inventory)
        )

        elem.save()
        messages.success(request,"Item Group Added Successfully")

    return render(request,"hod/add_item_groups.html")

def edit_item_groups(request,id):
    if request.method == "POST":
        id = request.POST.get('id')
        elem = ItemGroup.objects.get(id=int(id))
        elem.name = request.POST.get('name')
        elem.brand = request.POST.get('brand')
        elem.tax = request.POST.get('tax')
        elem.inventory = request.POST.get('inventory')
        elem.updated_at = datetime.datetime.now()

        elem.save()
        messages.success(request,"Item Group Updated Successfully")
    item_group = ItemGroup.objects.get(id=id)
    context = {
        "elem":item_group
    }
    return render(request,"hod/edit_item_groups.html",context)



def view_items(request):
    items = Item.objects.all()
    context = {
        "items":items
    }
    return render(request,"hod/view_items.html", context)

def view_items_id(request,id):
    item = Item.objects.get(id=id)
    context = {
        "item":item
    }
    return render(request,"hod/view_item_id.html",context)

def add_item(request):
    item_groups = ItemGroup.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        image = request.FILES.get('image')
        item_group_id = request.POST.get('item_group')
        item_group = ItemGroup.objects.get(pk=item_group_id)
        hsn = request.POST.get('hsn')
        unit = request.POST.get('unit')
        tax = request.POST.get('tax')
        cur_stock = request.POST.get('cur_stock')
        min_stock = request.POST.get('min_stock')
        unit_plural = unit+"s"
        elem = Item(
            name=name,
            image=image,
            item_group=item_group,
            hsn_code=hsn,
            unit=unit,
            unit_plural=unit_plural,
            state_tax_rate=tax,
            current_stock=cur_stock,
            min_stock=min_stock
        )

        elem.save()
        messages.success(request,"Item Added Successfully")
    context = {
        "item_groups":item_groups
    }
    return render(request,"hod/add_item.html",context)

def edit_item(request,id):
    item_groups = ItemGroup.objects.all()
    if request.method == "POST":
        id = request.POST.get('id')
        elem = Item.objects.get(id=int(id))
        elem.name = request.POST.get('name')
        image = request.FILES.get('image')
        if image:
            elem.image = image
        item_group_id = request.POST.get('item_group')
        elem.item_group = ItemGroup.objects.get(pk=item_group_id)
        elem.hsn = request.POST.get('hsn')
        elem.unit = request.POST.get('unit')
        elem.tax = request.POST.get('tax')
        elem.cur_stock = request.POST.get('cur_stock')
        elem.min_stock = request.POST.get('min_stock')
        elem.unit_plural = elem.unit+"s"
        elem.updated_at = datetime.datetime.now()
        elem.save()
        messages.success(request,"Item Updated Successfully")
    item = Item.objects.get(id=id)
    context = {
        "item_groups":item_groups,
        "elem":item
    }
    return render(request,"hod/edit_item.html",context)

def delete_item(request,id):
    item = Item.objects.get(id=id)
    item.delete()
    messages.success(request,"Item Deleted Successfully")
    return redirect("view_items")


def view_item_adjustment(request):
    inventory_adjustments = InventoryAdjustments.objects.all()


    context = {
        "inventory_adjustments":inventory_adjustments
    }
    return render(request,"hod/view_item_adjustment.html",context)

def add_item_adjustment(request):
    items = Item.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        qnt = request.POST.get('qnt')
        item_id = request.POST.get('item')
        item = Item.objects.get(id=item_id)
        type = request.POST.get('type')
        reason_title = request.POST.get('reason_title')
        reason_desc = request.POST.get('reason_desc')

        elem = InventoryAdjustments(
            date=date,
            item=item,
            quantity=qnt,
            ADJUSTMENT_TYPE = int(type),
            reason_title=reason_title,
            reason_desc=reason_desc
        )
        # Do The Changes to other models Here
        if int(type) == 1:
            item.current_stock += int(qnt)
        else:
            item.current_stock -= int(qnt)
            
        item.save()
        elem.save()
        messages.success(request,"Adjustment Added Successfully")

    return render(request,"hod/add_item_adjustment.html",{
        "items":items
    })


def edit_item_adjustment(request,id):
    items = Item.objects.all()
    if request.method == "POST":
        id = request.POST.get('id')
        elem = InventoryAdjustments.objects.get(id=int(id))
        elem.date = request.POST.get('date')
        elem.quantity = request.POST.get('qnt')
        item_id = request.POST.get('item')
        elem.item = Item.objects.get(id=item_id)
        elem.ADJUSTMENT_TYPE = request.POST.get('type')
        elem.reason_title = request.POST.get('reason_title')
        elem.reason_desc = request.POST.get('reason_desc')
        elem.updated_at = datetime.datetime.now()
        
        elem.save()
        messages.success(request,"Adjustment Updated Successfully")

    elem = InventoryAdjustments.objects.get(id=int(id))
    day = str(elem.date.day).rjust(2,"0")
    month = str(elem.date.month).rjust(2,"0")
    year = str(elem.date.year).rjust(4,"0")

    return render(request,"hod/edit_item_adjustment.html",{
        "items":items,
        "elem":elem,
        "day":day,
        "month":month,
        "year":year
    })

def delete_item_adjustment(request,id):
    adjustment = InventoryAdjustments.objects.get(id=id)
    if adjustment.ADJUSTMENT_TYPE == 1:
        adjustment.item.current_stock -= adjustment.quantity
    else:
        adjustment.item.current_stock += adjustment.quantity
    adjustment.item.save()
    adjustment.delete()
    messages.success(request,"Item Adjustment Deleted Successfully")
    return redirect("view_item_adjustment")

def view_customers(request):
    customers = Customer.objects.all()
    return render(request,"hod/view_customer.html",{
        "customers":customers
    })

def view_customers_id(request,id):
    customer = Customer.objects.get(id=id)
    return  render(request,"hod/view_customer_id.html",{
        "elem":customer
    })

def add_customer(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gstin = request.POST.get('gstin')
        current_balance = request.POST.get('balance')

        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
            gstin=gstin,
            current_balance = current_balance
        )
        
        customer.save()
        messages.success(request,"Customer Saved Successfully")
    return render(request,"hod/add_customer.html")

def edit_customer(request,id):
    elem = Customer.objects.get(id=id)
    return render(request,"hod/edit_customer.html",{
        "elem":elem
    })

def delete_customer(request,id):
    if request.method == "POST":
        elem.name = request.POST.get('name')
        elem.email = request.POST.get('email')
        elem.phone = request.POST.get('phone')
        elem.address = request.POST.get('address')
        elem.gstin = request.POST.get('gstin')
        elem.current_balance = request.POST.get('balance')

        elem.save()
        messages.success(request,"Customer Updated Successfully")

    elem = Customer.objects.get(id=id)
    elem.delete()
    return redirect("view_customers")

def view_invoices(request):
    invoices = Invoice.objects.filter(valid=True)
    return render(request,"hod/view_invoice.html",{
        "invoices":invoices
    })



def add_invoice(request):
    customers = Customer.objects.all()
    items = Item.objects.all()
    #get invoice
    invoices = Invoice.objects.filter(valid=False)
    if not invoices:
        last_invoice = Invoice.objects.all().order_by('-id')
        if last_invoice:
            last_invoice = last_invoice[0]
            new_inv_no = get_invoice(last_invoice.invoice_no)
        else:
            new_inv_no = get_invoice("0")
        current_invoice = Invoice.objects.create(
            invoice_no=new_inv_no,
            customer = Customer.objects.all()[0],
            date = datetime.date.today(),
            total_taxable_amount=0,
            total_tax_amount=0,
            total_amount = 0
        )
    else:
        current_invoice = invoices[0]
    
    transactions = current_invoice.transaction_set.all()
    if request.method == "POST":
        current_invoice.invoice_no = request.POST.get('invoice_no')
        current_invoice.date = request.POST.get('date')
        customer_id = request.POST.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        current_invoice.customer = customer
        customer.current_balance += current_invoice.total_amount
        customer.save()
        for tr in current_invoice.transaction_set.all():
            tr.item.current_stock -= tr.quantity
            tr.item.save()
        current_invoice.valid = True
        current_invoice.save()
        return redirect("view_invoices")
    day = str(current_invoice.date.day).rjust(2,"0")
    month = str(current_invoice.date.month).rjust(2,"0")
    year = str(current_invoice.date.year).rjust(4,"0")
    return render(request,"hod/add_invoice.html",{
        "customers":customers,
        "items":items,
        "invoice":current_invoice,
        "day":day,
        "month":month,
        "year":year,
        "transactions":transactions
    })

def delete_invoice(request,id):
    invoice = Invoice.objects.get(id=id)
    if invoice.valid:
        invoice.customer.current_balance -= invoice.total_amount
        invoice.customer.save()
        for tr in invoice.transaction_set.all():
            tr.item.current_stock += tr.quantity
            tr.item.save()

    invoice.delete()
    return redirect("view_invoices")

def edit_invoice(request,id):
    customers = Customer.objects.all()
    items = Item.objects.all()
    #get invoice
    current_invoice = Invoice.objects.get(id=id)
    transactions = current_invoice.transaction_set.all()
    if request.method == "POST":
        current_invoice.invoice_no = request.POST.get('invoice_no')
        current_invoice.date = request.POST.get('date')
        customer_id = request.POST.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        current_invoice.customer = customer
        current_invoice.valid = True
        current_invoice.save()
        return redirect("view_invoices")
    day = str(current_invoice.date.day).rjust(2,"0")
    month = str(current_invoice.date.month).rjust(2,"0")
    year = str(current_invoice.date.year).rjust(4,"0")
    return render(request,"hod/edit_invoice.html",{
        "customers":customers,
        "items":items,
        "invoice":current_invoice,
        "day":day,
        "month":month,
        "year":year,
        "transactions":transactions
    })


def save_transaction(request):
    if request.method == "POST":
        invoice_id = request.POST.get("invoice_id")
        invoice = Invoice.objects.get(id=invoice_id)
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

        
        

        transaction = Transaction(
            invoice = invoice,
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
        invoice.total_taxable_amount += transaction.taxable_value
        invoice.total_tax_amount += transaction.state_tax + transaction.central_tax
        invoice.total_amount += transaction.amount 
        invoice.save()

    return redirect("add_invoices")

def save_edit_transaction(request,id):
    if request.method == "POST":
        invoice_id = request.POST.get("invoice_id")
        invoice = Invoice.objects.get(id=invoice_id)
        item_id = request.POST.get('item')
        item = get_object_or_404(Item,id=int(item_id))

        qnt = decimal.Decimal(request.POST.get('qnt'))
        amount = decimal.Decimal(request.POST.get('amount'))
        discount = request.POST.get('discount')
        rate = amount / qnt
        taxable_amount = amount / (1 + decimal.Decimal(item.state_tax_rate*2) / 100)
        tax_amount = taxable_amount * decimal.Decimal(item.state_tax_rate) / 100 * 2


        transaction = Transaction(
            invoice = invoice,
            item = item,
            quantity = qnt,
            rate = rate,
            discount = discount,
            tax = tax_amount,
            amount = amount

        )

        transaction.save()
        invoice.total_amount += transaction.amount 
        invoice.save()

    return redirect("edit_invoice",id)

def delete_transaction(request,id):
    elem = Transaction.objects.get(id=id)
    elem.invoice.total_amount -= elem.amount
    elem.invoice.save()
    elem.delete()

    return redirect("add_invoices")