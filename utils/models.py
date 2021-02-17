# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

User = get_user_model()

STATUS_TYPE = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('blocked', 'Blocked')
)


class ModelMixin(models.Model):
    """
    This mixins provide the default field in the models project wise
    """
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created",
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_updated",
                                   on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='active', choices=STATUS_TYPE, help_text=_('Status'))

    class Meta:
        abstract = True