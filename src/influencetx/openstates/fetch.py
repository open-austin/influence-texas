from datetime import timedelta
import os
import logging
import requests
import requests_cache
LOG = logging.getLogger(__name__)
EXPIRE_CACHE_AFTER = timedelta(hours=24)
# Cache open states data to limit API calls
requests_cache.install_cache('openstates_cache', expire_after=EXPIRE_CACHE_AFTER)
BASE_URI = 'https://openstates.org/graphql'
OPENSTATES_API_KEY = os.environ.get('OPENSTATES_API_KEY')
DEFAULT_HEADERS = {
    'X-API-KEY': OPENSTATES_API_KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
}
DEFAULT_COUNT = 100  # 100 is the maximum count allowed by openstates


def legislator_ids(options):
    if options['session']:
        session = options['session']
    else:
        session = 1
    custom_query = f'''query={{
  jurisdiction(name: "Texas") {{
    legislativeSessions(first: 1) {{
      edges {{
        node {{
          identifier
          jurisdiction {{
            organizations(first: 1, classification: "legislature") {{
              edges {{
                node {{
                  children(first: 2) {{
                    edges {{
                      node {{
                        currentMemberships {{
                          person {{
                            id
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
    '''
    fetched_data = fetch_json(query=custom_query)
    leg_id_groups = fetched_data["data"]["jurisdiction"]["legislativeSessions"]["edges"][0]["node"]["jurisdiction"]["organizations"]["edges"][0]["node"]["children"]["edges"]
    leg_id_session = fetched_data["data"]["jurisdiction"]["legislativeSessions"]["edges"][0]["node"]["identifier"]
    leg_ids = []
    try:
        for group in leg_id_groups:
            memberships = group["node"]["currentMemberships"]
            for person in memberships:
                # LOG.warn(person)
                if person["person"] and person["person"]["id"]:
                    ocd_id = person["person"]["id"]
                    if len(ocd_id) > 1:
                        leg_ids.append(ocd_id)
        print(f"Found {len(leg_ids)} Legislators for the {leg_id_session} session.")
        return leg_ids[:options['max']]
    except Exception as e:
        print(f"Unable to get Legislators for the {leg_id_session} session. Error: {e}")
        return []


def legislator_list(id_list):
    leg_data_list = []
    custom_query = 'query={'
    count = 0
    for leg_id in id_list:
        custom_query += f'''
      p{count}: person(id: "{leg_id}") {{
        id
        name
        givenName
        familyName
        updatedAt
        party: currentMemberships(classification: "party") {{
          organization {{
            name
          }}
        }}
        links {{
          url
        }}
        image
        chamber: currentMemberships(classification: ["upper", "lower"]) {{
          post {{
            label
          }}
          organization {{
            name
            classification
            parent {{
              name
            }}
          }}
        }}
      }}
        '''
        count += 1
    custom_query += '}'
    fetched_data = fetch_json(query=custom_query)
    leg_id_data = fetched_data["data"]
    for c in range(count):
        data = leg_id_data[f'p{c}']
        # LOG.warn(data)
        leg_data_list.append(data)

    return leg_data_list


def bills(startCursor, options):
    bill_data = []
    first_count = DEFAULT_COUNT
    if options['max'] < DEFAULT_COUNT and options['max'] != 0:
        first_count = options['max']
    custom_query = f'''query={{
  b0: bills(first: {first_count}, after: "{startCursor}", jurisdiction: "Texas", session: "{options['session']}", classification: "bill") {{
    edges {{
      node {{
        id
        identifier
        title
        subject
        sponsorships {{
          name
          primary
          classification
        }}
        fromOrganization {{
          name
        }}
        updatedAt
        legislativeSession {{
          identifier
          name
        }}
        actions {{
          date
          description
          classification
          vote {{
            id
          }}
          order
        }}
        versions {{
          note
          links {{
            url
          }}
        }}
        votes {{
          edges {{
            node {{
              id
            }}
          }}
        }}
      }}
    }}
    totalCount
    pageInfo {{
      startCursor
      endCursor
    }}
  }}
}}
    '''
    try:
        fetched_data = fetch_json(query=custom_query)
        for data in fetched_data['data']['b0']['edges']:
            if 'node' in data:
                bill_data.append(data['node'])
    except:
        LOG.warn(f'Unable to retrieve bills.')

    bill_total = fetched_data['data']['b0']['totalCount']
    # bill_session=fetched_data['data']['b0']['edges'][0]['node']['legislativeSession']['identifier']
    if bill_total > 0:
        page_token = fetched_data['data']['b0']['pageInfo']['endCursor']
        # print(f"Found {bill_total} Bills for the {bill_session} session.")

    # LOG.warn(bill_data)
    bill_data.append(page_token)
    bill_data.append(bill_total)
    return bill_data


def fetch_json(query, headers=DEFAULT_HEADERS):
    response = requests.post(BASE_URI, data=query, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        LOG.warn(response.json())
        raise Exception(f"Query failed to run by returning code of {response.status_code} {query}")
