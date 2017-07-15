import logging

from . import constants


log = logging.getLogger(__name__)


# Party labels mapped to enum.
# Only use lowercase values as keys, since will normalize values.
# FIXME: This should be moved into a table.
PARTY_MAPPING = {
    'democratic': constants.Party.DEMOCRATIC,
    'democrat': constants.Party.DEMOCRATIC,
    'd': constants.Party.DEMOCRATIC,
    'independent': constants.Party.INDEPENDENT,
    'i': constants.Party.INDEPENDENT,
    'republican': constants.Party.REPUBLICAN,
    'r': constants.Party.REPUBLICAN,
}


def party_enum(string):
    if string is None:
        return constants.Party.UNKNOWN
    party = PARTY_MAPPING.get(string.lower())
    if party is None:
        log.warn(f"Could not determine party from {string!r}")
    return party
