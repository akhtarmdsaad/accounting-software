from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from finance.models import ItemGroup, Item,InventoryAdjustments,Customer
import datetime

# Create your views here.
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
        elem.image = request.FILES.get('image')
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
    item = InventoryAdjustments.objects.get(id=id)
    item.delete()
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