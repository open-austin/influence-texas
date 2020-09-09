from django.contrib import admin
from . import models


class JobAdmin(admin.ModelAdmin):
    list_display = ('employer', 'position', 'held_by', 'financial_disclosure')
    readonly_fields = ('legislator', )


admin.site.register(models.Job, JobAdmin)


class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('name', "view_jobs_count")

    def view_jobs_count(self, obj):
        return obj.jobs.count()
    view_jobs_count.short_description = "Jobs"


admin.site.register(models.JobType, JobTypeAdmin)


class FinancialDisclosureAdmin(admin.ModelAdmin):
    list_display = ("legislator", "year", "elected_officer", "candidate")
    readonly_fields = ('legislator', )


admin.site.register(models.FinancialDisclosure, FinancialDisclosureAdmin)


admin.site.register(models.Gift)
admin.site.register(models.Board)
admin.site.register(models.Stock)
