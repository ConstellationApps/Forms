from django.contrib import admin

from .models import ApiKey, Log

admin.site.register(ApiKey)
admin.site.register(Log)
