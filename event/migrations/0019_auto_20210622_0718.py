# Generated by Django 3.1.7 on 2021-06-22 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0018_groupinvitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitation',
            name='invited_to',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
