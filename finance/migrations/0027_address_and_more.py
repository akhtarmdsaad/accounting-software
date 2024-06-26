# Generated by Django 4.2.3 on 2023-07-28 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0026_invoice_shiipping_state_invoice_shipping_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=50, verbose_name='address')),
                ('state', models.IntegerField(choices=[(1, 'Andaman & Nicobar Islands'), (2, 'Andhra Pradesh'), (3, 'Arunachal Pradesh'), (4, 'Assam'), (5, 'Bihar'), (6, 'Chandigarh'), (7, 'Chhattisgarh'), (8, 'Dadra & Nagar Haveli and Daman & Diu'), (9, 'Delhi'), (10, 'Goa'), (11, 'Gujarat'), (12, 'Haryana'), (13, 'Himachal Pradesh'), (14, 'Jammu & Kashmir'), (15, 'Jharkhand'), (16, 'Karnataka'), (17, 'Kerala'), (18, 'Ladakh'), (19, 'Lakshadweep'), (20, 'Madhya Pradesh'), (21, 'Maharashtra'), (22, 'Manipur'), (23, 'Meghalaya'), (24, 'Mizoram'), (25, 'Nagaland'), (26, 'Odisha'), (27, 'Puducherry'), (28, 'Punjab'), (29, 'Rajasthan'), (30, 'Sikkim'), (31, 'Tamil Nadu'), (32, 'Telangana'), (33, 'Tripura'), (34, 'Uttarakhand'), (35, 'Uttar Pradesh'), (36, 'West Bengal')], default=1)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='total_tax_amount',
            new_name='total_central_tax_amount',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='shiipping_state',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='shipping_customer',
        ),
        migrations.RemoveField(
            model_name='item',
            name='central_tax_rate',
        ),
        migrations.RemoveField(
            model_name='item',
            name='integrated_tax_rate',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='central_tax',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='integrated_tax',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='state_tax',
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_integrated_tax_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_state_tax_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.IntegerField(choices=[(1, 'Andaman & Nicobar Islands'), (2, 'Andhra Pradesh'), (3, 'Arunachal Pradesh'), (4, 'Assam'), (5, 'Bihar'), (6, 'Chandigarh'), (7, 'Chhattisgarh'), (8, 'Dadra & Nagar Haveli and Daman & Diu'), (9, 'Delhi'), (10, 'Goa'), (11, 'Gujarat'), (12, 'Haryana'), (13, 'Himachal Pradesh'), (14, 'Jammu & Kashmir'), (15, 'Jharkhand'), (16, 'Karnataka'), (17, 'Kerala'), (18, 'Ladakh'), (19, 'Lakshadweep'), (20, 'Madhya Pradesh'), (21, 'Maharashtra'), (22, 'Manipur'), (23, 'Meghalaya'), (24, 'Mizoram'), (25, 'Nagaland'), (26, 'Odisha'), (27, 'Puducherry'), (28, 'Punjab'), (29, 'Rajasthan'), (30, 'Sikkim'), (31, 'Tamil Nadu'), (32, 'Telangana'), (33, 'Tripura'), (34, 'Uttarakhand'), (35, 'Uttar Pradesh'), (36, 'West Bengal')], default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='state_tax_rate',
            field=models.IntegerField(),
        ),
    ]
