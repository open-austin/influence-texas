"""
Factory functions for creating fake data (not models) from Open States API.
"""
from faker import Factory

from influencetx.core.constants import Chamber


FAKE = Factory.create()


def fake_openstates_timestamp():
    """Return fake timestamp matching Open States' formatting."""
    return FAKE.iso8601().replace('T', ' ')


def random_chamber():
    return FAKE.random_element([Chamber.LOWER.value, Chamber.UPPER.value])


def fake_bill():
    """Fake data mimicking item in Bill Search endpoint of Open States API."""
    bill = {
        'bill_id': FAKE.pystr(),
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
        'yes_votes': [],
        'no_votes': [],
        'other_votes': [],
    }
    return vote_tally


def fake_legislator():
    """Fake data mimicking item in Legislator Search endpoint of Open States API."""
    legislator = {
        'leg_id': FAKE.pystr(),
        'full_name': FAKE.name(),
        'district': FAKE.pystr(),
        'party': FAKE.pystr(),
        'chamber': FAKE.pystr(),
    }
    return legislator
