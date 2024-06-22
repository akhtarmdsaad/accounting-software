# Generated by Django 4.2.3 on 2024-05-22 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0035_alter_purchasetransaction_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='tax_type',
            field=models.IntegerField(choices=[(1, 'CGST/SGST'), (2, 'IGST')], default=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='extra_details',
            field=models.JSONField(default='{}'),
        ),
    ]