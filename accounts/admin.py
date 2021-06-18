# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserProfile, Otp, SocialAccount
from django.contrib.auth.admin import UserAdmin as UAdmin
from utils.download_csv import ExportCsvMixin

User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    For Export purpose only(ca_num and mobile)
    """

    model = UserProfile
    list_display = ['user', 'mobile']
    actions = ['export_as_csv']


class ProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(UAdmin, ExportCsvMixin):
    inlines = [ProfileInline]
    list_display = ["id", "username", "email", "first_name", "last_name", "last_login", "date_joined" ,'is_superuser', 'get_mobile']
    actions = ["download_csv"]

    def get_mobile(self, instance):
        return instance.profile.mobile
    get_mobile.short_description = 'mobile'


class OtpAdmin(admin.ModelAdmin):
    model = Otp
    list_display = ('email', 'mobile', 'otp', 'verify')


class SocialAccountAdmin(admin.ModelAdmin):
    model = SocialAccount
    list_display = ('email', 'mobile', 'token', 'providers', 'is_social_login', 'date_created')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(Otp, OtpAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)
