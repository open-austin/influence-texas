"""
Django admin command wrapper around `sync_bill_data` in `influencetx.openstates.services`.
"""
from django.core.management.base import BaseCommand

from influencetx.openstates import fetch, services
from finances.models import FinancialDisclosure, Stocks, Boards, Gifts, Jobs
from influencetx.legislators.models import Legislator
import json
import os.path as pth
import re
from influencetx.core import constants


def getHeldBy(choice):
    if (choice == "spouse"):
        return 'Spouse'
    if (choice == "dependent"):
        return 'Dependent'
    return 'Filer'


class Command(BaseCommand):

    help = "Sync financial disclosures from json"

    def handle(self, *args, **options):
        FinancialDisclosure.objects.all().delete()
        result = get_sample_json(
            "../../data/sample_financial_disclosures.json")
        mappings = get_sample_json("../../data/mappings.json")

        for item in result:
            split_name = re.findall('[A-Z][^A-Z]*', item["file_name"])
            last_name = split_name[0]

            if (item.get("district")):
                legQuery = Legislator.objects.filter(last_name=last_name,
                                                     district=item["district"],
                                                     chamber=item["chamber"])
            else:
                legQuery = Legislator.objects.filter(
                    last_name=last_name,
                    first_name=item.get("first_name"),
                    chamber=item["chamber"])

            if (len(legQuery) != 1 and mappings.get(item["file_name"])):
                district = mappings.get(item["file_name"])["district"]
                legQuery = Legislator.objects.filter(district=district,
                                                     chamber=item["chamber"])

            if (len(legQuery) == 1):
                if (last_name == "Murr"):
                    print(item["year"])
                currentItem = FinancialDisclosure.objects.filter(
                    legislator=legQuery[0].id, year=item["year"])
                if (len(currentItem) == 0):
                    f = FinancialDisclosure(year=item["year"],
                                            legislator=legQuery[0])
                    if (item.get("candidate")):
                        f.candidate = item.get("candidate")
                    if (item.get("elected_officer")):
                        f.elected_officer = item.get("elected_officer")
                    f.save()

                    for job in item["occupational_income"]:
                        new_job = Jobs(financial_disclosure=f,
                                       employer=job["employer"],
                                       held_by=getHeldBy(job["held_by"]))
                        if job.get("position"):
                            new_job.position = job.get("position")
                        new_job.save()

                    for stock in item["stocks"]:
                        Stocks(financial_disclosure=f,
                               name=stock["name"],
                               held_by=getHeldBy(stock["held_by"]),
                               num_shares=stock["num_shares"]).save()
                    for board in item["boards"]:
                        Boards(financial_disclosure=f,
                               name=board["name"],
                               held_by=getHeldBy(board["held_by"]),
                               position=board["position"]).save()

                    for gift in item["gifts"]:
                        Gifts(financial_disclosure=f,
                              donor=gift["name"],
                              recipient=getHeldBy(gift["recipient"]),
                              description=gift["description"]).save()
                print('.')

            else:
                print(
                    "Could not determine legId for " +
                    str(item.get("first_name")) + ' ' + str(last_name) + ' ' +
                    str(item.get("chamber")) + " " +
                    str(item.get("district")) + " " + item.get("file_name"),
                    len(legQuery)
                )
        # print(FinancialDisclosure.objects.all())


LOCAL_DIR = pth.dirname(pth.abspath(__file__))


def get_sample_json(filename):
    with open(pth.join(LOCAL_DIR, filename)) as f:
        api_data = json.load(f)
    return api_data
