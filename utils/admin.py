# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Register your models here.
EXCLUDE_FOR_API = ('date_created', 'updated_by', 'date_updated', 'created_by')


class CustomModelAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name not in EXCLUDE_FOR_API]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)
