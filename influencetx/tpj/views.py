from django.views.generic import DetailView, ListView

from influencetx.core import constants
from . import models


class DonorListView(ListView):

    model = models.Donor
    context_object_name = 'donors'
    extra_context = {'title': 'All Donors'}
    filters = {}

    def get_queryset(self, *args, **kwargs):
        return (
            models.Donor.objects
            .filter(**self.filters)
            .order_by('total_contributions').reverse()[0:20]
        )

    def get_context_data(self, *args, **kwargs):
        context = super(DonorListView, self).get_context_data(*args, **kwargs)
        context.update(**self.extra_context)
        return context


class DonorDetailView(DetailView):

    model = models.Donor
    context_object_name = 'donor'

    def get_context_data(self, *args, **kwargs):
        context = super(DonorDetailView, self).get_context_data(*args, **kwargs)
        contributions = []
        for each in models.Contribution.objects.all().order_by('amount').reverse()[0:20]:
            amount = each.amount
            date = each.date
            contributions.append({'amount': amount, 'date': date})
        context['contributions'] = contributions
        return context
