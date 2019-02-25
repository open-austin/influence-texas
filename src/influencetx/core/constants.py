from enum import Enum


class Chamber(Enum):
    LOWER = 'House'
    UPPER = 'Senate'


CHAMBER_CHOICES = [
    (Chamber.LOWER.value, Chamber.LOWER.value),
    (Chamber.UPPER.value, Chamber.UPPER.value),
]


CHAMBER_LABELS = {
    Chamber.LOWER: 'Representative',
    Chamber.UPPER: 'Senator',
}


class Party(Enum):
    DEMOCRATIC = 'D'
    INDEPENDENT = 'I'
    REPUBLICAN = 'R'
    UNKNOWN = 'U'


PARTY_CHOICES = [
    (Party.DEMOCRATIC.value, 'Democratic'),
    (Party.INDEPENDENT.value, 'Independent'),
    (Party.REPUBLICAN.value, 'Republican'),
    (Party.UNKNOWN.value, 'Unknown'),
]

PARTY_LABELS = {
    Party.DEMOCRATIC: 'Democrat',
    Party.INDEPENDENT: 'Independent',
    Party.REPUBLICAN: 'Republican',
    Party.UNKNOWN: 'Unknown',
}


class Vote(Enum):
    YAY = 'Y'
    NAY = 'N'
    OTHER = 'O'


VOTE_CHOICES = [
    (Vote.YAY, 'Yay'),
    (Vote.NAY, 'Nay'),
    (Vote.OTHER, 'Other'),
]
