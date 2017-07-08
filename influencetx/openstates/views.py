from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from . import fetch


class IndexView(View):

    def get(self, request):
        return render(request, 'openstates/index.html')


def require_api_key(f):
    """Decorator that redirects to error page if the `OPENSTATES_API_KEY` is not found."""
    def wrapped(request, *args, **kwargs):
        if not fetch.OPENSTATES_API_KEY:
            if settings.DEBUG:
                import os
                print('-'* 50)
                print(os.environ.get('OPENSTATES_API_KEY'))
                print('-'* 50)
                return redirect(reverse('openstates:api-key-required'))
            else:
                raise ImproperlyConfigured('OPENSTATES_API_KEY is not defined')
        return f(request, *args, **kwargs)
    return wrapped


class APIKeyRequiredView(View):

    def get(self, request):
        return render(request, 'openstates/api_key_required.html')


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
        context = { 'legislator': legislator }
        return render(request, 'openstates/legislator_detail.html', context=context)


class BillListView(View):

    @method_decorator(require_api_key)
    def get(self, request):
        context = {
            'bill_list': fetch.bills(),
        }
        return render(request, 'openstates/bill_list.html', context=context)


class BillDetailView(View):

    @method_decorator(require_api_key)
    def get(self, request, session=None, id=None):
        if not session or not id:
            return HttpResponseBadRequest()
        bill = fetch.bills(session=session, pk=id)
        if not bill:
            raise Http404()
        context = { 'bill': bill }
        return render(request, 'openstates/bill_detail.html', context=context)
