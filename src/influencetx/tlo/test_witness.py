import re
from bs4 import BeautifulSoup, SoupStrainer
import requests

bill_id = "HB 864"
session = "86"

# ex: "HB 864" -> "https://capitol.texas.gov/tlodocs/86R/witlistbill/html/HB00864H.htm"
parsed_bill_id = re.search(r"(\w+)\s+(\d+)", bill_id)
bill_type = parsed_bill_id.group(1)
bill_number = parsed_bill_id.group(2).zfill(5)
url_prefix = f"https://capitol.texas.gov/tlodocs/{session}R/witlistbill/html/{bill_type}{bill_number}"
house_url = f"{url_prefix}H.htm"
senate_url = f"{url_prefix}S.htm"

res = requests.get(house_url)


##### Basic Test
# parsing all <p/> blocks up front may not be efficient
filter = SoupStrainer('p') # only <p/> tags contain text that we care about
text_blocks = BeautifulSoup(res.content, "html.parser", parse_only=filter)
selecting = None;
for block in text_blocks:
    text = block.get_text(strip=True)
    print(f"[{text}]")


# ##### For real
# content = BeautifulSoup(res.content, "html.parser")
#
# def is_section(text, section):
#     return re.match(section, text, re.IGNORECASE)
#
# def identify_witness(text, section, not_testifying):
#     print(f"::{section}, testifying={!not_testifying}: {text}")
#
# wits_for = []
# wits_against = []
# wits_ons = []
# wits_for_no_testify = []
# wits_against_no_testify = []
# wits_on_no_testify = []
#
#
# text = content.find_next('p')
# section = None
# not_testifying = False
# while text:
#     if (is_section(text, "for")):
#         identify_witness(text, "for")
#     if (is_section(text, 'Registering, but not testifying')):
#         not_testifying = True
#     else:
#         text = content.find_next('p')
#
# print(f"get it? {text}")
#
# witness_types = ('for', 'on', 'against', 'Registering, but not testifying');
