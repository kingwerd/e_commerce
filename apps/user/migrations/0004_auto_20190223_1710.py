# Generated by Django 2.1.5 on 2019-02-23 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190221_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.IntegerField(default=1),
        ),
    ]
