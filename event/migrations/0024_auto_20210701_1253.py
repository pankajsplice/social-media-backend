# Generated by Django 3.1.7 on 2021-07-01 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0023_auto_20210629_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='paypal_plan_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='paypal_product_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
