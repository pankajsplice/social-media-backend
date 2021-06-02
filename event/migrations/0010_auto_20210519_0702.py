# Generated by Django 3.1.7 on 2021-05-19 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20210519_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Subscription Price', max_digits=8),
        ),
    ]