def assert_simple_attributes_match_data(attribute_names, instance, data):
    """Assert attributes on object instance match keys in data dict."""
    for name in attribute_names:
        assert getattr(instance, name) == data[name]
