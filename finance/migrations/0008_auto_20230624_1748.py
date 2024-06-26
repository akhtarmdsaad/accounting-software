# Generated by Django 3.1 on 2023-06-24 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='mode',
            field=models.IntegerField(choices=[(1, 'CASH'), (2, 'BANK')], default=1),
        ),
        migrations.CreateModel(
            name='SaleReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(default='')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Disapproved')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.item')),
            ],
        ),
    ]
