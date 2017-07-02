import functools
import os
import urllib
from datetime import timedelta

import requests
import requests_cache
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone


API_PATH = '/api/v1'
BASE_URI = urllib.parse.urlparse('https://openstates.org')

EXPIRE_CACHE_AFTER = timedelta(hours=24)
# Cache open states data to limit API calls
requests_cache.install_cache('openstates_cache', expire_after=EXPIRE_CACHE_AFTER)

OPENSTATES_API_KEY = os.environ.get('OPENSTATES_API_KEY')
DEFAULT_HEADERS = {
    'X-API-KEY': OPENSTATES_API_KEY,
}
DEFAULT_QUERY_DICT = {
    'state': 'tx',
}
DEFAULT_TIME_RANGE = timedelta(days=180)


def legislators(pk=None):
    query = urllib.parse.urlencode(DEFAULT_QUERY_DICT)
    path = API_PATH + ('/legislators/' if pk is None else f'/legislators/{pk}/')
    uri = BASE_URI._replace(path=path, query=query)
    return fetch_json(uri.geturl(), headers=DEFAULT_HEADERS)


def bills():
    query = urllib.parse.urlencode({**DEFAULT_QUERY_DICT, })
    uri = BASE_URI._replace(path=API_PATH+'/bills/tx/')
    return fetch_json(uri.geturl(), headers=DEFAULT_HEADERS)


def fetch_json(url, headers=None):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return HttpResponse(status=response.status_code)


def _default_bill_created_date(start=None, stop=None):
    if start is None:
        start = timezone.now()

    return f'{previous_year}-{current_year}'
