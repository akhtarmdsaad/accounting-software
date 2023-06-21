# Generated by Django 3.1 on 2023-06-20 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20230619_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemgroup',
            name='inventory',
            field=models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='itemgroup',
            name='tax_preference',
            field=models.IntegerField(choices=[(1, 'Taxable'), (2, 'Non Taxable')], default=1, max_length=100),
        ),
    ]