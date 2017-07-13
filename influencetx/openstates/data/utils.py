import functools
import json
import os
import os.path as pth


__all__ = ['get_sample_json', 'get_sample_legislator_detail']


LOCAL_DIR = pth.dirname(pth.abspath(__file__))


def get_sample_json(filename):
    with open(pth.join(LOCAL_DIR, filename)) as f:
        return json.load(f)


get_sample_legislator_detail = functools.partial(get_sample_json, 'sample_legislator_detail.json')
