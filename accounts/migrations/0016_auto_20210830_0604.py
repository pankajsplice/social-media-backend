# Generated by Django 3.1.7 on 2021-08-30 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_userprofile_is_profile_pic_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='postal_code',
            field=models.IntegerField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
