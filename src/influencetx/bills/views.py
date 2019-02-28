from django.views.generic import DetailView, ListView
from django.http import Http404
from influencetx.bills import models
import logging
log = logging.getLogger(__name__)


class BillListView(ListView):

    model = models.Bill
    context_object_name = 'bills'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return (
            models.Bill.objects.all()
            .prefetch_related('subjects__bills')
            .order_by('bill_id')
        )

    def get_context_data(self, *args, **kwargs):
        context = super(BillListView, self).get_context_data(*args, **kwargs)
        context['total_bills'] = models.Bill.objects.all().count()
        object = models.Bill.objects.first()
        context['session'] = object.session
        context['updated'] = object.openstates_updated_at
        return context


class BillDetailView(DetailView):

    model = models.Bill
    context_object_name = 'bill'

    def get_context_data(self, *args, **kwargs):
        context = super(BillDetailView, self).get_context_data(*args, **kwargs)
        bill = models.Bill.objects.get(openstates_bill_id=self.object.openstates_bill_id)
        context['actions'] = models.ActionDate.objects.filter(bill=self.object.id)
        if not bill:
            raise Http404()
        return context
