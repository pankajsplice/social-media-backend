# Generated by Django 3.1.7 on 2021-07-29 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0025_auto_20210701_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagesetting',
            name='gp_receiver',
            field=models.ForeignKey(blank=True, help_text='group_receiver', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gp_receiver_setting', to='event.group'),
        ),
        migrations.AlterField(
            model_name='messagesetting',
            name='receiver',
            field=models.ForeignKey(blank=True, help_text='receiver', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver_setting', to=settings.AUTH_USER_MODEL),
        ),
    ]
