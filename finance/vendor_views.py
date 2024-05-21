import datetime
import decimal,json
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from finance.models import Item, PurchaseInvoice, PurchaseTransaction, Reciept, Vendor,VendorCreditNote, LastItemRate, RelatedFile, PurchaseInvoiceDetails
from django.contrib import messages
from finance.common import state_names

@login_required(login_url="account_login")
def view_vendors(request):
    if not request.user.has_perm('finance.view_vendor'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    vendors = Vendor.objects.all()
    return render(request,"hod/view_vendor.html",{
        "vendors":vendors
    })

@login_required(login_url="account_login")
def view_vendors_id(request,id):
    if not request.user.has_perm('finance.view_vendor'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    vendor = get_object_or_404(Vendor,id=id)
    return  render(request,"hod/view_vendor_id.html",{
        "elem":vendor
    })

@login_required(login_url="account_login")
def add_vendor(request):
    if not request.user.has_perm('finance.add_vendor'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
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

@login_required(login_url="account_login")
def edit_vendor(request,id):
    if not request.user.has_perm('finance.change_vendor'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(Vendor,id=id)
    if request.method == "POST":
        elem.name = request.POST.get('name')
        elem.email = request.POST.get('email')
        elem.phone = request.POST.get('phone')
        elem.address = request.POST.get('address')
        elem.gstin = request.POST.get('gstin')
        elem.current_balance = request.POST.get('balance')
        elem.company = request.POST.get('company')
        elem.website = request.POST.get('website')
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user

        elem.save()
        messages.success(request,"Vendor Updated Successfully")

    
    return render(request,"hod/edit_vendor.html",{
        "elem":elem
    })

@login_required(login_url="account_login")
def delete_vendor(request,id):
    if not request.user.has_perm('finance.delete_vendor'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(Vendor,id=id)
    
    elem.delete()
    return redirect("view_vendors")


@login_required(login_url="account_login")
def view_purchase_invoices(request):
    if not request.user.has_perm('finance.view_purchaseinvoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    purchase_invoices = PurchaseInvoiceDetails.objects.all()
    return render(request,"hod/view_purchase.html",{
        "purchase_invoices":purchase_invoices
    })



@login_required(login_url="account_login")
def add_purchase_invoice(request):
    if not request.user.has_perm('finance.add_purchaseinvoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    context = {
        "vendors":Vendor.objects.all(),
        "items":Item.objects.all(),
        "states":state_names,
    }
    return render(request,'hod/add_purchase.html',context)


@login_required(login_url="account_login")
def delete_purchase_invoice(request,id):
    if not request.user.has_perm('finance.delete_purchaseinvoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    purchase_invoice = get_object_or_404(PurchaseInvoice,id=id)
    if purchase_invoice.valid:
        purchase_invoice.vendor.current_balance += purchase_invoice.total_amount
        purchase_invoice.vendor.save()
        for tr in purchase_invoice.purchasetransaction_set.all():
            tr.item.current_stock -= tr.quantity
            tr.item.save()

    purchase_invoice.delete()
    return redirect("view_purchase_invoices")



@login_required(login_url="account_login")
def edit_purchase_invoice(request,id):
    if not request.user.has_perm('finance.change_purchaseinvoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    vendors = Vendor.objects.all()
    items = Item.objects.all()
    #get purchase_invoice
    current_purchase_invoice = get_object_or_404(PurchaseInvoice,id=id)
    purchase_transactions = current_purchase_invoice.purchasetransaction_set.all()
    if request.method == "POST":
        if current_purchase_invoice.valid:
            current_purchase_invoice.vendor.current_balance += current_purchase_invoice.total_amount
            current_purchase_invoice.vendor.save()
            for tr in current_purchase_invoice.transaction_set.all():
                tr.item.current_stock -= tr.quantity
                tr.item.save()
            
        current_purchase_invoice.invoice_no = request.POST.get('purchase_invoice_no')
        current_purchase_invoice.date = request.POST.get('date')
        purchase_invoice_file = request.FILES.get("purchase_invoice_file")
        if purchase_invoice_file:
            current_purchase_invoice.file_invoice = purchase_invoice_file
        vendor_id = request.POST.get('vendor_id')
        vendor = get_object_or_404(Vendor,id=vendor_id)
        current_purchase_invoice.vendor = vendor
        current_purchase_invoice.valid = True
        current_purchase_invoice.updated_at = datetime.datetime.now()
        current_purchase_invoice.changed_by_user = request.user

        current_purchase_invoice.vendor.current_balance -= current_purchase_invoice.total_amount
        current_purchase_invoice.vendor.save()
        for tr in current_purchase_invoice.transaction_set.all():
            tr.item.current_stock += tr.quantity
            tr.item.save()

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
        "purchase_transactions":purchase_transactions
    })


@login_required(login_url="account_login")
def save_purchase_transaction(request):
    if not request.user.has_perm('finance.add_purchaseinvoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    if request.method == "POST":
        purchase_invoice_id = request.POST.get("purchase_invoice_id")
        purchase_invoice = get_object_or_404(PurchaseInvoice,id=purchase_invoice_id)
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

        
        

        purchase_transaction = PurchaseTransaction(
            invoice = purchase_invoice,
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

        purchase_transaction.save()
        purchase_invoice.total_taxable_amount += purchase_transaction.taxable_value
        purchase_invoice.total_tax_amount += purchase_transaction.state_tax + purchase_transaction.central_tax
        purchase_invoice.total_amount += purchase_transaction.amount 
        purchase_invoice.save()

    return redirect("add_purchase_invoices")

@login_required(login_url="account_login")
def save_edit_purchase_transaction(request,id):
    if not request.user.has_perm('finance.change_purchaseinvoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    if request.method == "POST":
        purchase_invoice_id = request.POST.get("purchase_invoice_id")
        purchase_invoice = get_object_or_404(PurchaseInvoice,id=purchase_invoice_id)
        item_id = request.POST.get('item')
        item = get_object_or_404(Item,id=int(item_id))

        qnt = decimal.Decimal(request.POST.get('qnt'))
        amount = decimal.Decimal(request.POST.get('amount'))
        discount = request.POST.get('discount')
        rate = amount / qnt
        taxable_amount = amount / (1 + decimal.Decimal(item.state_tax_rate*2) / 100)
        tax_amount = taxable_amount * decimal.Decimal(item.state_tax_rate) / 100 * 2


        purchase_transaction = PurchaseTransaction(
            invoice = purchase_invoice,
            item = item,
            quantity = qnt,
            rate = rate,
            discount = discount,
            tax = tax_amount,
            amount = amount

        )
        purchase_transaction.updated_at = datetime.datetime.now()
        purchase_transaction.changed_by_user = request.user
        purchase_transaction.save()
        purchase_invoice.total_amount += purchase_transaction.amount 
        purchase_invoice.save()

    return redirect("edit_purchase_invoice",id)

@login_required(login_url="account_login")
def delete_purchase_transaction(request,id):
    if not request.user.has_perm('finance.delete_purchaseinvoice'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(PurchaseTransaction,id=id)
    elem.invoice.total_amount -= elem.amount
    elem.invoice.save()
    elem.delete()

    return redirect("add_purchase_invoices")

@login_required(login_url="account_login")
def view_reciepts(request):
    if not request.user.has_perm('finance.view_reciept'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    reciepts = Reciept.objects.all()

    return render(request,"hod/view_reciepts.html",{
        "reciepts":reciepts
    })

@login_required(login_url="account_login")
def add_reciept(request):
    if not request.user.has_perm('finance.add_reciept'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    vendors = Vendor.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        desc = request.POST.get('desc')
        vendor_id = request.POST.get('vendor_id')
        vendor = get_object_or_404(Vendor,id=vendor_id)
        mode = request.POST.get('mode')
        amount = request.POST.get('amount')
        elem = Reciept(
            date = date, 
            description = desc,
            vendor = vendor,
            mode=mode,
            amount = amount
        )

        elem.save()
        elem.vendor.current_balance += decimal.Decimal(amount)
        elem.vendor.save()
        messages.success(request,"Reciept Added Successfully")
    context = {
        "vendors":vendors
    }
    return render(request,"hod/add_reciept.html",context)

@login_required(login_url="account_login")
def edit_reciept(request,id):
    if not request.user.has_perm('finance.change_reciept'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    vendors = Vendor.objects.all()
    elem = get_object_or_404(Reciept,id=id)
    if request.method == "POST":
        elem.vendor.current_balance -= decimal.Decimal(elem.amount)
        elem.vendor.save()
        
        elem.date = request.POST.get('date')
        elem.description = request.POST.get('desc')
        vendor_id = request.POST.get('vendor_id')
        elem.vendor = get_object_or_404(Vendor,id=vendor_id)
        elem.mode = request.POST.get('mode')
        elem.amount = request.POST.get('amount')
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user

        elem.vendor.current_balance += decimal.Decimal(elem.amount)
        elem.vendor.save()
        elem.save()
        messages.success(request,"Reciept Updated Successfully")
        return redirect("edit_reciept",id)
    
    day = str(elem.date.day).rjust(2,"0")
    month = str(elem.date.month).rjust(2,"0")
    year = str(elem.date.year).rjust(4,"0")
    context = {
        "vendors":vendors,
        "elem":elem,
        "day":day,
        "month":month,
        "year":year
    }

    return render(request,"hod/edit_reciept.html",context)

@login_required(login_url="account_login")
def delete_reciept(request,id):
    if not request.user.has_perm('finance.delete_reciept'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    elem = get_object_or_404(Reciept,id=id)
    elem.vendor.current_balance -= decimal.Decimal(elem.amount)
    elem.vendor.save()
    elem.delete()
    return redirect("view_reciepts")


@login_required(login_url="account_login")
def view_vendor_credit_notes(request):
    if not request.user.has_perm('finance.view_vendorcreditnote'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    credit_note = VendorCreditNote.objects.all()
    return render(request,"hod/view_vendor_notes.html",{
        "credit_note":credit_note
    })

@login_required(login_url="account_login")
def add_vendor_credit_note(request):
    if not request.user.has_perm('finance.add_vendorcreditnote'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.all()
    vendors = Vendor.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        qnt = request.POST.get('qnt')
        vendor_id = request.POST.get('vendor_id')
        vendor = get_object_or_404(Vendor,id=vendor_id)
        item_id = request.POST.get('item')
        item = get_object_or_404(Item,id=item_id)
        desc = request.POST.get('desc')
        amount = request.POST.get('amount')


        elem = VendorCreditNote(
            date=date,
            vendor=vendor,
            item=item,
            quantity=qnt,
            description=desc,
            amount=amount
            
        )
        # Do The Changes to other models Here
        item.current_stock -= decimal.Decimal(qnt)
        item.save()

        elem.save()
        messages.success(request,"Credit Note Added Successfully")

    context = {
        "items":items,
        "vendors":vendors,
    }
    return render(request,"hod/add_vendor_note.html",context)


@login_required(login_url="account_login")
def delete_vendor_credit_note(request,id):
    if not request.user.has_perm('finance.delete_vendorcreditnote'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    # elem = get_object_or_404(VendorCreditNote,id=id)
    # elem.item.current_stock -= decimal.Decimal(elem.quantity)
    # elem.item.save()

    elem.delete()
    return redirect("view_vendor_credit_notes")

@login_required(login_url="account_login")
def edit_vendor_credit_note(request,id):
    if not request.user.has_perm('finance.change_vendorcreditnote'):
        return HttpResponse("Permission Error. Sorry You are not authorised to visit this page")
    items = Item.objects.all()
    vendors = Vendor.objects.all()
    elem = VendorCreditNote.objects.get(id=int(id))
    if request.method == "POST":
        elem.item.current_stock += decimal.Decimal(elem.quantity)
        elem.item.save()

        id = request.POST.get('id')
        elem = VendorCreditNote.objects.get(id=int(id))
        elem.date = request.POST.get('date')
        elem.quantity = request.POST.get('qnt')
        item_id = request.POST.get('item')
        elem.item = get_object_or_404(Item,id=item_id)
        vendor_id = request.POST.get('vendor_id')
        elem.vendor = get_object_or_404(Vendor,id=vendor_id)
        elem.description = request.POST.get('desc')
        elem.amount = request.POST.get('amount')
        elem.status = int(request.POST.get('status'))
        elem.updated_at = datetime.datetime.now()
        elem.changed_by_user = request.user

        # Do The Changes to other models Here
        # elem.item.current_stock -= decimal.Decimal(elem.quantity)
        # elem.item.save()
        
        elem.save()
        messages.success(request,"Credit Note Updated Successfully")
        return redirect("edit_vendor_credit_note",elem.id)

    
    day = str(elem.date.day).rjust(2,"0")
    month = str(elem.date.month).rjust(2,"0")
    year = str(elem.date.year).rjust(4,"0")

    return render(request,"hod/edit_vendor_note.html",{
        "items":items,
        "vendors":vendors,
        "elem":elem,
        "day":day,
        "month":month,
        "year":year
    })

def redeem_vendor_credit_note(request,id):
    elem = VendorCreditNote.objects.get(id=id)
    elem.status = 2
    elem.save()
    return redirect("view_vendor_credit_notes")


def testme(request):
    context = {
        
    }
    return render(request,'hod/base_invoice.html',context=context)





# AJAX (async)

def save_purchase_invoice(request):
    # get async data 
    '''
    data = {
    "invoice_no":invoice_no,
    "date":date,
    "customer":customer,
    "tax_type":tax_type,
    "file_id":file_id,
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
    customer_id = request.GET.get('customer_id')    # vendor id
    tax_type = request.GET.get('tax_type')
    file_id = request.GET.get('file_id')
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
        vendor = Vendor.objects.get(id=(customer_id))      # we need customer in both cases (shipping = true or false)
    except Vendor.DoesNotExist:
        return JsonResponse({
            "error":"No such Vendor Found"
        })
    try:
        if file_id:
            file = RelatedFile.objects.get(id=int(file_id))      # we need customer in both cases (shipping = true or false)
    except RelatedFile.DoesNotExist:
        return JsonResponse({
            "error":"No such File Found"
        })
    except:
        return JsonResponse({
            "error":"Invalid id"
        })
    if change_shipping_address == "true" and (shipping_customer_name and state and address):
        return JsonResponse({
            "error":"Invalid Shipping Details"
        })
    if change_shipping_address == "true":
        # Name of party where the goods are being transported
        shipping = ShippingDetail(
            name = shipping_customer_name,
            state = state,
            address = address
        )
        shipping.save()
    

    # print(customer,type(customer))
    
    invoice = PurchaseInvoiceDetails(
        invoice_no = invoice_no
    )
    invoice.vendor = vendor
    invoice.date = date
    invoice.shipping_details = shipping
    invoice.save()

    base_invoice = PurchaseInvoice(
        file=file,
        details=invoice
    )
    base_invoice.save()
    # add transaction
    separator = "$$$"
    divide_separator = "$$$&&^^@#"
    
    transaction = transaction.split(divide_separator)
    # transaction_addon = {}
    # transaction_addon = transaction_addon.split(divide_separator)

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
        tr = PurchaseTransaction(
            invoice=invoice,
            item = item,
            quantity = qnt,
            rate = rate,
            taxable_value = taxable_value,
            discount_percent = dis_per,
            discount_amount = dis_amt,
        )
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
    
    invoice.valid = True
    invoice.save()


    # invoice.delete()
    return JsonResponse({
        "status":"success"
        })


def get_tax_quantity(request):
    '''
    $('#rate').val(data.rate);
        $('#tax').val(data.tax);
        $('#current_stock').val(data.available_quantity);
    '''
    vendor_id = request.GET.get('customer_id')
    vendor = get_object_or_404(Vendor,id=vendor_id)

    item_id = request.GET.get('item_id')
    item = get_object_or_404(Item,id=item_id)
    

    data = {
            "tax":item.state_tax_rate,
            "available_quantity":item.current_stock,
            "edit_item_url": reverse("edit_item",args=[item.id])
        }
    
        
    
    return JsonResponse(data)

