# Generated by Django 4.2.3 on 2023-07-23 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0025_item_central_tax_rate_item_integrated_tax_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='shiipping_state',
            field=models.IntegerField(choices=[(1, 'Andaman & Nicobar Islands'), (2, 'Andhra Pradesh'), (3, 'Arunachal Pradesh'), (4, 'Assam'), (5, 'Bihar'), (6, 'Chandigarh'), (7, 'Chhattisgarh'), (8, 'Dadra & Nagar Haveli and Daman & Diu'), (9, 'Delhi'), (10, 'Goa'), (11, 'Gujarat'), (12, 'Haryana'), (13, 'Himachal Pradesh'), (14, 'Jammu & Kashmir'), (15, 'Jharkhand'), (16, 'Karnataka'), (17, 'Kerala'), (18, 'Ladakh'), (19, 'Lakshadweep'), (20, 'Madhya Pradesh'), (21, 'Maharashtra'), (22, 'Manipur'), (23, 'Meghalaya'), (24, 'Mizoram'), (25, 'Nagaland'), (26, 'Odisha'), (27, 'Puducherry'), (28, 'Punjab'), (29, 'Rajasthan'), (30, 'Sikkim'), (31, 'Tamil Nadu'), (32, 'Telangana'), (33, 'Tripura'), (34, 'Uttarakhand'), (35, 'Uttar Pradesh'), (36, 'West Bengal')], null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='shipping_address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='shipping_customer',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
