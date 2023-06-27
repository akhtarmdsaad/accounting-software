# Generated by Django 3.1 on 2023-06-25 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0013_purchaseinvoice_valid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reciept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('description', models.TextField(default='')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('mode', models.IntegerField(choices=[(1, 'CASH'), (2, 'BANK')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.vendor')),
            ],
        ),
    ]
