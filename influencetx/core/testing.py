from contextlib import contextmanager
from unittest import mock


def assert_simple_attributes_match_data(attribute_names, instance, data):
    """Assert attributes on object instance match keys in data dict."""
    for name in attribute_names:
        value = getattr(instance, name)
        expected = data[name]
        assert value == expected, f"{value!r} == {expected!r} failed for attribute {name!r}"


class StringContaining(str):

    def __eq__(self, other):
        return self in other


def assert_mock_logger_called_once(mock_log, log_level, message=None):
    log_func = getattr(mock_log, log_level)
    if message:
        log_func.assert_called_once_with(message)
    else:
        log_func.assert_called_once()


def create_assert_log_context(log_level):
    @contextmanager
    def assert_logged(logger_import, message=None):
        with mock.patch(logger_import) as mock_log:
            yield
            assert_mock_logger_called_once(mock_log, log_level, message=message)
    return assert_logged


def assert_log_warning(logger_import, message=None):
    return create_assert_log_context('warn')(logger_import, message=None)
