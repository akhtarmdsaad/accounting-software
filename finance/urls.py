from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.dashboard,name="finance_dashboard"),

    #items
    path('view_item_groups/',views.view_item_groups,name="view_item_groups"),
    path('add_item_groups/',views.add_item_groups,name="add_item_groups"),
    path('edit_item_groups/<int:id>/',views.edit_item_groups,name="edit_item_groups"),
    path('delete_item_groups/<int:id>/',views.delete_item_groups,name="delete_item_groups"),
    
    path('view_items/',views.view_items,name="view_items"),
    path('add_items/',views.add_item,name="add_items"),
    path('view_items/<int:id>/',views.view_items_id,name="view_items_id"),
    path('edit_items/<int:id>/',views.edit_item,name="edit_item"),
    path('delete_item/<int:id>/',views.delete_item,name="delete_item"),
    
    path('view_item_adjustment/',views.view_item_adjustment,name="view_item_adjustment"),
    path('add_item_adjustments/',views.add_item_adjustment,name="add_item_adjustment"),
    path('edit_item_adjustments/<int:id>/',views.edit_item_adjustment,name="edit_item_adjustment"),
    path('delete_item_adjustment/<int:id>/',views.delete_item_adjustment,name="delete_item_adjustment"),

    #Customer
    path('view_customers/',views.view_customers,name="view_customers"),
    # path('add_customers/',views.add_customer,name="add_customers"),
    path('view_customers/<int:id>/',views.view_customers_id,name="view_customers_id"),
    # path('edit_customers/<int:id>/',views.edit_customer,name="edit_customer"),
    # path('delete_customer/<int:id>/',views.delete_customer,name="delete_customer"),

]
