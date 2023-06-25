# Generated by Django 3.1 on 2023-06-24 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_payment_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='mode',
            field=models.IntegerField(choices=[(1, 'CASH'), (2, 'BANK')], default=2),
        ),
    ]
