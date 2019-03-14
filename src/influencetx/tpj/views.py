from django.views.generic import DetailView, ListView
from . import models
import logging
log = logging.getLogger(__name__)


class DonorListView(ListView):

    model = models.Donor
    context_object_name = 'donors'
    template_name = 'tpj/donor_list.html'
    extra_context = {'title': 'Top Donors'}
    filters = {}

    queryset = (
        models.Contributiontotalbydonor.objects.all()
        .select_related('donor')
        .order_by('cycle_total')
        .reverse()[:25]
    )

    def get_context_data(self, *args, **kwargs):
        context = super(DonorListView, self).get_context_data(*args, **kwargs)
        context.update(**self.extra_context)
        # log.warn(context)
        return context


class DonorDetailView(DetailView):

    model = models.Donor
    context_object_name = 'donor'
    template_name = 'tpj/donor_detail.html'
    # queryset = (
    #     models.Donor.objects.all()
    #     .prefetch_related('donorsummarys')
    # )

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super(DonorDetailView, self).get_context_data(*args, **kwargs)
        contributions = (
            self.object
            .donorsummarys
            .prefetch_related('filer')
            .order_by('cycle_total')
            .reverse()[:25]
        )
        context['top_contributions'] = contributions
        # log.warn(context)
        return context
