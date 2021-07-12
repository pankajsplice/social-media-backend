# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _

from django.contrib.auth import get_user_model
from django.db import models

from utils.models import ModelMixin

User = get_user_model()

USER_LANGUAGE = (
        ('EN', 'ENGLISH'),
        ('HI', 'हिंदी '),
    )

STAFF_TYPE = (
        ('1', _('Company Admin')),
        ('2', _('Organizer')),
        ('3', _('Participant')),
    )

GENDER_TYPE = (
        ('male','Male'),
        ('female','Female'),
        ('other','Other'),
    )

ROLE_TYPE = (
        ('customer', _('Customer')),
        ('vendor', _('Vendor'))
    )


class UserProfile(models.Model):
    """
    User Profile model store the basic user information
    """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    gender = models.CharField(max_length=20,choices=GENDER_TYPE,null=True,blank=True)
    type = models.CharField(max_length=30, choices=STAFF_TYPE, blank=True, null=True)
    mobile = models.CharField(max_length=15, db_index=True)
    profile_pic = models.ImageField(blank=True, null=True, help_text=_('Upload your profile pic'))
    enabled_msg = models.BooleanField(default=False)
    public_profile = models.BooleanField(default=False)
    invited = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_groups = models.BooleanField(default=False, help_text=_('Show Group on Profile'))
    profile_interest = models.BooleanField(default=False, help_text=_('Show interest on Profile'))
    dob = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_TYPE, blank=True, null=True)


class SocialAccount(models.Model):
    email = models.CharField(max_length=128, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    providers = models.CharField(max_length=100, blank=True, null=True)
    is_social_login = models.BooleanField(default=False)
    social_picture = models.CharField(max_length=500, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token


class Otp(models.Model):
    email = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    otp = models.IntegerField(blank=True)
    verify = models.BooleanField(default=False)
