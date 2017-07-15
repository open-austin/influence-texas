import json
import os
import os.path as pth

import pytest
from django.forms import ValidationError

from influencetx.core.utils import party_enum
from influencetx.openstates import data, utils


class TestDeserializeLegislator():

    def test_deserialize_from_openstates_sample(self):
        json_data = data.get_sample_legislator_detail()

        legislator = utils.deserialize_openstates_legislator(json_data, commit=False)

        simple_fields = ['first_name', 'last_name', 'middle_name', 'suffixes', 'chamber',
                         'transparencydata_id', 'votesmart_id', 'url', 'photo_url']
        assert_simple_attributes_match_data(simple_fields, legislator, json_data)

        assert legislator.party == party_enum(json_data['party']).value
        assert legislator.district == int(json_data['district'])
        assert utils.format_datetime(legislator.openstates_updated_at) == json_data['updated_at']
        assert legislator.openstates_leg_id == json_data['leg_id']

    def test_deserialize_with_missing_required_field_raises(self):
        json_data = data.get_sample_legislator_detail()
        del json_data['first_name']  # Delete required key, first_name

        with pytest.raises(ValidationError):
            legislator = utils.deserialize_openstates_legislator(json_data)


def assert_simple_attributes_match_data(attribute_names, instance, data):
    """Assert attributes on object match keys in data dict."""
    for name in attribute_names:
        assert getattr(instance, name) == data[name]
