import pytest, os, sys
from importlib import import_module
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scrapper import parse_witness_list_html

'''
Edgecase:
https://capitol.texas.gov/tlodocs/86R/witlistbill/html/HB00864S.htm
"Representing" list for Rita Beving continues to a newline.
'''

testcases_dir = os.path.join(os.path.dirname(__file__), './testcases')
for test in os.listdir(testcases_dir):
    witness_list_html_file = os.path.join(os.path.dirname(__file__), f'./testcases/{test}/index.html')

    if os.path.isfile(witness_list_html_file):
        try:
            expected_value = import_module(f".{test}", package="testcases").expected_value
            witness_list_html = open(witness_list_html_file).read()
            witness_list = parse_witness_list_html(witness_list_html)
            assert(witness_list == expected_value)
            print("Pass")
        except AttributeError as e:
            print("Failed")
        except BaseException as e:
            print("Failed")
