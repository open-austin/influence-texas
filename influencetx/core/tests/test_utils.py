from contextlib import contextmanager
from unittest import mock

import pytest

from influencetx.core import constants, testing, utils


class TestChamberEnum():

    def test_null_input(self):
        with pytest.raises(ValueError):
            utils.chamber_enum(None)

    def test_invalid_input(self):
        with assert_log_warning():
            assert utils.chamber_enum('not valid') is None

    def test_lower_chamber(self):
        assert utils.chamber_enum('lower') == constants.Chamber.LOWER

    def test_upper_chamber(self):
        assert utils.chamber_enum('upper') == constants.Chamber.UPPER

    def test_mixed_case_lower_chamber(self):
        assert utils.chamber_enum('LoWeR') == constants.Chamber.LOWER


class TestChamberLabel():

    def test_null_input(self):
        with pytest.raises(ValueError):
            utils.chamber_label(None)

    def test_invalid_input(self):
        with assert_log_warning():
            assert utils.chamber_label('not valid') == ''

    def test_lower_chamber_label(self):
        utils.chamber_label('lower') == constants.CHAMBER_LABELS[constants.Chamber.LOWER]

    def test_higher_chamber_label(self):
        utils.chamber_label('upper') == constants.CHAMBER_LABELS[constants.Chamber.UPPER]


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


class TestPartyLabel():

    def test_null_input(self):
        utils.party_label(None) == constants.PARTY_LABELS[constants.Party.UNKNOWN]

    def test_invalid_input(self):
        with assert_log_warning():
            assert utils.party_label('not valid') == ''

    def test_democrat_label(self):
        utils.party_label('democrat') == constants.PARTY_LABELS[constants.Party.DEMOCRATIC]

    def test_independent_label(self):
        utils.party_label('independent') == constants.PARTY_LABELS[constants.Party.INDEPENDENT]

    def test_republican_label(self):
        utils.party_label('republican') == constants.PARTY_LABELS[constants.Party.REPUBLICAN]


class TestHandleError():

    def setup(self):
        self.mock_handler = mock.Mock()
        self.error = ValueError()

    def test_defaults(self):
        @utils.handle_error(ValueError, self.mock_handler)
        def function_that_raises_value_error():
            raise self.error

        with assert_handle_error_logs():
            function_that_raises_value_error()
        self.mock_handler.assert_called_once_with(self.error)

    def test_log_warning(self):
        @utils.handle_error(ValueError, self.mock_handler, log_level='warn')
        def function_that_raises_value_error():
            raise self.error

        with assert_handle_error_logs(log_level='warn'):
            function_that_raises_value_error()

    def test_not_logged(self):
        @utils.handle_error(ValueError, self.mock_handler, log_level=None)
        def function_that_raises_value_error():
            raise self.error

        with mock_handle_error_logging() as mock_logging:
            function_that_raises_value_error()
            mock_logging.getLogger.assert_not_called()


def assert_log_warning(message=None):
    return testing.assert_log_warning('influencetx.core.utils.log', message=message)


def mock_handle_error_logging():
    return mock.patch('influencetx.core.utils.logging')


@contextmanager
def mock_handle_error_logger():
    with mock_handle_error_logging() as mock_logging:
        mock_log = mock.Mock()
        mock_logging.getLogger.return_value = mock_log
        yield mock_log


@contextmanager
def assert_handle_error_logs(log_level='info', message=None):
    with mock_handle_error_logger() as mock_log:
        yield
        testing.assert_mock_logger_called_once(mock_log, log_level, message=message)
