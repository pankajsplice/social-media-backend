# Generated by Django 3.1.7 on 2021-09-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0029_auto_20210827_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='validity',
            field=models.IntegerField(choices=[(1, 'Monthly'), (3, 'Quarterly'), (6, 'HalfYearly'), (12, 'Yearly')], help_text='Validity in months'),
        ),
    ]
