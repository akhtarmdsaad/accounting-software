# Generated by Django 4.2.3 on 2024-05-21 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0034_alter_purchasetransaction_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasetransaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]