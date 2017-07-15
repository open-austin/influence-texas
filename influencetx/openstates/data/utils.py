import json
import os
import os.path as pth


__all__ = ['get_sample_json', 'get_sample_legislator_detail']


LOCAL_DIR = pth.dirname(pth.abspath(__file__))


def get_sample_json(filename):
    with open(pth.join(LOCAL_DIR, filename)) as f:
        return json.load(f)


def get_sample_legislator_detail(**kwargs):
    """Return sample data from legislator-detail endpoint.

    Any additional kwargs are used to update the sample data before returning.
    """
    api_data = get_sample_json('sample_legislator_detail.json')
    api_data.update(kwargs)
    return api_data
