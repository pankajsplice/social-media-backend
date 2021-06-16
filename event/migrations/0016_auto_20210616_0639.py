# Generated by Django 3.1.7 on 2021-06-16 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0015_auto_20210614_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='RecurringEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(blank=True, help_text='Event Timing', null=True)),
                ('date', models.DateField(blank=True, help_text='Event Date', null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
        ),
    ]