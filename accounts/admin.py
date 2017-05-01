# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	fields=('user', 'nickname', 'gender', 'addr', 'is_email_verified', 'is_phone_verified', 'is_deleted', 'img_heading')
	readonly_fields=('user', 'is_email_verified', 'is_phone_verified')
	save_on_top=True

admin.site.register(Profile, ProfileAdmin)