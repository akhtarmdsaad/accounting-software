# Generated by Django 3.1 on 2023-06-20 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20230620_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryAdjustments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('reason_title', models.CharField(max_length=100)),
                ('reason_desc', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.item')),
            ],
        ),
    ]
