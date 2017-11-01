import os
import urllib
from datetime import timedelta

import requests
import requests_cache


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
DEFAULT_BILL_COUNT = 100000  # Use large default bill count to get all bills.


def legislators(pk=None):
    query = urllib.parse.urlencode(DEFAULT_QUERY_DICT)
    path = f'{API_PATH}/legislators/' if pk is None else f'{API_PATH}/legislators/{pk}/'
    uri = BASE_URI._replace(path=path, query=query)
    return fetch_json(uri.geturl(), headers=DEFAULT_HEADERS)


def bills(page=1, per_page=DEFAULT_BILL_COUNT, search_window='session'):
    custom_query = {'search_window': search_window, 'page': page, 'per_page': per_page}
    query = urllib.parse.urlencode({**DEFAULT_QUERY_DICT, **custom_query})
    uri = BASE_URI._replace(path=f'{API_PATH}/bills/', query=query)
    return fetch_json(uri.geturl(), headers=DEFAULT_HEADERS)


def bill_detail(session=None, pk=None):
    uri = BASE_URI._replace(path=f'{API_PATH}/bills/tx/{session}/{pk}/')
    return fetch_json(uri.geturl(), headers=DEFAULT_HEADERS)


def fetch_json(url, headers=None):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return response
