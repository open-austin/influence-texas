from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View

from . import fetch


class IndexView(TemplateView):
    template_name = 'openstates/index.html'


def require_api_key(f):
    """Decorator that redirects to error page if the `OPENSTATES_API_KEY` is not found."""
    def wrapped(request, *args, **kwargs):
        if not fetch.OPENSTATES_API_KEY:
            if settings.DEBUG:
                return redirect(reverse('openstates:api-key-required'))
            else:
                raise ImproperlyConfigured('OPENSTATES_API_KEY is not defined')
        return f(request, *args, **kwargs)
    return wrapped


class APIKeyRequiredView(TemplateView):
    template_name = 'openstates/api_key_required.html'


class LegislatorListView(View):

    @method_decorator(require_api_key)
    def get(self, request):
        context = {
            'legislators': fetch.legislators(),
        }
        return render(request, 'openstates/legislator_list.html', context=context)


class LegislatorDetailView(View):

    @method_decorator(require_api_key)
    def get(self, request, leg_id=None):
        legislator = fetch.legislators(leg_id)
        if not legislator:
            raise Http404()
        context = {'legislator': legislator}
        return render(request, 'openstates/legislator_detail.html', context=context)


class BillListView(View):

    @method_decorator(require_api_key)
    def get(self, request):
        bills = fetch.bills()
        context = {'bill_rows': [row_from_bill_item(b) for b in bills]}
        return render(request, 'openstates/bill_list.html', context=context)


def row_from_bill_item(bill):
    """Return row for bill-list page.

    This function is tightly coupled with the bill_list template and data-tables render function.
    """
    detail_url = reverse('openstates:bill-detail', args=(bill['session'], bill['bill_id']))
    return [bill['bill_id'], bill['title'], bill['subjects'], detail_url]


class BillDetailView(View):

    @method_decorator(require_api_key)
    def get(self, request, session=None, id=None):
        bill = fetch.bill_detail(session=session, pk=id)
        if not bill:
            raise Http404()
        context = {'bill': bill}
        return render(request, 'openstates/bill_detail.html', context=context)
