import json
import os
import os.path as pth

from django.forms import ValidationError
from django.test import TestCase

from influencetx.core.utils import party_enum
from influencetx.openstates import data, utils


class TestDeserializeLegislator(TestCase):

    def test_deserialize_from_openstates_sample(self):
        json_data = data.get_sample_legislator_detail()

        legislator = utils.deserialize_openstates_legislator(json_data)

        assert legislator.first_name == json_data['first_name']
        assert legislator.last_name == json_data['last_name']
        assert legislator.middle_name == json_data['middle_name']
        assert legislator.suffixes == json_data['suffixes']

        assert legislator.party == party_enum(json_data['party']).value
        assert legislator.district == int(json_data['district'])

        assert utils.format_datetime(legislator.openstates_updated_at) == json_data['updated_at']
        assert legislator.openstates_leg_id == json_data['leg_id']
        assert legislator.transparencydata_id == json_data['transparencydata_id']
        assert legislator.votesmart_id == json_data['votesmart_id']

        assert legislator.url == json_data['url']
        assert legislator.photo_url == json_data['photo_url']

    def test_deserialize_with_missing_required_field_raises(self):
        json_data = data.get_sample_legislator_detail()
        del json_data['first_name']  # Delete required key, first_name

        with self.assertRaises(ValidationError):
            legislator = utils.deserialize_openstates_legislator(json_data)
