from django.contrib import admin
from django.urls import path,include

from finance import report_views, vendor_views

from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name="finance_dashboard"),

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
    path('add_customers/',views.add_customer,name="add_customers"),
    path('view_customers/<int:id>/',views.view_customers_id,name="view_customers_id"),
    path('edit_customers/<int:id>/',views.edit_customer,name="edit_customer"),
    path('delete_customer/<int:id>/',views.delete_customer,name="delete_customer"),


    #Invoice
    path('view_invoices/',views.view_invoices,name="view_invoices"),
    path('add_invoices/',views.add_invoice,name="add_invoices"),
    # path('view_invoices/<int:id>/',views.view_invoices_id,name="view_invoices_id"),
    path('edit_invoices/<int:id>/',views.edit_invoice,name="edit_invoice"),
    path('delete_invoice/<int:id>/',views.delete_invoice,name="delete_invoice"),
    path('save_transaction/',views.save_transaction,name="save_transaction"),
    path('save_edit_transaction/<int:id>',views.save_edit_transaction,name="save_edit_transaction"),
    path('delete_transaction/<int:id>',views.delete_transaction,name="delete_transaction"),

    #payments
    path('view_payments/',views.view_payments,name="view_payments"),
    path('add_payments/',views.add_payment,name="add_payments"),
    path('edit_payments/<int:id>/',views.edit_payment,name="edit_payment"),
    path('delete_payment/<int:id>/',views.delete_payment,name="delete_payment"),

    #sale return
    path('view_salereturns/',views.view_salereturns,name="view_salereturns"),
    path('add_salereturns/',views.add_salereturn,name="add_salereturns"),
    path('edit_salereturns/<int:id>/',views.edit_salereturn,name="edit_salereturn"),
    path('delete_salereturn/<int:id>/',views.delete_salereturn,name="delete_salereturn"),
    path('redeem_salereturn/<int:id>/',views.redeem_salereturn,name="sale_return_redeem"),

    #Vendors
    path('view_vendors/',vendor_views.view_vendors,name="view_vendors"),
    path('add_vendors/',vendor_views.add_vendor,name="add_vendors"),
    path('view_vendors/<int:id>/',vendor_views.view_vendors_id,name="view_vendors_id"),
    path('edit_vendors/<int:id>/',vendor_views.edit_vendor,name="edit_vendor"),
    path('delete_vendor/<int:id>/',vendor_views.delete_vendor,name="delete_vendor"),

    #purchase invoices
    path('view_purchase_invoices/',vendor_views.view_purchase_invoices,name="view_purchase_invoices"),
    path('add_purchase_invoices/',vendor_views.add_purchase_invoice,name="add_purchase_invoices"),
    # path('view_purchase_invoices/<int:id>/',vendor_views.view_purchase_invoices_id,name="view_purchase_invoices_id"),
    path('edit_purchase_invoices/<int:id>/',vendor_views.edit_purchase_invoice,name="edit_purchase_invoice"),
    path('delete_purchase_invoice/<int:id>/',vendor_views.delete_purchase_invoice,name="delete_purchase_invoice"),
    path('save_purchase_transaction/',vendor_views.save_purchase_transaction,name="save_purchase_transaction"),
    path('save_edit_purchase_transaction/<int:id>',vendor_views.save_edit_purchase_transaction,name="save_edit_purchase_transaction"),
    path('delete_purchase_transaction/<int:id>',vendor_views.delete_purchase_transaction,name="delete_purchase_transaction"),

    #reciepts
    path('view_reciepts/',vendor_views.view_reciepts,name="view_reciepts"),
    path('add_reciepts/',vendor_views.add_reciept,name="add_reciepts"),
    path('edit_reciepts/<int:id>/',vendor_views.edit_reciept,name="edit_reciept"),
    path('delete_reciept/<int:id>/',vendor_views.delete_reciept,name="delete_reciept"),

    # My Credit Notes
    path('view_vendor_credit_notes/',vendor_views.view_vendor_credit_notes,name="view_vendor_credit_notes"),
    path('view_vendor_credit_notes/',vendor_views.view_vendor_credit_notes,name="view_vendor_credit_notes"),
    path('add_vendor_credit_notes/',vendor_views.add_vendor_credit_note,name="add_vendor_credit_notes"),
    path('edit_vendor_credit_notes/<int:id>/',vendor_views.edit_vendor_credit_note,name="edit_vendor_credit_note"),
    path('delete_vendor_credit_note/<int:id>/',vendor_views.delete_vendor_credit_note,name="delete_vendor_credit_note"),
    path('redeem_vendor_credit_note/<int:id>/',vendor_views.redeem_vendor_credit_note,name="my_credit_redeem"),

    # Reports
    path('report_sales_customer/',report_views.sales_by_customer,name="report_sales_customer"),
    path('report_sales_item/',report_views.sales_by_item,name="report_sales_item"),
    path('report_payment_customer/',report_views.payments_by_customers,name="report_payment_customer"),
    # path('report_payment_item/',report_views.sales_by_item,name="report_payment_item"),
    
    path('report_inventory_item/',report_views.inventory_by_items,name="report_inventory_item"),



    path("test/",vendor_views.testme,name="testme"),

    path('get_available_quantity/', views.get_available_quantity, name='available_quantity')
]
