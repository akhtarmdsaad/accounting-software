# Generated by Django 3.1 on 2023-06-21 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_auto_20230621_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='last_payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.payment'),
        ),
    ]
