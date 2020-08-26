from django.contrib import admin

from . import models

admin.site.register(models.Bill)
admin.site.register(models.SubjectTag)
admin.site.register(models.ActionDate)
admin.site.register(models.VoteTally)
admin.site.register(models.SingleVote)
