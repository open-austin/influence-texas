from contextlib import contextmanager
from unittest import mock
from urllib.parse import urlparse, parse_qs

from influencetx.openstates import fetch


def test_fetch_legislator_list():
    with mock_get_request() as mock_get:
        fetch.legislators()

    url, headers = url_and_headers_from_mock_get_request(mock_get)
    assert_valid_openstates_url_and_headers(url, headers)
    assert url.path == '/api/v1/legislators/'
    assert url.query == 'state=tx'


def test_fetch_bill_list():
    with mock_get_request() as mock_get:
        fetch.bills()

    url, headers = url_and_headers_from_mock_get_request(mock_get)
    assert_valid_openstates_url_and_headers(url, headers)
    assert url.path == '/api/v1/bills/'
    query = parse_qs(url.query)
    assert query['state'] == ['tx']
    assert query['search_window'] == ['session']
    assert query['page'] == ['1']
    assert query['per_page'] == [str(fetch.DEFAULT_BILL_COUNT)]


def test_fetch_bill_detail():
    session = 85
    pk = 'HB%20512'
    with mock_get_request() as mock_get:
        fetch.bill_detail(session=session, pk=pk)

    url, headers = url_and_headers_from_mock_get_request(mock_get)
    assert_valid_openstates_url_and_headers(url, headers)
    assert url.path == f'/api/v1/bills/tx/{session}/{pk}/'


def test_fetch_json_failure():
    with mock_get_request(response_code=404) as mock_get:
        fetch.fetch_json('bogus-url')
    mock_get.assert_called_once_with('bogus-url', headers=None)


def assert_valid_openstates_url_and_headers(url, headers):
    assert url.netloc == 'openstates.org'
    assert 'X-API-KEY' in headers


def url_and_headers_from_mock_get_request(mock_get):
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert len(args) == 1
    assert len(kwargs) == 1
    return urlparse(args[0]), kwargs['headers']


@contextmanager
def mock_get_request(response_code=200):
    with mock.patch.object(fetch, 'requests') as requests:
        requests.get.return_value = mock.Mock(status_code=response_code)
        yield requests.get
