from django.views.generic import DetailView, ListView

from influencetx.core import constants
from . import models

class DonorListView(ListView):

    model = models.Donor
    context_object_name = 'donors'
    extra_context = {'title': 'Top Donors'}
    filters = {}

    def get_queryset(self, *args, **kwargs):
        return (
            models.Donor.objects
            .order_by('contributiontotalbydonor__cycle_total')
            .reverse()[:25]
        )

    def get_context_data(self, *args, **kwargs):
        context = super(DonorListView, self).get_context_data(*args, **kwargs)
        context.update(**self.extra_context)

        context['cycle_total'] = models.Donor.cycle_total
        return context


class DonorDetailView(DetailView):

    model = models.Donor
    context_object_name = 'donor'

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super(DonorDetailView, self).get_context_data(*args, **kwargs)
        # Add in a QuerySet of all the contributions

        context['contributions'] = models.Donor.contributions
        return context
