# Generated by Django 3.1.7 on 2021-04-02 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210223_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='enabled_msg',
            field=models.BooleanField(default=False),
        ),
    ]
