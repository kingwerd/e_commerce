# Generated by Django 2.1.5 on 2019-02-23 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20190222_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippinginformation',
            name='email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='shippinginformation',
            name='first_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='shippinginformation',
            name='last_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='shippinginformation',
            name='phone',
            field=models.CharField(default='', max_length=10),
        ),
    ]
