from django.contrib import admin

from . import models

admin.site.register(models.Bill)
admin.site.register(models.SubjectTag)
# admin.site.register(models.ActionDates)
admin.site.register(models.VoteTally)
admin.site.register(models.SingleVote)
