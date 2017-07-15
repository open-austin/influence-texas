import json
import os
import os.path as pth

import pytest
from django.forms import ValidationError

from influencetx.legislators import factories
from influencetx.openstates import data, utils
from influencetx.openstates.testing import assert_legislator_fields_match_data


def test_deserialize_from_openstates_sample():
    json_data = data.get_sample_legislator_detail()

    legislator = utils.deserialize_openstates_legislator(json_data, commit=False)

    assert_legislator_fields_match_data(legislator, json_data)


def test_deserialize_with_missing_required_field_raises():
    json_data = data.get_sample_legislator_detail()
    del json_data['first_name']  # Delete required key, first_name

    with pytest.raises(ValidationError):
        legislator = utils.deserialize_openstates_legislator(json_data)


@pytest.mark.django_db
def test_update_legislator_instance():
    original = factories.LegislatorFactory()
    original_id = original.id

    json_data = data.get_sample_legislator_detail()
    legislator = utils.update_legislator_instance(original, json_data)

    assert_legislator_fields_match_data(legislator, json_data)
    assert legislator.id == original_id
