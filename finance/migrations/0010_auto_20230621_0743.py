# Generated by Django 3.1 on 2023-06-21 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0009_auto_20230620_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.IntegerField(verbose_name='amount')),
            ],
        ),
        migrations.AddField(
            model_name='inventoryadjustments',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='inventoryadjustments',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email')),
                ('phone', models.CharField(max_length=50, verbose_name='phone')),
                ('address', models.TextField()),
                ('gstin', models.CharField(max_length=15, verbose_name='gstin')),
                ('current_balance', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.payment')),
            ],
        ),
    ]
