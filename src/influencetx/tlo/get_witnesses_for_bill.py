import re
from bs4 import BeautifulSoup, SoupStrainer
import requests

'''
TODO:
- Need to parse witnesses for senate_url
'''
def get_witnesses_for_bill(bill_id, session):
    # ex: "HB 864" -> "https://capitol.texas.gov/tlodocs/86R/witlistbill/html/HB00864H.htm"
    parsed_bill_id = re.search(r"(\w+)\s+(\d+)", bill_id)
    bill_type = parsed_bill_id.group(1)
    bill_number = parsed_bill_id.group(2).zfill(5)
    url_prefix = f"https://capitol.texas.gov/tlodocs/{session}R/witlistbill/html/{bill_type}{bill_number}"
    house_url = f"{url_prefix}H.htm"
    senate_url = f"{url_prefix}S.htm"

    res = requests.get(house_url)

    # ##### Basic Test
    # # parsing all <p/> blocks up front may not be efficient
    # filter = SoupStrainer('p') # only <p/> tags contain text that we care about
    # text_blocks = BeautifulSoup(res.content, "html.parser", parse_only=filter)
    # selecting = None;
    # for block in text_blocks:
    #     text = block.get_text(strip=True)
    #     print(f"[{text}]")

    ##### For real
    content = BeautifulSoup(res.content, "html.parser").find("p")

    # Make regex to check if text is header of a new section
    # ex: make_section_regex(0) > "^for|^against|^on|^Registering, but not testifying|^for|^against|^on"
    # Return "None" if we are at the last section and there are no more new sections to be discovered
    def make_section_regex(current_section):
        return ("|").join([w["regex"] for w in witness_sections[(current_section+1):]]) or None

    # Check if we are at the start of a new section
    def is_new_section(section_regex, text):
        try:
            return re.match(section_regex, text, re.IGNORECASE)
        except:
            return None

    # Check if we are at the end of a witness list page
    def is_page_end(text):
        return re.match(r"^\d", text)

    # Update our current_section
    def get_new_section(text, current_section):
        for i,w in enumerate(witness_sections[(current_section+1):], start=(current_section+1)):
            if (re.match(w["regex"], text, re.IGNORECASE)):
                return i, make_section_regex(i)

    def get_next_line(content):
        content = content.find_next('p')
        try:
            text = content.get_text(strip=True)
        except:
            text = None
        return content, text

    def get_witness_data(text, current_section):
        m=re.match(r"(.+),\s+(.+)\s+\((.+)\)", text)
        # print(f"firstname: {m.group(2)}")
        # print(f"lastname: {m.group(1)}")
        # print(f"representing: {m.group(3)}")
        witness = {
            "firstname": m.group(2),
            "lastname": m.group(1),
            "representing": [x.strip() for x in m.group(3).split(";")]
        }
        witness_sections[current_section]["witnesses"].append(witness)

    witness_sections = [
        {
            "name": "for",
            "regex": "^for(\s+)*:",
            "witnesses": []
        },
        {
            "name": "against",
            "regex": "^against(\s+)*:",
            "witnesses": []
        },
        {
            "name": "on",
            "regex": "^on(\s+)*:",
            "witnesses": []
        },
        {
            "name": "Registering, but not testifying",
            "regex": "^Registering,\s+but\s+not\s+testifying(/s+)*:"
        },
        {
            "name": "for_no_testify",
            "regex": "^for(\s+)*:",
            "witnesses": []
        },
        {
            "name": "against_no_testify",
            "regex": "^against(\s+)*:",
            "witnesses": []
        },
        {
            "name": "on_no_testify",
            "regex": "^on(\s+)*:",
            "witnesses": []
        }
    ]

    current_section = -1
    section_regex = make_section_regex(current_section)
    content, text = get_next_line(content)

    while text:
        if (is_new_section(section_regex, text)):
            # If we're at a new section headering, update current_section and section_regex
            current_section, section_regex = get_new_section(text, current_section)
            # print(f"##### [{witness_sections[current_section]['name']}]")
        elif (is_page_end(text)):
            break
        elif (current_section > -1):
            get_witness_data(text, current_section)
        content, text = get_next_line(content)

    for section in witness_sections:
        del section["regex"]

    return witness_sections
