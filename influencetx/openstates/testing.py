from influencetx.core.testing import assert_simple_attributes_match_data
from influencetx.core.utils import party_enum
from influencetx.openstates import utils


# "Simple" fields match one-to-one on Legislator model and Open States json API.
SIMPLE_LEGISLATOR_FIELDS = [
    'first_name', 'last_name', 'middle_name', 'suffixes', 'chamber',
    'transparencydata_id', 'votesmart_id', 'url', 'photo_url',
]


def assert_legislator_fields_match_data(legislator, data):
    """Assert fields on legislator instance match values in Open States data."""
    assert_simple_attributes_match_data(SIMPLE_LEGISLATOR_FIELDS, legislator, data)
    _assert_adapted_legislator_fields_match_data(legislator, data)


def _assert_adapted_legislator_fields_match_data(legislator, data):
    assert legislator.party == party_enum(data['party']).value
    assert legislator.district == int(data['district'])
    assert utils.format_datetime(legislator.openstates_updated_at) == data['updated_at']
    assert legislator.openstates_leg_id == data['leg_id']
