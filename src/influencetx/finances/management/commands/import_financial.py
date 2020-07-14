"""
Django admin command wrapper around `sync_bill_data` in `influencetx.openstates.services`.
"""
from django.core.management.base import BaseCommand

from influencetx.openstates import fetch, services
from finances.models import FinancialDisclosure
from influencetx.legislators.models import Legislator
import json
import os.path as pth
import re
class Command(BaseCommand):

    help = "Sync bill witness data from Texas Legislature Online"

    def handle(self, *args, **options):
        # FinancialDisclosure.objects.all().delete()
        result = get_sample_json("../../data/sample_financial_disclosures.json")
        for item in result:
            split_name = re.findall('[A-Z][^A-Z]*', item["file_name"])
            last_name = split_name[0]
            legQuery = Legislator.objects.filter(last_name=last_name, chamber=item["chamber"]) 
            if(len(legQuery) == 1):
                currentItem = FinancialDisclosure.objects.filter(legislator=legQuery[0].id, year=item["year"])       
                print(currentItem)
                if(len(currentItem) == 0):
                    f = FinancialDisclosure(year=item["year"], legislator=legQuery[0])
                    if(item.get("candidate")):
                        f.candidate=item.get("candidate")
                    if(item.get("elected_officer")):
                        f.elected_officer=item.get("elected_officer")
                    f.save()
                    print("Created " + item["file_name"] + item["year"])
                else:
                    foundDbItem = currentItem[0]
                    foundDbItem.year = item["year"]
                    foundDbItem.elected_officer = item["elected_officer"]
                    if("candidate" in item):
                        foundDbItem.candidate = item["candidate"]
                    foundDbItem.legislator = legQuery[0]
                    foundDbItem.save()
                    # print("Updated " + item["file_name"]  + item["year"])
            else:
                print("Could not determine legId for " + item["file_name"] )
        print(FinancialDisclosure.objects.all())


LOCAL_DIR = pth.dirname(pth.abspath(__file__))

def get_sample_json(filename):
    with open(pth.join(LOCAL_DIR, filename)) as f:
        api_data = json.load(f)
    return api_data

