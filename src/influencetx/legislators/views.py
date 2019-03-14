from django.views.generic import DetailView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from influencetx.core import constants
from . import models
from influencetx.tpj import models as tpj_models
from influencetx.bills import models as bill_models
import logging
log = logging.getLogger(__name__)


class LegislatorListView(ListView):

    model = models.Legislator
    context_object_name = 'legislators'
    extra_context = {'title': 'All Legislators'}
    filters = {}

    def get_queryset(self, *args, **kwargs):
        return (
            models.Legislator.objects
            .filter(**self.filters)
            .order_by('name')
        )

    def get_context_data(self, *args, **kwargs):
        context = super(LegislatorListView, self).get_context_data(*args, **kwargs)
        context.update(**self.extra_context)
        return context


class FindrepsListView(ListView):

    model = models.Legislator
    context_object_name = 'legislators'
    extra_context = { 'title': 'My Legislators' }

    def get_context_data(self, *args, **kwargs):
        context = super(FindrepsListView, self).get_context_data(*args, **kwargs)
        try:
            senate_rep = models.Legislator.objects.get(district=self.kwargs.get('pk_s', ''),chamber=constants.Chamber.UPPER.value)
        except ObjectDoesNotExist:
            senate_rep = None
        try:
            house_rep = models.Legislator.objects.get(district=self.kwargs.get('pk_h', ''),chamber=constants.Chamber.LOWER.value)
        except ObjectDoesNotExist:
            house_rep = None
        context['legislators'] = [senate_rep, house_rep]
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
        .prefetch_related('votes__vote_tally__bills__bills_sponsored')
    )

    def get_context_data(self, *args, **kwargs):
        context = super(LegislatorDetailView, self).get_context_data(*args, **kwargs)

        # TODO: Fix this once we get vote data
        # """Last vote on bill by legislator."""
        # votes = []
        # for each in self.object.votes.all():
        #     tally = each.vote_tally
        #     bill = tally.bill
        #     subjects = [subject.label for subject in bill.subjects.all()]
        #     votes.append({'value': each.value, 'date': tally.date,
        #                   'bill': tally.bill, 'subjects': subjects})
        # context['votes'] = votes

        # """Bills sponsored by legislator."""
        context['bills'] = bill_models.Bill.objects.filter(sponsors=self.object.id)

        # """Campaign contributions to legislator."""
        contributions = []
        try:
            id_map = models.LegislatorIdMap.objects.get(
                openstates_leg_id=self.object.openstates_leg_id)
            # log.warn(models.tpj_models)
            filer = tpj_models.Filer.objects.filter(id=id_map.tpj_filer_id).first()
            # log.warn(filer)
            contributions = tpj_models.Contributionsummary.objects.select_related(
                'donor').filter(filer=filer.id).order_by('-cycle_total')[:25]
        except models.LegislatorIdMap.DoesNotExist:
            log.warn(f"Filer id not found for openstates_leg_id {self.object.openstates_leg_id}" +
                     "in {models.LegislatorIdMap.objects.first}.")

        context['top_contributions'] = contributions
        return context
