# Generated by Django 3.1.7 on 2021-05-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile_public_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_groups',
            field=models.BooleanField(default=False, help_text='Show Group on Profile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_interest',
            field=models.BooleanField(default=False, help_text='Show interest on Profile'),
        ),
    ]
