# Generated by Django 3.1.7 on 2021-07-08 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_userprofile_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('customer', 'Customer'), ('vendor', 'Vendor')], max_length=10, null=True),
        ),
    ]
