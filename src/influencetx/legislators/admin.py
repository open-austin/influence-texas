from django.contrib import admin

from . import models

admin.site.register(models.Legislator)
admin.site.register(models.LegislatorIdMap)
