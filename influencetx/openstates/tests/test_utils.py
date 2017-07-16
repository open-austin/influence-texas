from unittest import mock

import pytest
from django.forms import ValidationError
from django.test import TestCase

from influencetx.bills.models import Bill, VoteTally
from influencetx.legislators.factories import LegislatorFactory
from influencetx.openstates import data, factories, testing, utils


class TestLegislatorDeserialization(object):

    def test_deserialize_from_openstates_sample(self):
        api_data = data.get_sample_legislator_detail()
        legislator = utils.deserialize_openstates_legislator(api_data, commit=False)
        testing.assert_legislator_fields_match_data(legislator, api_data)

    def test_deserialize_with_missing_required_field_raises(self):
        api_data = data.get_sample_legislator_detail()
        del api_data['first_name']  # Delete required key, first_name

        with pytest.raises(ValidationError):
            legislator = utils.deserialize_openstates_legislator(api_data)

    @pytest.mark.django_db
    def test_update_legislator_instance(self):
        original = LegislatorFactory()
        original_id = original.id

        api_data = data.get_sample_legislator_detail()
        legislator = utils.update_legislator_instance(original, api_data)

        testing.assert_legislator_fields_match_data(legislator, api_data)
        assert legislator.id == original_id


class TestBillDeserialization(TestCase):
    """Test deserialization of data from Open States API to Bill model.

    Note that all tests touch database because bill deserialization is wrapped in a transaction.
    """

    def test_deserialize_from_openstates_sample(self):
        self.assert_data_adds_single_row(data.get_sample_bill_detail())

    def test_deserialize_fake_bill_detail(self):
        self.assert_data_adds_single_row(factories.fake_bill_detail())

    def test_deserialize_same_bill_id_twice_adds_single_row(self):
        """Assert that identitical Open States bill id used to detect and prevent duplicates."""
        api_data = factories.fake_bill_detail()

        with mock.patch.object(utils, 'LOG') as mock_log:
            utils.deserialize_openstates_bill(api_data)
            bill = utils.deserialize_openstates_bill(api_data)

        assert Bill.objects.all().count() == 1

    def test_deserialize_same_vote_id_twice_adds_single_row(self):
        """Assert that identitical Open States vote id used to detect and prevent duplicates."""
        api_data = factories.fake_bill_detail()

        with mock.patch.object(utils, 'LOG') as mock_log:
            utils.deserialize_openstates_bill(api_data)

        assert VoteTally.objects.all().count() == 1

        bill = Bill.objects.all().first()

        # Deserializing vote data from fake-bill should not add the same vote tally again.
        with mock.patch.object(utils, 'LOG') as mock_log:
            vote_data = api_data['votes'][0]
            vote_data['bill'] = bill.id
            utils.adapt_openstates_vote_tally(vote_data)  # modifies data in-place.
            utils.deserialize_vote_tally(vote_data)

        assert VoteTally.objects.all().count() == 1

    def assert_data_adds_single_row(self, api_data):
        assert not Bill.objects.all().exists()

        with mock.patch.object(utils, 'LOG') as mock_log:
            bill = utils.deserialize_openstates_bill(api_data)

        testing.assert_bill_fields_match_data(bill, api_data)
        assert Bill.objects.all().count() == 1
