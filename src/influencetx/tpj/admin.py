from django.contrib import admin

from . import models

admin.site.register(models.Donor)
admin.site.register(models.Filer)
admin.site.register(models.Contribution)
admin.site.register(models.Contributionsummary)
admin.site.register(models.Contributiontotalbydonor)
