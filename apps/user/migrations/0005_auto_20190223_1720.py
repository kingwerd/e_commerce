# Generated by Django 2.1.5 on 2019-02-23 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190223_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default='', max_length=150),
        ),
    ]
