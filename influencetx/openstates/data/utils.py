import json
import os.path as pth


__all__ = [
    'get_sample_json',
    'get_sample_legislator_list', 'get_sample_legislator_detail',
    'get_sample_bill_list', 'get_sample_bill_detail',
]


LOCAL_DIR = pth.dirname(pth.abspath(__file__))


def get_sample_json(filename, **value_overrides):
    with open(pth.join(LOCAL_DIR, filename)) as f:
        api_data = json.load(f)
    api_data.update(**value_overrides)
    return api_data


def get_sample_legislator_list():
    """Return sample data from legislator-list endpoint."""
    return get_sample_json('sample_legislator_list.json')


def get_sample_legislator_detail(**value_overrides):
    """Return sample data from legislator-detail endpoint.

    Any additional `value_overrides` are used to update the sample data before returning.
    """
    return get_sample_json('sample_legislator_detail.json', **value_overrides)


def get_sample_bill_list():
    """Return sample data from bill-list endpoint."""
    return get_sample_json('sample_bill_list.json')


def get_sample_bill_detail(**value_overrides):
    """Return sample data from bill-detail endpoint.

    Any additional `value_overrides` are used to update the sample data before returning.
    """
    return get_sample_json('sample_bill_detail.json', **value_overrides)
