# Generated by Django 3.2.19 on 2023-07-19 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0019_customer_pancard'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='item',
            name='rate_change_system',
            field=models.IntegerField(choices=[(1, 'Fixed'), (2, 'Last Rate')], default=2),
        ),
        migrations.CreateModel(
            name='LastItemRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('changed_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.item')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.customer')),
            ],
        ),
    ]
