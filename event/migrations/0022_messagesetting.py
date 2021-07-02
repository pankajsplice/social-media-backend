# Generated by Django 3.1.7 on 2021-06-28 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0021_auto_20210623_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.BooleanField(default=False)),
                ('report', models.TextField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('receiver', models.ForeignKey(help_text='receiver', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver_setting', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(help_text='sender', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_setting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]