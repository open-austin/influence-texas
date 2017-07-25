from unittest import mock

from influencetx.core import constants, utils


class TestPartyEnum():

    def test_null_input(self):
        assert utils.party_enum(None) == constants.Party.UNKNOWN

    def test_democrat_input(self):
        assert utils.party_enum('democrat') == constants.Party.DEMOCRATIC

    def test_democratic_input(self):
        assert utils.party_enum('democratic') == constants.Party.DEMOCRATIC

    def test_letter_d_input(self):
        assert utils.party_enum('D') == constants.Party.DEMOCRATIC

    def test_mixed_case_democrat_input(self):
        assert utils.party_enum('DeMocRatiC') == constants.Party.DEMOCRATIC

    def test_independent_input(self):
        assert utils.party_enum('independent') == constants.Party.INDEPENDENT

    def test_letter_i_input(self):
        assert utils.party_enum('I') == constants.Party.INDEPENDENT

    def test_mixed_case_independent_input(self):
        assert utils.party_enum('InDePenDenT') == constants.Party.INDEPENDENT

    def test_republican_input(self):
        assert utils.party_enum('republican') == constants.Party.REPUBLICAN

    def test_letter_r_input(self):
        assert utils.party_enum('R') == constants.Party.REPUBLICAN

    def test_mixed_case_republican_input(self):
        assert utils.party_enum('RePubLiCan') == constants.Party.REPUBLICAN

    def test_non_party_input(self):
        with mock.patch.object(utils, 'log') as log:
            assert utils.party_enum('not a real party') is None
        log.warn.assert_called_once_with("Could not determine party from 'not a real party'")
