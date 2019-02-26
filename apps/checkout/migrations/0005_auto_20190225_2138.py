# Generated by Django 2.1.5 on 2019-02-25 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20190223_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='billing_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='checkout.BillingInformation'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='checkout.PaymentInformation'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='checkout.ShippingInformation'),
        ),
    ]
