from contextlib import contextmanager
from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import reverse
from django.test import SimpleTestCase
from faker import Factory

from influencetx.openstates import factories, views
from influencetx.testing.view_utils import render_view, response_from_view


FAKE = Factory.create()


def test_index_view():
    html = render_view('openstates:index')
    assert reverse('openstates:legislator-list') in html
    assert reverse('openstates:bill-list') in html


def test_api_key_required_view():
    html = render_view('openstates:api-key-required')
    assert 'https://openstates.org/api/register/' in html


class BaseOpenStatesAPITestCase(SimpleTestCase):

    def assert_fetch_redirects(self, view_name, args=None, kwargs=None):
        """Assert view redirects to error page when api-key is missing and in debug mode."""
        response = response_from_view(view_name, args=args, kwargs=kwargs)
        self.assertRedirects(response, reverse('openstates:api-key-required'))

    def assert_fetch_raises(self, view_name, args=None, kwargs=None):
        """Assert view raises error when api-key is missing and in debug mode."""
        with self.assertRaises(ImproperlyConfigured):
            response_from_view(view_name, args=args, kwargs=kwargs)


class TestLegislatorListView(BaseOpenStatesAPITestCase):

    def test_no_api_key(self):
        with mock_fetch_with_no_api_key(debug_mode=True):
            self.assert_fetch_redirects('openstates:legislator-list')
        with mock_fetch_with_no_api_key(debug_mode=False):
            self.assert_fetch_raises('openstates:legislator-list')

    def test_data_rendering(self):
        legislator = factories.fake_legislator()
        detail_url = reverse('openstates:legislator-detail', args=(legislator['leg_id'],))

        with mock_fetch() as fetch:
            fetch.legislators.return_value = [legislator]
            html = render_view('openstates:legislator-list')

        assert detail_url in html
        for value in legislator.values():
            assert value in html


class TestLegislatorDetailView(BaseOpenStatesAPITestCase):

    def test_no_api_key(self):
        args = (FAKE.pyint(), FAKE.pystr())
        with mock_fetch_with_no_api_key(debug_mode=True):
            self.assert_fetch_redirects('openstates:bill-detail', args=args)
        with mock_fetch_with_no_api_key(debug_mode=False):
            self.assert_fetch_raises('openstates:bill-detail', args=args)

    def test_data_rendering(self):
        legislator = factories.fake_legislator()
        leg_id = legislator['leg_id']

        with mock_fetch() as fetch:
            fetch.legislators.return_value = legislator
            html = render_view('openstates:legislator-detail', args=(leg_id,))

        fetch.legislators.assert_called_once_with(leg_id)
        assert legislator['full_name'] in html
        assert legislator['district'] in html
        assert legislator['party'] in html
        assert legislator['chamber'] in html

    def test_legislator_not_found(self):
        with mock_fetch() as fetch:
            fetch.legislators.return_value = None
            with self.assertRaises(Http404):
                render_view('openstates:legislator-detail', kwargs={'leg_id': FAKE.pystr()})


class TestBillListView(BaseOpenStatesAPITestCase):

    def test_no_api_key(self):
        with mock_fetch_with_no_api_key(debug_mode=True):
            self.assert_fetch_redirects('openstates:bill-list')
        with mock_fetch_with_no_api_key(debug_mode=False):
            self.assert_fetch_raises('openstates:bill-list')

    def test_data_rendering(self):
        bill = factories.fake_bill()
        detail_url = reverse('openstates:bill-detail', args=(bill['session'], bill['bill_id']))

        with mock_fetch() as fetch:
            fetch.bills.return_value = [bill]
            html = render_view('openstates:bill-list')

        assert detail_url in html
        for key, value in bill.items():
            assert value in html



class TestBillDetailView(BaseOpenStatesAPITestCase):

    def test_no_api_key(self):
        args = (FAKE.pyint(), FAKE.pystr())
        with mock_fetch_with_no_api_key(debug_mode=True):
            self.assert_fetch_redirects('openstates:bill-detail', args=args)
        with mock_fetch_with_no_api_key(debug_mode=False):
            self.assert_fetch_raises('openstates:bill-detail', args=args)

    def test_data_rendering(self):
        bill = factories.fake_bill_detail()
        bill_id = bill['bill_id']
        session = bill['session']

        with mock_fetch() as fetch:
            fetch.bill_detail.return_value = bill
            html = render_view('openstates:bill-detail',
                                       kwargs={'session': session, 'id': bill_id})

        fetch.bill_detail.assert_called_once_with(session=session, pk=bill_id)

        assert bill_id in html
        assert bill['title'] in html
        assert bill['subjects'][0] in html
        assert str(session) in html

        action, date = list(bill['action_dates'].items())[0]
        date, timestamp = date.split()
        assert action in html
        assert date in html
        assert timestamp not in html

        vote = bill['votes'][0]
        date, timestamp = vote['date'].split()
        assert date in html
        assert timestamp not in html
        assert str(vote['yes_count']) in html
        assert str(vote['no_count']) in html
        assert vote['chamber'] in html

    def test_bill_not_found(self):
        bill_kwargs = {'session': FAKE.pyint(), 'id': FAKE.pystr()}
        with mock_fetch() as fetch:
            fetch.bill_detail.return_value = None
            with self.assertRaises(Http404):
                render_view('openstates:bill-detail', kwargs=bill_kwargs)


@contextmanager
def mock_fetch():
    with mock.patch.object(views, 'fetch') as fetch:
        yield fetch

@contextmanager
def mock_fetch_with_no_api_key(debug_mode=True):
    with use_debug_mode(debug_mode):
        with mock_fetch() as fetch:
            fetch.OPENSTATES_API_KEY = None
            yield fetch


@contextmanager
def use_debug_mode(is_debug):
    with mock.patch.object(views, 'settings') as settings:
        settings.DEBUG = is_debug
        yield
