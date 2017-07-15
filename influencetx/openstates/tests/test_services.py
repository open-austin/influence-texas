from datetime import timedelta
from unittest import mock

from django.test import TestCase

from influencetx.legislators import factories
from influencetx.openstates import data, services, utils
from influencetx.openstates.testing import assert_legislator_fields_match_data


ONE_DAY = timedelta(days=1)


def test_sync_new_legislator_data():
    api_data = data.get_sample_legislator_detail()
    info = services.sync_new_legislator_data(api_data, commit=False)

    assert info.action == services.Action.ADDED
    assert_legislator_fields_match_data(info.instance, api_data)


def test_sync_new_legislator_with_data_with_missing_keys_fails():
    bad_data_input = {}
    info = services.sync_new_legislator_data(bad_data_input, commit=False)
    assert info.action == services.Action.FAILED
    assert 'missing key' in info.error


def test_sync_new_legislator_without_leg_id_fails():
    data_with_invalid_id = data.get_sample_legislator_detail()
    data_with_invalid_id['leg_id'] = ''  # 'leg_id' is a required field.
    info = services.sync_new_legislator_data(data_with_invalid_id, commit=False)

    assert info.action == services.Action.FAILED
    assert 'openstates_leg_id' in info.error


def test_sync_existing_legislator_data_updates_from_recently_updated_data():
    instance = factories.LegislatorFactory.build()
    original_id = instance.id
    updated_at = utils.format_datetime(instance.openstates_updated_at + ONE_DAY)
    api_data = data.get_sample_legislator_detail(updated_at=updated_at)

    info = services.sync_existing_legislator_data(instance, api_data, commit=False)

    assert info.action == services.Action.UPDATED
    assert_legislator_fields_match_data(info.instance, api_data)
    assert info.instance.id == original_id


def test_sync_existing_legislator_data_skips_old_data():
    instance = factories.LegislatorFactory.build()
    original_id = instance.id
    updated_at = utils.format_datetime(instance.openstates_updated_at - ONE_DAY)
    api_data = data.get_sample_legislator_detail(updated_at=updated_at)

    info = services.sync_existing_legislator_data(instance, api_data, commit=False)

    assert info.action == services.Action.SKIPPED
    assert info.instance.id == original_id


class TestSyncLegislatorData(TestCase):

    @mock.patch.object(services, 'sync_existing_legislator_data')
    def test_sync_legislator_data_for_existing_data(self, mock_sync_existing):
        instance = factories.LegislatorFactory.create()
        data = {'leg_id': instance.openstates_leg_id}
        info = services.sync_legislator_data(data)
        mock_sync_existing.assert_called_once_with(instance, data, commit=True)

    @mock.patch.object(services, 'sync_new_legislator_data')
    def test_sync_legislator_data_for_new_data(self, mock_sync_new):
        data = {'leg_id': 'TX00001'}
        info = services.sync_legislator_data(data)
        mock_sync_new.assert_called_once_with(data, commit=True)
