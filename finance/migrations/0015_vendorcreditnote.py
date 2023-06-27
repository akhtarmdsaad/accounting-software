# Generated by Django 3.1 on 2023-06-26 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0014_reciept'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorCreditNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(default='')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.item')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.vendor')),
            ],
        ),
    ]