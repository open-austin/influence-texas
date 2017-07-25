def assert_simple_attributes_match_data(attribute_names, instance, data):
    """Assert attributes on object instance match keys in data dict."""
    for name in attribute_names:
        value = getattr(instance, name)
        expected = data[name]
        assert value == expected, f"{value!r} == {expected!r} failed for attribute {name!r}"


class StringContaining(str):

    def __eq__(self, other):
        return self in other
