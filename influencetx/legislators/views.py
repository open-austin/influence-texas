from django.views.generic import DetailView, ListView

from influencetx.core import constants
from . import models


class LegislatorListView(ListView):

    model = models.Legislator
    context_object_name = 'legislators'
    extra_context = {'title': 'All Legislators'}
    filters = {}

    def get_queryset(self, *args, **kwargs):
        return (
            models.Legislator.objects
            .filter(**self.filters)
            .order_by('first_name', 'last_name')
        )

    def get_context_data(self, *args, **kwargs):
        context = super(LegislatorListView, self).get_context_data(*args, **kwargs)
        context.update(**self.extra_context)
        return context


class SenatorListView(LegislatorListView):

    extra_context = {'title': 'Senators'}
    filters = {'chamber': constants.Chamber.UPPER.value}


class RepresentativeListView(LegislatorListView):

    extra_context = {'title': 'Representatives'}
    filters = {'chamber': constants.Chamber.LOWER.value}


class LegislatorDetailView(DetailView):

    model = models.Legislator
    context_object_name = 'legislator'
    queryset = (
        models.Legislator.objects.all()
        .prefetch_related('votes__vote_tally__bill__subjects')
    )

    def get_context_data(self, *args, **kwargs):
        context = super(LegislatorDetailView, self).get_context_data(*args, **kwargs)

        votes = []
        for each in self.object.votes.all():
            tally = each.vote_tally
            bill = tally.bill
            subjects = [subject.label for subject in bill.subjects.all()]
            votes.append({'value': each.value, 'date': tally.date,
                          'bill': tally.bill, 'subjects': subjects})
        context['votes'] = votes
        return context
