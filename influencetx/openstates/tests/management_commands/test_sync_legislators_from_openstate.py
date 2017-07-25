from collections import namedtuple
from contextlib import contextmanager
from unittest import mock

from django.core.management.base import BaseCommand, CommandError
from django.test import TestCase

from influencetx.legislators.factories import LegislatorFactory
from influencetx.openstates.management.commands import sync_legislators_from_openstate
from influencetx.openstates.services import Action, ActionInfo


FAKE_LEGISLATOR_DATA = {'leg_id': 'TX00001'}


class StringContaining(str):

    def __eq__(self, other):
        return self in other


class TestSyncLegislatorsFromOpenState(TestCase):

    def test_no_data(self):
        command = sync_legislators_from_openstate.Command()
        with mock_dependencies(command, return_legislators=()) as mocked:
            command.handle(max=None, leg_ids=None)

        mocked.fetch.legislators.assert_called_once_with()
        mocked.stdout.write.assert_called_once_with(StringContaining('No data'))

    def test_sync_func_is_successful(self):
        command = sync_legislators_from_openstate.Command()

        legislator = LegislatorFactory.build()
        success_info = ActionInfo.create(Action.ADDED, legislator)
        with mock_dependencies(command, return_sync_info=success_info) as mocked:
            command.handle(max=None, leg_ids=None)

        mocked.sync_func.assert_called_once()
        mocked.stdout.write.assert_any_call(StringContaining(legislator.first_name))
        mocked.stdout.write.assert_any_call(StringContaining(legislator.last_name))
        mocked.stdout.write.assert_any_call(StringContaining(legislator.openstates_leg_id))

    def test_sync_func_is_failure(self):
        command = sync_legislators_from_openstate.Command()
        legislator = {'leg_id': 'TX00001'}

        failure_info = ActionInfo.fail('error message')
        with mock_dependencies(command, return_sync_info=failure_info) as mocked:
            command.handle(max=None, leg_ids=None)

        mocked.sync_func.assert_called_once()
        mocked.stdout.write.assert_any_call(StringContaining('error message'))


@contextmanager
def mock_dependencies(command, return_legislators=None, return_sync_info=None):
    """Context manager return context containing mocked fetch, stdout, and sync function."""
    if return_legislators is None:
        return_legislators = [FAKE_LEGISLATOR_DATA]

    Dependencies = namedtuple('Dependencies', 'fetch sync_func stdout')
    services_module = sync_legislators_from_openstate.services
    with mock.patch.object(sync_legislators_from_openstate, 'fetch') as mock_fetch:
        with mock.patch.object(services_module, 'sync_legislator_data') as mock_sync_func:
            with mock.patch.object(command, 'stdout') as mock_stdout:

                mock_fetch.legislators.return_value = return_legislators
                mock_sync_func.return_value = return_sync_info

                yield Dependencies(fetch=mock_fetch, sync_func=mock_sync_func, stdout=mock_stdout)
