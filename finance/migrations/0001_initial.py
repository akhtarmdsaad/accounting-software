# Generated by Django 3.1 on 2023-06-19 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('brand', models.CharField(max_length=50, verbose_name='brand')),
                ('tax_preference', models.CharField(choices=[(1, 'Taxable'), (2, 'Non Taxable')], default=0, max_length=100)),
                ('inventory', models.CharField(choices=[(1, 'Yes'), (2, 'No')], default=1, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image', models.ImageField(upload_to='')),
                ('hsn_code', models.IntegerField()),
                ('unit', models.CharField(max_length=10)),
                ('unit_plural', models.CharField(max_length=10)),
                ('tax_rate_state', models.IntegerField()),
                ('current_stock', models.IntegerField()),
                ('item_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.itemgroup')),
            ],
        ),
    ]
