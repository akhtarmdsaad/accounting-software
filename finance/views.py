from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from finance.forms import TransactionForm
from finance.models import Invoice, ItemGroup, Item,InventoryAdjustments,Customer, LastItemRate, Payment, SaleReturn, Transaction, Vendor, ShippingDetail
import datetime,decimal
from company_settings import get_invoice
from finance.common import state_names
from django.db.models import Sum, F
import json



# Create your views here.
def test_form(request):
    form = TransactionForm()
    return render(request,"hod/form.html",{
        "form":form
    })

def invoice(request,id=None):
    if not id:
        return HttpResponse(request,"Nothing to show ...")
    from company_settings import COMPANY_NAME,COMPANY_EMAIL,COMPANY_ADDR
    from company_settings import COMPANY_GSTIN
    # from finance.models import Invoice
    # print(len(Invoice.objects.all()))
    inv = Invoice.objects.get(id=id)
    context = {
        "inv":inv,
        "NAME":COMPANY_NAME,
        "EMAIL":COMPANY_EMAIL,
        "ADDR":COMPANY_ADDR,
        "GST":COMPANY_GSTIN,
        "transactions":inv.transaction_set.all(),
    }
    return render(request,'hod/invoice.html',context=context)

@login_required(login_url="account_login")
def dashboard(request):
    total_item_groups = ItemGroup.objects.all().count()
    items = Item.objects.all()
    total_items = items.count()
    low_stock_items = 0
    no_of_customers = Customer.objects.count()
    total_recievables = Customer.objects.aggregate(Sum('current_balance'))['current_balance__sum']
    total_payables = Vendor.objects.aggregate(Sum('current_balance'))['current_balance__sum']
    no_of_invoices = Invoice.objects.count()
    for i in items:
        if i.current_stock <= i.min_stock:
            low_stock_items += 1

    context = {
        "total_item_groups":total_item_groups,
        "total_items":total_items,
        "low_stock_items":low_stock_items,
        "no_of_customers":no_of_customers,
        "total_recievables":total_recievables,
        "total_payables":total_payables,
        "no_of_invoices":no_of_invoices,
    }
    return render(request,"hod/dashboard.html",context)

@login_required(login_url="account_login")
def view_item_groups(request):
    if not request.user.has_perm('finance.view_itemgroup'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    item_groups = ItemGroup.objects.all()
    context = {
        "item_groups":item_groups
    }
    return render(request,"hod/view_item_groups.html", context)

@login_required(login_url="account_login")
def delete_item_groups(request,id):
    if not request.user.has_perm('finance.delete_itemgroup'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    item_group = get_object_or_404(ItemGroup,id=id)
    item_group.delete()
    
    messages.success(request,"Item Group Deleted Successfully")
    return redirect("view_item_groups")


@login_required(login_url="account_login")
def add_item_groups(request):
    if not request.user.has_perm('finance.add_itemgroup'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
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

@login_required(login_url="account_login")
def edit_item_groups(request,id):
    if not request.user.has_perm('finance.change_itemgroup'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    if request.method == "POST":
        id = request.POST.get('id')
        elem = ItemGroup.objects.get(id=int(id))
        elem.name = request.POST.get('name')
        elem.brand = request.POST.get('brand')
        elem.tax_preference = request.POST.get('tax')
        elem.inventory = request.POST.get('inventory')
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user

        elem.save()
        messages.success(request,"Item Group Updated Successfully")
    item_group = get_object_or_404(ItemGroup,id=id)
    context = {
        "elem":item_group
    }
    return render(request,"hod/edit_item_groups.html",context)



@login_required(login_url="account_login")
def view_items(request):
    if not request.user.has_perm('finance.view_item'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.all()
    context = {
        "items":items
    }
    return render(request,"hod/view_items.html", context)

@login_required(login_url="account_login")
def view_low_stock_items(request):
    if not request.user.has_perm('finance.view_item'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.filter(current_stock__lt = F('min_stock'))
    context = {
        "items":items
    }
    return render(request,"hod/view_low_stock_items.html", context)

@login_required(login_url="account_login")
def view_items_id(request,id):
    if not request.user.has_perm('finance.view_item'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    item = get_object_or_404(Item,id=id)
    rate_change_system = "Fixed" if item.rate_change_system==1 else "Last Entry"
    context = {
        "item":item,
        "rate_change_system":rate_change_system
    }
    return render(request,"hod/view_item_id.html",context)

@login_required(login_url="account_login")
def add_item(request):
    if not request.user.has_perm('finance.add_item'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    item_groups = ItemGroup.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        image = request.FILES.get('image')
        item_group_id = request.POST.get('item_group')
        item_group = get_object_or_404(ItemGroup,pk=item_group_id)
        hsn = request.POST.get('hsn')
        unit = request.POST.get('unit')
        tax = request.POST.get('tax')
        rate_change_system = request.POST.get('rate_change_system')
        rate = request.POST.get('rate')
        cur_stock = request.POST.get('cur_stock')
        min_stock = request.POST.get('min_stock')
        unit_plural = request.POST.get('unit_plural')
        if not unit_plural:
            unit_plural = unit+"s"
        elem = Item(
            name=name,
            image=image,
            item_group=item_group,
            hsn_code=hsn,
            rate_change_system=rate_change_system,
            rate=rate,
            unit=unit,
            unit_plural=unit_plural,
            state_tax_rate=tax,
            central_tax_rate = tax,
            integrated_tax_rate = tax*2,
            current_stock=cur_stock,
            min_stock=min_stock
        )

        elem.save()
        messages.success(request,"Item Added Successfully")
    context = {
        "item_groups":item_groups
    }
    return render(request,"hod/add_item.html",context)

@login_required(login_url="account_login")
def edit_item(request,id):
    if not request.user.has_perm('finance.change_item'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    item_groups = ItemGroup.objects.all()
    if request.method == "POST":
        id = request.POST.get('id')
        elem = Item.objects.get(id=int(id))
        elem.name = request.POST.get('name')
        image = request.FILES.get('image')
        if image:
            elem.image = image
        item_group_id = request.POST.get('item_group')
        elem.item_group = get_object_or_404(ItemGroup,pk=item_group_id)
        elem.rate_change_system = request.POST.get('rate_change_system')
        elem.rate = request.POST.get('rate')
        elem.hsn_code = request.POST.get('hsn')
        elem.unit = request.POST.get('unit')
        elem.state_tax_rate = request.POST.get('tax')
        elem.central_tax_rate = request.POST.get('tax')
        elem.integrated_tax_rate = float(request.POST.get('tax')) * 2
        elem.current_stock = request.POST.get('cur_stock')
        elem.min_stock = request.POST.get('min_stock')
        elem.unit_plural = elem.unit+"s"
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user

        elem.save()
        messages.success(request,"Item Updated Successfully")
    item = get_object_or_404(Item,id=id)
    context = {
        "item_groups":item_groups,
        "elem":item
    }
    return render(request,"hod/edit_item.html",context)

@login_required(login_url="account_login")
def delete_item(request,id):
    if not request.user.has_perm('finance.delete_item'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    item = get_object_or_404(Item,id=id)
    item.delete()
    messages.success(request,"Item Deleted Successfully")
    return redirect("view_items")


@login_required(login_url="account_login")
def view_item_adjustment(request):
    if not request.user.has_perm('finance.view_inventoryadjustments'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    inventory_adjustments = InventoryAdjustments.objects.all()


    context = {
        "inventory_adjustments":inventory_adjustments
    }
    return render(request,"hod/view_item_adjustment.html",context)

@login_required(login_url="account_login")
def add_item_adjustment(request):
    if not request.user.has_perm('finance.add_inventoryadjustments'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        qnt = request.POST.get('qnt')
        item_id = request.POST.get('item')
        item = get_object_or_404(Item,id=item_id)
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
            item.current_stock += decimal.Decimal(qnt)
        else:
            item.current_stock -= decimal.Decimal(qnt)
            
        item.save()
        elem.save()
        messages.success(request,"Adjustment Added Successfully")

    return render(request,"hod/add_item_adjustment.html",{
        "items":items
    })


@login_required(login_url="account_login")
def edit_item_adjustment(request,id):
    if not request.user.has_perm('finance.change_inventoryadjustments'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.all()
    elem = InventoryAdjustments.objects.get(id=int(id))
    if request.method == "POST":
        if int(elem.ADJUSTMENT_TYPE) == 1:
            elem.item.current_stock -= decimal.Decimal(elem.quantity)
        else:
            elem.item.current_stock += decimal.Decimal(elem.quantity)
        elem.item.save()
        elem.date = request.POST.get('date')
        elem.quantity = request.POST.get('qnt')
        item_id = request.POST.get('item')
        elem.item = get_object_or_404(Item,id=item_id)
        elem.ADJUSTMENT_TYPE = request.POST.get('type')
        elem.reason_title = request.POST.get('reason_title')
        elem.reason_desc = request.POST.get('reason_desc')
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user
        
        if int(elem.ADJUSTMENT_TYPE) == 1:
            elem.item.current_stock += decimal.Decimal(elem.quantity)
        else:
            elem.item.current_stock -= decimal.Decimal(elem.quantity)
            
        elem.item.save()

        elem.save()
        messages.success(request,"Adjustment Updated Successfully")
        return redirect("edit_item_adjustment",elem.id)

    
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

@login_required(login_url="account_login")
def delete_item_adjustment(request,id):
    if not request.user.has_perm('finance.delete_inventoryadjustments'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    adjustment = get_object_or_404(InventoryAdjustments,id=id)
    if adjustment.ADJUSTMENT_TYPE == 1:
        adjustment.item.current_stock -= adjustment.quantity
    else:
        adjustment.item.current_stock += adjustment.quantity
    adjustment.item.save()
    adjustment.delete()
    messages.success(request,"Item Adjustment Deleted Successfully")
    return redirect("view_item_adjustment")

@login_required(login_url="account_login")
def view_customers(request):
    if not request.user.has_perm('finance.view_customer'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    customers = Customer.objects.all()
    return render(request,"hod/view_customer.html",{
        "customers":customers
    })

@login_required(login_url="account_login")
def view_customers_id(request,id):
    if not request.user.has_perm('finance.view_customer'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    customer = get_object_or_404(Customer,id=id)
    return  render(request,"hod/view_customer_id.html",{
        "elem":customer
    })

@login_required(login_url="account_login")
def add_customer(request):
    if not request.user.has_perm('finance.add_customer'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gstin = request.POST.get('gstin').upper()
        pancard = request.POST.get('pan_card').upper()
        save_last_rate = request.POST.get('save_last_rate')
        current_balance = request.POST.get('balance')

        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address,
            gstin=gstin,
            pancard=pancard,
            current_balance = current_balance,
            save_last_rate=save_last_rate
        )
        
        customer.save()
        messages.success(request,"Customer Saved Successfully")
    return render(request,"hod/add_customer.html")

@login_required(login_url="account_login")
def edit_customer(request,id):
    if not request.user.has_perm('finance.change_customer'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(Customer,id=id)
    if request.method == "POST":
        elem.name = request.POST.get('name')
        elem.email = request.POST.get('email')
        elem.phone = request.POST.get('phone')
        elem.address = request.POST.get('address')
        elem.gstin = request.POST.get('gstin').upper()
        elem.pancard = request.POST.get('pan_card').upper()
        elem.save_last_rate = request.POST.get('save_last_rate')
        elem.current_balance = request.POST.get('balance')
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user

        elem.save()
        messages.success(request,"Customer Updated Successfully")

    
    return render(request,"hod/edit_customer.html",{
        "elem":elem
    })

@login_required(login_url="account_login")
def delete_customer(request,id):
    if not request.user.has_perm('finance.delete_customer'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(Customer,id=id)
    
    elem.delete()
    return redirect("view_customers")

@login_required(login_url="account_login")
def view_invoices(request):
    if not request.user.has_perm('finance.view_invoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    inv_no = request.GET.get("inv_search")
    if inv_no:
        invoices = Invoice.objects.filter(invoice_no__contains=inv_no,valid=True).order_by('-id')
    else:
        invoices = Invoice.objects.filter(valid=True).order_by('-id')
    pagination_applied = True
    if(invoices.count() < 1000):
        invoices_paged = invoices
        pagination_applied = False
    else:
        paginator = Paginator(invoices, 100)  # Show 100 invoices per page
        page_number = request.GET.get('page')
        invoices_paged = paginator.get_page(page_number)

    
    return render(request,"hod/view_invoice.html",{
        "invoices":invoices_paged,
        "pagination_applied":pagination_applied
    })

def add_invoices(request):
    if request.method == "POST":
        print("POSTS:")
        print(request.POST)
        print("\nGETS:")
        print(request.GET)
    current_invoice = Invoice.objects.filter(valid=False)
    if not current_invoice:
        new_invoice_no = get_invoice(Invoice.objects.last().invoice_no)
        current_invoice = Invoice(
            invoice_no=new_invoice_no,
            date=datetime.datetime.today(),
            valid=False
        )
        current_invoice.save()
    else:
        current_invoice = current_invoice[0]
    invoice_no = current_invoice.invoice_no
    date = current_invoice.date
    
    context = {
        "invoice":current_invoice,
        "cash_id":68,
        "invoice_no":invoice_no,
        "day":str(date.day).rjust(2,'0'),
        "month":str(date.month).rjust(2,'0'),
        "year":str(date.year).rjust(4,'0'),
        "customers":Customer.objects.all(),
        "states":state_names,
        "items":Item.objects.all(),
        "clear":False,       # Clear the local Storage
        "realname":"Invoice",
        "work":"Add"
    }
    return render(request,"hod/add_invoice.html",context)

def edit_invoice(request,id=None):

    if not id:
        return redirect("add_invoices")
    try:
        current_invoice = Invoice.objects.get(id=id)
    except Invoice.DoesNotExist:
        return redirect("add_invoices")
    invoice_no = current_invoice.invoice_no
    date = current_invoice.date
    extra_details = current_invoice.extra_details
    if not extra_details:
        extra_details = '{}'
    context = {
        "invoice":current_invoice,
        "cash_id":68,
        "invoice_no":invoice_no,
        "day":str(date.day).rjust(2,'0'),
        "month":str(date.month).rjust(2,'0'),
        "year":str(date.year).rjust(4,'0'),
        "customers":Customer.objects.all(),
        "states":state_names,
        "items":Item.objects.all(),
        "transactions":current_invoice.transaction_set.all(),
        "extra_details": json.loads(extra_details),
        "clear":True,        # Clear the localStorage
        "realname": "Invoice",
        "work":"Edit"
    }
    return render(request,"hod/edit_invoice.html",context)
def reset_invoice(request):
    invoice = Invoice.objects.last()
    for i in invoice.transaction_set.all():
        i.delete()
    invoice.total_amount = 0
    invoice.total_taxable_amount = 0
    invoice.total_state_tax_amount = 0
    invoice.total_central_tax_amount = 0
    invoice.total_integrated_tax_amount = 0
    invoice.extra_details = ""
    invoice.save()
    return redirect("add_invoices")

@login_required(login_url="account_login")
def delete_invoice(request,id):
    if not request.user.has_perm('finance.delete_invoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    invoice = get_object_or_404(Invoice,id=id)

    invoice.delete()
    return redirect("view_invoices")

@login_required(login_url="account_login")
def view_payments(request):
    if not request.user.has_perm('finance.view_payment'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    payments = Payment.objects.all()

    return render(request,"hod/view_payments.html",{
        "payments":payments
    })

@login_required(login_url="account_login")
def add_payment(request):
    if not request.user.has_perm('finance.add_payment'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    customers = Customer.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        desc = request.POST.get('desc')
        customer_id = request.POST.get('customer_id')
        customer = get_object_or_404(Customer,id=customer_id)
        mode = request.POST.get('mode')
        amount = request.POST.get('amount')
        elem = Payment(
            date = date, 
            description = desc,
            customer = customer,
            mode=mode,
            amount = amount
        )

        elem.save()
        elem.customer.current_balance -= decimal.Decimal(amount)
        elem.customer.save()
        messages.success(request,"Payment Added Successfully")
    context = {
        "customers":customers
    }
    return render(request,"hod/add_payment.html",context)

@login_required(login_url="account_login")
def edit_payment(request,id):
    if not request.user.has_perm('finance.change_payment'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    customers = Customer.objects.all()
    elem = get_object_or_404(Payment,id=id)
    if request.method == "POST":
        elem.customer.current_balance += decimal.Decimal(elem.amount)
        elem.customer.save()
        
        elem.date = request.POST.get('date')
        elem.description = request.POST.get('desc')
        customer_id = request.POST.get('customer_id')
        elem.customer = get_object_or_404(Customer,id=customer_id)
        elem.mode = request.POST.get('mode')
        elem.amount = request.POST.get('amount')
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user

        elem.customer.current_balance -= decimal.Decimal(elem.amount)
        elem.customer.save()
        elem.save()
        messages.success(request,"Payment Updated Successfully")
        return redirect("edit_payment",id)
    
    day = str(elem.date.day).rjust(2,"0")
    month = str(elem.date.month).rjust(2,"0")
    year = str(elem.date.year).rjust(4,"0")
    context = {
        "customers":customers,
        "elem":elem,
        "day":day,
        "month":month,
        "year":year
    }

    return render(request,"hod/edit_payment.html",context)

@login_required(login_url="account_login")
def delete_payment(request,id):
    if not request.user.has_perm('finance.delete_payment'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(Payment,id=id)
    elem.customer.current_balance += decimal.Decimal(elem.amount)
    elem.customer.save()
    elem.delete()
    return redirect("view_payments")

@login_required(login_url="account_login")
def view_salereturns(request):
    if not request.user.has_perm('finance.view_salereturn'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    sale_return = SaleReturn.objects.all()
    return render(request,"hod/view_salereturn.html",{
        "sale_return":sale_return
    })

@login_required(login_url="account_login")
def add_salereturn(request):
    if not request.user.has_perm('finance.add_salereturn'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.all()
    customers = Customer.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        qnt = request.POST.get('qnt')
        customer_id = request.POST.get('customer_id')
        customer = get_object_or_404(Customer,id=customer_id)
        item_id = request.POST.get('item')
        item = get_object_or_404(Item,id=item_id)
        desc = request.POST.get('desc')
        amount = request.POST.get('amount')


        elem = SaleReturn(
            date=date,
            customer=customer,
            item=item,
            quantity=qnt,
            description=desc,
            amount=amount
            
        )
        # Do The Changes to other models Here
        item.current_stock += decimal.Decimal(qnt)
        item.save()
        
        elem.save()
        messages.success(request,"Sale Return Added Successfully")

    context = {
        "items":items,
        "customers":customers,
    }
    return render(request,"hod/add_salereturn.html",context)


@login_required(login_url="account_login")
def delete_salereturn(request,id):
    if not request.user.has_perm('finance.delete_salereturn'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(SaleReturn,id=id)
    elem.item.current_stock += decimal.Decimal(elem.quantity)
    elem.item.save()

    elem.delete()
    return redirect("view_salereturns")

@login_required(login_url="account_login")
def edit_salereturn(request,id):
    if not request.user.has_perm('finance.change_salereturn'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.all()
    customers = Customer.objects.all()
    elem = SaleReturn.objects.get(id=int(id))
    if request.method == "POST":
        elem.item.current_stock -= elem.quantity 
        elem.item.save()
        
        id = request.POST.get('id')
        elem = SaleReturn.objects.get(id=int(id))
        elem.date = request.POST.get('date')
        elem.quantity = request.POST.get('qnt')
        item_id = request.POST.get('item')
        elem.item = get_object_or_404(Item,id=item_id)
        customer_id = request.POST.get('customer_id')
        elem.customer = get_object_or_404(Customer,id=customer_id)
        elem.description = request.POST.get('desc')
        elem.amount = request.POST.get('amount')
        elem.status = int(request.POST.get('status'))
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user
        
        # Do The Changes to other models Here
        elem.item.current_stock += decimal.Decimal(elem.quantity)
        elem.item.save()

        elem.save()
        messages.success(request,"Sale Return Updated Successfully")
        return redirect("edit_salereturn",elem.id)

    
    day = str(elem.date.day).rjust(2,"0")
    month = str(elem.date.month).rjust(2,"0")
    year = str(elem.date.year).rjust(4,"0")

    return render(request,"hod/edit_salereturn.html",{
        "items":items,
        "customers":customers,
        "elem":elem,
        "day":day,
        "month":month,
        "year":year
    })



    

def redeem_salereturn(request,id):
    elem = SaleReturn.objects.get(id=id)
    elem.status = 2
    elem.save()
    return  redirect("view_salereturns")


   

# AJAX
def get_tax_quantity(request):
    '''
    $('#rate').val(data.rate);
        $('#tax').val(data.tax);
        $('#current_stock').val(data.available_quantity);
    '''
    customer_id = request.GET.get('customer_id')
    customer = get_object_or_404(Customer,id=customer_id)

    item_id = request.GET.get('item_id')
    item = get_object_or_404(Item,id=item_id)
    

    data = {
            "tax":item.state_tax_rate,
            "available_quantity":item.current_stock,
            "edit_item_url": reverse("edit_item",args=[item.id])
        }
    
    # check if lastItemrate present
    last_rate = LastItemRate.objects.filter(party=customer,item=item)
    if last_rate:data["rate"] = last_rate[0].rate
    else:data["rate"] = item.rate
        
    
    return JsonResponse(data)

# Ajax
def save_invoice(request):
    # get async data 
    '''
    data = {
    "invoice_no":invoice_no,
    "date":date,
    "customer":customer,
    "tax_type":tax_type,
    "change_shipping_address":change_shipping_address,
    "customer_shipping":customer_shipping,
    "state":state,
    "address":address,
    "transaction":transaction,
    "transaction_addon":transaction_addon
  }
    '''
    invoice_no = request.GET.get('invoice_no')
    date = request.GET.get('date')
    customer_id = request.GET.get('customer_id')
    tax_type = request.GET.get('tax_type')
    change_shipping_address = request.GET.get('change_shipping_address')
    shipping_customer_name = request.GET.get('shipping_customer_name')
    state = request.GET.get('state')
    address = request.GET.get('address')
    transaction = request.GET.get('transaction')
    transaction_addon = request.GET.get('transaction_addon')
    shipping = None

    if customer_id.isdigit():
        customer_id = int(customer_id)
    else:
        return JsonResponse({
            "error":"customer id is invalid"
        })
    

    # Name of Customer who is Purchasing 
    try:
        customer = Customer.objects.get(id=(customer_id))      # we need customer in both cases (shipping = true or false)
    except Customer.DoesNotExist:
        return JsonResponse({
            "error":"No such Customer Found"
        })
    if change_shipping_address == "true" and not (shipping_customer_name and state and address):
        return JsonResponse({
            "error":"Invalid Shipping Details"
        })
    print(shipping_customer_name,state,address,sep=", ")
    if change_shipping_address == "true":
        # Name of party where the goods are being transported
        shipping = ShippingDetail(
            name = shipping_customer_name,
            state = state,
            address = address
        )
        shipping.save()

    # print(customer,type(customer))
    
    invoice = Invoice.objects.filter(invoice_no=invoice_no)
    if len(invoice) == 1:
        invoice = invoice[0]
    elif len(invoice) > 1:
        return JsonResponse({
            "error":"More than one invoice with same inv no"
        })
    else:
        return JsonResponse({
            "error":"No such invoices found"
        })
    # invoice.invoice_no = invoice_no
    invoice.customer = customer
    invoice.date = date
    invoice.shipping_details = shipping
    invoice.save()
    # add transaction
    separator = "$$$"
    divide_separator = "$$$&&^^@#"
    
    transaction = transaction.split(divide_separator)
    # transaction_addon = {}
    # transaction_addon = transaction_addon.split(divide_separator)

    total_taxable_amount = 0
    total_state_tax_amount = 0
    total_central_tax_amount = 0
    total_integrated_tax_amount = 0
    total_invoice_amount = 0

    for tr in transaction:
        x = tr.split(separator)
        if len(x)!=7:
            continue
        sl_no,item,tax,qnt,rate,dis_per,taxable_value = x
        
        "Should i get the item from `name` or `id` ??"
        item = get_object_or_404(Item,name=item)
        
        # print(taxable_value,type(taxable_value), dis_per,type(dis_per))
        taxable_value = float(taxable_value)
        dis_per = float(dis_per)
        dis_amt = taxable_value * dis_per / 100
        tr = Transaction(
            invoice=invoice,
            item = item,
            quantity = qnt,
            rate = rate,
            taxable_value = taxable_value,
            discount_percent = dis_per,
            discount_amount = dis_amt,
        )
        x = (taxable_value - dis_amt) 
        total_taxable_amount += x
        if tax_type=="1":
            total_state_tax_amount += (x * item.state_tax_rate/100)
            total_central_tax_amount += (x * item.central_tax_rate/100)
        else:
            total_integrated_tax_amount += (x * item.integrated_tax_rate / 100)
        total_invoice_amount += x * (1 + (item.state_tax_rate+item.central_tax_rate)/100)
        tr.save()

    l = transaction_addon.split(divide_separator)
    json_dict = {}
    # makeit to json (name,value) pair
    for i in l:
        if i:
            name,value = i.split(separator)
            json_dict[name] = value

    # add to invoice
    invoice.extra_details = json.dumps(json_dict)
    
    # tax calculation
    invoice.total_taxable_amount = total_taxable_amount
    invoice.total_state_tax_amount = total_state_tax_amount
    invoice.total_central_tax_amount = total_central_tax_amount
    invoice.total_integrated_tax_amount = total_integrated_tax_amount
    invoice.total_amount = total_invoice_amount
    
    
    invoice.valid = True
    invoice.save()


    # invoice.delete()
    return JsonResponse({
        "status":"success"
        })
    