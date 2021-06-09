# Generated by Django 3.1.7 on 2021-06-09 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_auto_20210602_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='event',
            field=models.ForeignKey(default=1, help_text='Event', on_delete=django.db.models.deletion.CASCADE, to='event.event'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='EventGroup',
        ),
    ]
