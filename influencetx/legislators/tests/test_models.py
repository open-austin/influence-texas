from influencetx.legislators.factories import LegislatorFactory


class TestLegislatorModel():

    def test_str_with_all_names(self):
        legislator = LegislatorFactory.build(first_name='First', last_name='Last',
                                             middle_name='Middle', suffixes='Jr.')
        assert str(legislator) == 'First Middle Last Jr.'

    def test_str_with_only_first_and_last(self):
        legislator = LegislatorFactory.build(first_name='First', last_name='Last',
                                             middle_name='', suffixes='')
        assert str(legislator) == 'First Last'
