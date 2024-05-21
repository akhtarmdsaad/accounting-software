# Generated by Django 4.2.3 on 2024-05-21 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0031_remove_transaction_amount_alter_invoice_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='invoice_files/')),
            ],
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='changed_by_user',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='date',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='file_invoice',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='invoice_no',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='total_amount',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='total_tax_amount',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='total_taxable_amount',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='valid',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='salereturn',
            name='status',
        ),
        migrations.RemoveField(
            model_name='vendorcreditnote',
            name='status',
        ),
        migrations.CreateModel(
            name='PurchaseReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(default='')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('changed_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.item')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInvoiceDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=50, verbose_name='invoice_no')),
                ('date', models.DateField(verbose_name='date')),
                ('total_taxable_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total_tax_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valid', models.BooleanField(default=False, verbose_name='valid')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('changed_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.vendor')),
            ],
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.purchaseinvoicedetails'),
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.relatedfile'),
        ),
    ]
