from django.views.generic import TemplateView, DetailView, ListView
from django.http import Http404
from django.shortcuts import redirect, render, reverse
from influencetx.bills import models

import logging
log = logging.getLogger(__name__)

class BillListView(ListView):

    model = models.Bill
    context_object_name = 'bills'

    def get_queryset(self, *args, **kwargs):
        return (
            models.Bill.objects.all()
            .prefetch_related('subjects__bills')
            .order_by('bill_id')
        )

    def get_context_data(self, *args, **kwargs):
        context = super(BillListView, self).get_context_data(*args, **kwargs)
        context['total_bills'] = models.Bill.objects.all().count()
        return context


class BillDetailView(DetailView):

    model = models.Bill
    context_object_name = 'bill'

    def get_context_data(self, *args, **kwargs):
        context = super(BillDetailView, self).get_context_data(*args, **kwargs)
        bill = models.Bill.objects.get(openstates_bill_id=self.object.openstates_bill_id)
        if not bill:
            raise Http404()
        return context
