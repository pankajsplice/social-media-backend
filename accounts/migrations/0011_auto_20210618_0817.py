# Generated by Django 3.1.7 on 2021-06-18 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.IntegerField(blank=True),
        ),
    ]