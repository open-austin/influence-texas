from influencetx.core.testing import assert_simple_attributes_match_data
from influencetx.openstates import utils


def assert_legislator_fields_match_data(legislator, api_data):
    """Assert fields on legislator instance match values in Open States data."""
    data = utils.adapt_openstates_legislator(api_data)
    fields = [
        'first_name', 'last_name', 'middle_name', 'suffixes',
        'party', 'chamber', 'district', 'url', 'photo_url',
        'openstates_updated_at', 'openstates_leg_id',
        'transparencydata_id', 'votesmart_id',
    ]
    assert_simple_attributes_match_data(fields, legislator, data)


def assert_bill_fields_match_data(bill, api_data):
    """Assert fields on legislator instance match values in Open States data."""
    data = utils.adapt_openstates_bill(api_data)
    simple_fields = ['title', 'bill_id', 'openstates_bill_id', 'openstates_updated_at']
    assert_simple_attributes_match_data(simple_fields, bill, data)

    expected_subjects = set(api_data.get('subjects', []))
    assert set(subject.label for subject in bill.subjects.all()) == expected_subjects

    for tally_model, tally_data in zip(bill.vote_results.all(), data['votes']):
        assert_vote_tally_fields_match_adapted_data(tally_model, tally_data)


def assert_vote_tally_fields_match_adapted_data(instance, data):
    """"""
    fields = [
        'chamber', 'session', 'passed', 'date',
        'yes_count', 'no_count', 'other_count', 'openstates_vote_id',
    ]
    assert_simple_attributes_match_data(fields, instance, data)
