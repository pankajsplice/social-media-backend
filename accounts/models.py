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
        ('2', _('Branch Admin')),
        ('3', _('Filed Executive')),
    )


class UserProfile(models.Model):
    """
    User Profile model store the basic user information
    """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=STAFF_TYPE, blank=True, null=True)
    mobile = models.CharField(max_length=15, db_index=True)
    profile_pic = models.ImageField(blank=True, null=True, help_text=_('Upload your profile pic'))

