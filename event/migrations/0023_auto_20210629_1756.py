# Generated by Django 3.1.7 on 2021-06-29 17:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0022_messagesetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='member',
            field=models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
