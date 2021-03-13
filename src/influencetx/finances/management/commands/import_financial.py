"""
Django admin command wrapper around `sync_bill_data` in `influencetx.openstates.services`.
"""
from django.core.management.base import BaseCommand

from influencetx.openstates import fetch, services
from finances.models import FinancialDisclosure, Stock, Board, Gift, Job
from influencetx.legislators.models import Legislator
import json
import os.path as pth
import re
from influencetx.core import constants


def getHeldBy(choice):
    if choice == "spouse":
        return "Spouse"
    if choice == "dependent":
        return "Dependent"
    return "Filer"


CURRENT_YEAR = "2019"


class Command(BaseCommand):

    help = "Sync financial disclosures from json"

    def handle(self, *args, **options):
        FinancialDisclosure.objects.all().delete()
        result = get_sample_json("../../data/sample_financial_disclosures.json")
        mappings = get_sample_json("../../data/mappings.json")
        created_year = {}

        for item in result:
            split_name = re.findall("[A-Z][^A-Z]*", item["file_name"])
            last_name = split_name[0]

            if item.get("district"):
                legQuery = Legislator.objects.filter(
                    last_name=last_name,
                    district=item["district"],
                    chamber=item["chamber"],
                )
            else:
                legQuery = Legislator.objects.filter(
                    last_name=last_name,
                    first_name=item.get("first_name"),
                    chamber=item["chamber"],
                )

            mapping = mappings.get(item["file_name"])
            if len(legQuery) != 1 and mapping:
                district = mapping["district"]
                chamber = mapping["chamber"]
                legQuery = Legislator.objects.filter(district=district, chamber=chamber)

                # to double check manual matches didn't get mixed up
                if len(legQuery and legQuery[0] and legQuery[0].last_name):
                    if legQuery[0].last_name[0] != last_name[0]:
                        continue
                        # print("")
                        # print(
                        #     f"--- WARNING --- Matched {item['file_name']} with {legQuery[0].last_name}"
                        # )
                    # elif legQuery[0].last_name != last_name:
                    #     print(
                    #         f"Matched {item['file_name']} {item.get('first_name', 'NONE')} with {legQuery[0].last_name}"
                    #     )

            if len(legQuery) == 1:
                currentItem = FinancialDisclosure.objects.filter(
                    legislator=legQuery[0].id, year=item["year"]
                )
                if item["year"] == CURRENT_YEAR:
                    created_year[f"{legQuery[0].chamber}{legQuery[0].district}"] = {
                        "name": f"{legQuery[0].first_name} {legQuery[0].last_name}",
                        "file_name": item["file_name"],
                    }

                if len(currentItem) == 0:
                    f = FinancialDisclosure(year=item["year"], legislator=legQuery[0])
                    if item.get("candidate"):
                        f.candidate = item.get("candidate")
                    if item.get("elected_officer"):
                        f.elected_officer = item.get("elected_officer")
                    f.save()

                    for job in item["occupational_income"]:
                        new_job = Job(
                            financial_disclosure=f,
                            employer=job["employer"],
                            held_by=getHeldBy(job["held_by"]),
                        )
                        if job.get("position"):
                            new_job.position = job.get("position")
                        new_job.save()

                    for stock in item["stocks"]:
                        Stock(
                            financial_disclosure=f,
                            name=stock["name"],
                            held_by=getHeldBy(stock["held_by"]),
                            num_shares=stock["num_shares"],
                        ).save()
                    for board in item["boards"]:
                        Board(
                            financial_disclosure=f,
                            name=board["name"],
                            held_by=getHeldBy(board["held_by"]),
                            position=board["position"],
                        ).save()

                    for gift in item["gifts"]:
                        Gift(
                            financial_disclosure=f,
                            donor=gift["name"],
                            recipient=getHeldBy(gift["recipient"]),
                            description=gift["description"],
                        ).save()

            # elif item["year"] == CURRENT_YEAR:
            #     # the ones left these are not current legislators as far as I can tell
            #     print(
            #         f"\nCould not determine legId for {item.get('first_name')} {last_name}, {item.get('chamber')} {item.get('district')}, {item.get('file_name')}"
            #     )
            #     if len(legQuery):
            #         print(f"More than 1 possibility for {item.get('file_name')}")

        # print(
        #     "House missing districts ",
        #     [i for i in range(1, 151) if not created_year.get(f"House{i}")],
        # )
        # print(
        #     "Senate missing districts ",
        #     [i for i in range(1, 32) if not created_year.get(f"Senate{i}")],
        # )
        print(
            f"\n\033[92m{len(FinancialDisclosure.objects.all())} Financial Disclosures created"
        )


LOCAL_DIR = pth.dirname(pth.abspath(__file__))


def get_sample_json(filename):
    with open(pth.join(LOCAL_DIR, filename)) as f:
        api_data = json.load(f)
    return api_data
