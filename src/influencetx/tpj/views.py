from django.views.generic import DetailView, ListView

from influencetx.core import constants
from . import models

class DonorListView(ListView):

    model = models.Donor
    context_object_name = 'donors'
    extra_context = {'title': 'Top Donors'}
    filters = {}

    queryset = (
        models.Donor.objects
        .prefetch_related('contributiontotalbydonor')
        .order_by('contributiontotalbydonor__cycle_total')
        .reverse()[:25]
    )

    def get_context_data(self, *args, **kwargs):
        context = super(DonorListView, self).get_context_data(*args, **kwargs)
        context.update(**self.extra_context)

        return context


class DonorDetailView(DetailView):

    model = models.Donor
    context_object_name = 'donor'


    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super(DonorDetailView, self).get_context_data(*args, **kwargs)

        contributions = models.tpj_models.Contributionsummary.objects.prefetch_related('filer').filter(donor=self.object.id).order_by('amount').reverse()[:25]
        context['top_contributions'] = contributions
        return context
