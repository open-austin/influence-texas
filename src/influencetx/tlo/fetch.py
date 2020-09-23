# import json
import os
import logging
import lxml.html
import re
import requests
from django.conf import settings
from time import sleep
LOG = logging.getLogger(__name__)


def lxmlize(url, session=requests.Session()):
    """Parses document into an LXML object and makes links absolute.
    Args:
        url (str): URL of the document to parse.
    Returns:
        Element: Document node representing the page.
    """
    try:
        response = session.get(url, timeout=10)
    except requests.exceptions.SSLError:
        print('`lxmlize()` failed due to SSL error, trying '
                     'an unverified `requests.get()`')
        response = session.get(url, verify=False, timeout=10)
    except requests.exceptions.ConnectionError:
        print('Request limit exceeded. Waiting 10 seconds.')
        response = session.get(url, timeout=10)
    page = lxml.html.fromstring(response.text)
    page.make_links_absolute(url)
    response.close()
    return page


def get_legislator_ids(session, chamber):
    """
    Return a list of tlo legislator id & names
    """
    print(f"Getting {chamber} legislator ids for session {session}")
    chamber_map = {
        'Senate': 'S',
        'House': 'H',
    }
    url = f"https://capitol.texas.gov/Members/Members.aspx?Chamber={chamber_map[chamber]}"
    page = lxmlize(url)
    # table id="dataListMembers"
    hrefs = page.xpath('//table[@id="dataListMembers"]//@href')
    #LOG.warn(hrefs)
    id_map = []
    for ref in hrefs:
        m = re.search(r'(?<=Code=)[A-Z0-9]+$', ref)
        id = m.group(0)
        #LOG.warn(f'Found ID {id} in {chamber}')
        name = page.xpath(f'//table[@id="dataListMembers"]//a[contains(@href, "{id}")]/text()')[0].strip()
        #LOG.info(f'Found name {name} for {id} in {chamber}')
        data = {'id': f'{id}', 'name': f'{name}', 'url': f'{ref}'}
        id_map.append(data)
    return {f'{session}': {f'{chamber}': list(id_map)}}
