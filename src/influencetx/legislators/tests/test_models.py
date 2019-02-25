from influencetx.core import constants
from influencetx.legislators.factories import LegislatorFactory


class TestLegislatorModel():

    def test_str_with_all_names(self):
        legislator = LegislatorFactory.build(first_name='First', last_name='Last',
                                             name='Full_name')
        assert str(legislator) == 'First Middle Last Jr.'

    def test_str_with_only_first_and_last(self):
        legislator = LegislatorFactory.build(first_name='First', last_name='Last',
                                             name='')
        assert str(legislator) == 'First Last'

    def test_party_label(self):
        legislator = LegislatorFactory.build(party='D')
        assert legislator.party_label == constants.PARTY_LABELS[constants.Party.DEMOCRATIC]

    def test_chamber_label(self):
        legislator = LegislatorFactory.build(chamber='upper')
        assert legislator.chamber_label == constants.CHAMBER_LABELS[constants.Chamber.UPPER]
