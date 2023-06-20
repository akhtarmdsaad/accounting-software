from django.shortcuts import render,HttpResponse
from django.contrib import messages
from finance.models import ItemGroup, Item,InventoryAdjustments

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
