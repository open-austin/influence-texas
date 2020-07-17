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


class HeldBy(Enum):
    FILER = 'Filer'
    SPOUSE = 'Spouse'
    DEPENDENT = 'Dependent'


HELD_BY_CHOICES = [
    (HeldBy.FILER.value, HeldBy.FILER.value),
    (HeldBy.SPOUSE.value, HeldBy.SPOUSE.value),
    (HeldBy.DEPENDENT.value, HeldBy.DEPENDENT.value),
]
# class ShareNums(Enum):
#     LESS_THAN_100 = "LESS THAN 100"
#     BETWEEN_100_499 = "100 TO 499"
#     BETWEEN_500_999 = "500 TO 999"
#     BETWEEN_1000_4999 = "1,000 TO 4,999"
#     BETWEEN_5000_10000 = "LESS THAN 10K""
#     MORE_THAN_10000 = "10,000 OR MORE"

# SHARE_NUMS = [
#     (HeldBy.LESS_THAN_100.value, HeldBy.LESS_THAN_100.value),
#     (HeldBy.BETWEEN_100_499.value, HeldBy.BETWEEN_100_499.value),
#     (HeldBy.BETWEEN_500_999.value, HeldBy.BETWEEN_500_999.value),
#     (HeldBy.BETWEEN_1000_4999.value, HeldBy.BETWEEN_1000_4999.value),
#     (HeldBy.BETWEEN_5000_10000.value, HeldBy.BETWEEN_5000_10000.value),
#     (HeldBy.MORE_THAN_10000.value, HeldBy.MORE_THAN_10000.value),
# ]


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
