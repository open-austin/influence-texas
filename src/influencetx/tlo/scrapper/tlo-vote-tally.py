# from https://github.com/lazarus1331/tlo-vote-tally/blob/master/tlo-vote-tally.py
import argparse
import csv
import lxml.html
import re
import requests
from time import sleep

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

def get_chamber_bills(chamber, session='85R'):
    """
    Return a list of tlo urls for each bill detected.
    """
    print(f"Getting {chamber} bills")
    chamber_map = {
        'senate': 'senatefiled',
        'house': 'housefiled',
    }
    url = f"https://capitol.texas.gov/Reports/Report.aspx?LegSess={session}&ID={chamber_map[chamber]}"
    page = lxmlize(url)
    # the only links on the page are to tlo urls
    hrefs = page.xpath('//@href')
    links = []
    for url in hrefs:
        if re.match(r'.*=[SH]B\d+$', url):
            links.append(url)
    print(f'Found {len(links)} {chamber} bills')
    return links

def scrape_chamber(chamber, bill_list):
    """
    Return a list dictionary objects for each bill's vote record counts.
    Also includes links to journals used as original source, and date of vote.
    """
    #bill_list = bill_list[-300:0]
    bill_votes = []
    print(f'Scraping bill urls for chamber {chamber}')
    s = requests.Session()
    for url in bill_list:
        #print(url)
        bill = re.search(r'[SH]B\d+$', url).group()
        page = lxmlize(url, s)
        house_vote_records = page.xpath('//table/tr[@id="houvote"]')
        senate_vote_records = page.xpath('//table/tr[@id="senvote"]')
        num_house_votes = len(house_vote_records)
        num_senate_votes = len(senate_vote_records)
        h_data, s_data = [], []
        for record in house_vote_records:
            journal_link = record.xpath('./td[2]/a/@href')[0]
            type = record.xpath('./td[2]/a/text()')[0]
            date = record.xpath('./td[4]/text()')[0].strip()
            h_data.append({'date': date, 'source': journal_link, 'type': type})
        for record in senate_vote_records:
            journal_link = record.xpath('./td[2]/a/@href')[0]
            type = record.xpath('./td[2]/a/text()')[0]
            date = record.xpath('./td[4]/text()')[0].strip()
            s_data.append({'date': date, 'source': journal_link, 'type': type})
        data_row = {f'{bill}': {
            'lower_votes': num_house_votes,
            'upper_votes': num_senate_votes,
            'lower': h_data,
            'upper': s_data
        }}
        #bill_votes.append(data_row)
        yield data_row
    #return bill_votes

def write_data(data, file='results.csv', full=False):
    with open(file,'a') as myfile:
        writer = csv.writer(myfile, delimiter=',', quotechar='"')
        if full:
            headers = ['bill_id', 'chamber', 'date', 'journal']
            writer.writerow(headers)
            for row in data:
                for k, v in row.items():
                    bill_id = k
                    #print(bill_id)
                    for record in v['lower']:
                        full_row = [bill_id, 'house', record['date'],
                            record['source']]
                        writer.writerow(full_row)
                        myfile.flush()
                    for record in v['upper']:
                        full_row = [bill_id, 'senate', record['date'],
                            record['source']]
                        writer.writerow(full_row)
                        myfile.flush()
        else:
            headers = ['bill_id', 'lower_votes', 'upper_votes']
            writer.writerow(headers)
            for row in data:
                for k, v in row.items():
                    #print(k)
                    short_row = [k, v['lower_votes'], v['upper_votes']]
                    writer.writerow(short_row)
                    myfile.flush()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--chamber", help="Select between house|senate",
                        choices=['house', 'senate'])
    parser.add_argument("-f","--file", help="Output to this file",
                        type=str, default='results.csv')
    parser.add_argument("-m","--max", help="Maximum number of bills to process",
                        type=int, default=None)
    parser.add_argument("-o","--output", help="Output per vote data",
                        action="store_true", default=False)
    parser.add_argument("-s","--session", help="Enter the Session ID, e.g. '85R'",
                        type=str, default='85R')
    args = parser.parse_args()
    print('Starting...')
    if args.chamber:
        bill_urls = get_chamber_bills(args.chamber, args.session)
        if args.max > 0:
            bill_urls = get_chamber_bills(args.chamber, args.session)[0:args.max]
        write_data(scrape_chamber(args.chamber, bill_urls), args.file,
            args.output)
    else:
        if args.max:
            last = args.max//2
            hbill_urls = get_chamber_bills('house', args.session)[0:last]
        else:
            hbill_urls = get_chamber_bills('house', args.session)
        write_data(scrape_chamber('house', hbill_urls), args.file,
            args.output)
        if args.max:
            last = args.max//2
            sbill_urls = get_chamber_bills('senate', args.session)[0:last]
        else:
            sbill_urls = get_chamber_bills('senate', args.session)
        write_data(scrape_chamber('senate', sbill_urls), args.file,
            args.output)
    print('Finished.')

# ----------------------------------------------
if __name__ == "__main__":
    # execute only if run as a script
    main()
