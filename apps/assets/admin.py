from django.contrib import admin
from apps.assets import models

admin.site.register(models.WebApplication)
admin.site.register(models.WebRequest)