# Generated by Django 3.1.7 on 2021-06-11 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210507_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='invited',
            field=models.BooleanField(default=False),
        ),
    ]