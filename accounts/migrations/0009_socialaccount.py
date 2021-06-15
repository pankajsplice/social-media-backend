# Generated by Django 3.1.7 on 2021-06-15 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_invited'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=128, null=True)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('token', models.TextField(blank=True, null=True)),
                ('providers', models.CharField(blank=True, max_length=100, null=True)),
                ('is_social_login', models.BooleanField(default=False)),
                ('social_picture', models.CharField(blank=True, max_length=500, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
