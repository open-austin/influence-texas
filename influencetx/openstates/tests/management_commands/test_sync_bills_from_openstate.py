from collections import namedtuple
from contextlib import contextmanager
from unittest import mock

from django.test import TestCase

from influencetx.core.testing import StringContaining
from influencetx.bills.factories import BillFactory
from influencetx.openstates import factories
from influencetx.openstates.management.commands import sync_bills_from_openstate
from influencetx.openstates.services import Action, ActionInfo


class TestSyncLegislatorsFromOpenState(TestCase):

    def test_no_data(self):
        command = sync_bills_from_openstate.Command()
        with mock_dependencies(command) as mocked:
            mocked.fetch.bills.return_value = ()
            command.handle(max=3, force_update=False, session=None)

        mocked.fetch.bills.assert_called_once_with(per_page=3, search_window='session')
        mocked.stdout.write.assert_called_once_with(StringContaining('No data'))

    def test_sync_func_is_successful(self):
        command = sync_bills_from_openstate.Command()

        bill = BillFactory.build()
        bill_item = factories.fake_bill()
        bill_detail_data = factories.fake_bill_detail()
        success_info = ActionInfo.create(Action.ADDED, bill)
        with mock_dependencies(command, return_sync_info=success_info) as mocked:
            mocked.fetch.bills.return_value = [bill_item]
            mocked.fetch.bill_detail.return_value = bill_detail_data
            command.handle(max=None, force_update=False, session=None)

        # `fetch.bill_detail` should be called with official `bill_id` not openstates `id`.
        mocked.fetch.bill_detail.assert_called_once_with(bill_item['session'], bill_item['bill_id'])
        mocked.sync_func.assert_called_once_with(bill_detail_data, force_update=False)
        mocked.stdout.write.assert_any_call(StringContaining(bill.openstates_bill_id))

    def test_sync_func_is_failure(self):
        command = sync_bills_from_openstate.Command()

        failure_info = ActionInfo.fail('error message')
        with mock_dependencies(command, return_sync_info=failure_info) as mocked:
            mocked.fetch.bills.return_value = [factories.fake_bill()]
            mocked.fetch.bill_detail.return_value = factories.fake_bill_detail()
            command.handle(max=None, force_update=False, session=None)

        mocked.sync_func.assert_called_once()
        mocked.stdout.write.assert_any_call(StringContaining('error message'))

    def test_bill_detail_fails(self):
        command = sync_bills_from_openstate.Command()

        with mock_dependencies(command) as mocked:
            mocked.fetch.bills.return_value = [factories.fake_bill()]
            mocked.fetch.bill_detail.return_value = mock.Mock(status_code=404, reason='Not Found')
            command.handle(max=None, force_update=False, session=None)

        mocked.sync_func.assert_not_called()
        mocked.stdout.write.assert_any_call(StringContaining('Not Found'))


@contextmanager
def mock_dependencies(command, return_sync_info=None):
    """Context manager return context containing mocked fetch, stdout, and sync function."""
    Dependencies = namedtuple('Dependencies', 'fetch sync_func stdout')
    services_module = sync_bills_from_openstate.services
    with mock.patch.object(sync_bills_from_openstate, 'fetch') as mock_fetch:
        with mock.patch.object(services_module, 'sync_bill_data') as mock_sync_func:
            with mock.patch.object(command, 'stdout') as mock_stdout:

                mock_sync_func.return_value = return_sync_info

                yield Dependencies(fetch=mock_fetch, sync_func=mock_sync_func, stdout=mock_stdout)
