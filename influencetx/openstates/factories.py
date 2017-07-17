"""
Factory functions for creating fake data (not models) from Open States API.
"""
from faker import Factory

from influencetx.core.constants import Chamber
from influencetx.core.utils import PARTY_MAPPING


FAKE = Factory.create()


def fake_openstates_timestamp():

    """Return fake timestamp matching Open States' formatting."""
    return FAKE.iso8601().replace('T', ' ')


def random_chamber():
    return FAKE.random_element([Chamber.LOWER.value, Chamber.UPPER.value])


def random_party_name():
    return FAKE.random_element(PARTY_MAPPING.keys())


def fake_bill():
    """Fake data mimicking item in Bill Search endpoint of Open States API."""
    bill = {
        'id': FAKE.pystr(max_chars=20),
        'bill_id': FAKE.pystr(max_chars=10),
        'title': FAKE.pystr(),
        'subjects': FAKE.pystr(),
        'session': str(FAKE.pyint()),
    }
    return bill


def fake_bill_detail():
    """Fake data mimicking Bill Detail endpoint of Open States API."""
    session = str(FAKE.pyint())
    bill = {
        'id': FAKE.pystr(max_chars=20),
        'bill_id': FAKE.pystr(max_chars=10),
        'title': FAKE.pystr(),
        'subjects': [FAKE.pystr()],
        'session': session,
        'chamber': random_chamber(),
        'action_dates': {
            FAKE.pystr(): fake_openstates_timestamp(),
        },
        'updated_at': fake_openstates_timestamp(),
        'votes': [fake_vote_tally(session=session)],
    }
    return bill


def fake_vote():
    return {'leg_id': FAKE.pystr(), 'name': FAKE.name()}


def fake_vote_tally(session=None):
    session = session or str(FAKE.pyint())
    vote_tally = {
        'vote_id': FAKE.pystr(),
        'date': fake_openstates_timestamp(),
        'chamber': random_chamber(),
        'session': session,
        'passed': FAKE.boolean(),
        'yes_count': FAKE.pyint(),
        'no_count': FAKE.pyint(),
        'other_count': FAKE.pyint(),
        'yes_votes': [fake_vote()],
        'no_votes': [fake_vote()],
        'other_votes': [fake_vote()],
    }
    return vote_tally


def fake_legislator():
    """Fake data mimicking item in Legislator Search endpoint of Open States API."""
    legislator = {
        'leg_id': FAKE.pystr(),
        'full_name': FAKE.name(),
        'first_name': FAKE.first_name(),
        'last_name': FAKE.last_name(),
        'district': str(FAKE.pyint()),
        'party': random_party_name(),
        'chamber': random_chamber(),
        'updated_at': fake_openstates_timestamp(),
    }
    return legislator
