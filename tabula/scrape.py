import csv
import json
import re
from os import walk

rawFiles = []
for (dirpath, dirnames, filenames) in walk("./raw/House/2019"):
    for filename in filenames:
        rawFiles.append({"filename": filename, "chamber": "House", "year": "2019"})
    break
for (dirpath, dirnames, filenames) in walk("./raw/House/2018"):
    for filename in filenames:
        rawFiles.append({"filename": filename, "chamber": "House", "year": "2018"})
    break

for (dirpath, dirnames, filenames) in walk("./raw/Senate/2019"):
    for filename in filenames:
        if "tabula" in filename:
            rawFiles.append({"filename": filename, "chamber": "Senate", "year": "2019"})
    break
for (dirpath, dirnames, filenames) in walk("./raw/Senate/2018"):
    for filename in filenames:
        if "tabula" in filename:
            rawFiles.append({"filename": filename, "chamber": "Senate", "year": "2018"})
    break


def cleanStr(str):
    result = str.replace('"', "").strip()
    result = re.sub("^,", "", result)
    result = re.sub(",$", "", result)
    return result.strip()


def getOwner(line):
    if "X FILER" in line:
        return "filer"
    if "X SPOUSE" in line:
        return "spouse"
    if "X DEPENDENT" in line:
        return "dependent"


def getChecked(line, options=[]):
    for opt in options:
        if "X " + opt in line:
            return opt


sections = ["4,REASON,", "2,EMPLOYMENT NAME AND ADDRESS OF EMPLOYER / POSITION HELD"]

fullDict = {}


def parseFile(file):
    fileName = file["filename"]
    chamber = file["chamber"]
    year = file["year"]
    prettyName = fileName.replace("tabula-", "").replace(" PFS.csv", "")
    fullDict[prettyName] = {
        "chamber": chamber,
        "year": year,
        "file_name": prettyName[0:-4],
        "occupational_income": [],
        "stocks": [],
        "mutual_fund": [],
        "boards": [],
        "lobbyists": [],
        "gifts": [],
        "property": [],
        "business_interests": [],
        "owned_businesses": [],
        "lobbyists_fees": [],
        "gov_contracts": [],
        "bond_counsel": [],
    }
    myDict = fullDict[prettyName]
    with open("./raw/" + chamber + "/" + year + "/" + fileName, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        i = 0
        currentSection = ""
        currentSubSection = ""
        currentPart = ""
        lastRow = ""
        lastLastRow = ""
        for row in spamreader:
            line = " ".join(row)
            if re.search("PART \d", line):
                currentPart = line
            if re.search("\d,\w", line):
                currentSubSection = line
            if "NAME TITLE; FIRST; MI OFFICE USE ONLY," in lastRow:
                myDict["first_name"] = cleanStr(
                    line.replace("The Honorable", "")
                    .replace("Mr.", "")
                    .replace("Ms.", "")
                    .replace("Mrs.", "")
                ).split(" ")[0]
            # income
            if "INCOMEPART 1A" in currentPart:
                if "INFORMATION RELATES TO" in lastRow:
                    myDict["occupational_income"].append({"held_by": getOwner(line)})

                if "EMPLOYER" in lastRow and "POSITION HELD" not in lastRow:
                    myDict["occupational_income"][-1]["employer"] = cleanStr(line)

                if (
                    "POSITION HELD" in lastRow
                    and "EMPLOYMENT NAME AND " not in lastRow
                    and "NATURE OF OCCUPATION" not in line
                ):
                    myDict["occupational_income"][-1]["position"] = cleanStr(line)
                if "ADDRESS / PO BOX;" in lastRow and "POSITION HELD" not in line:
                    myDict["occupational_income"][-1]["address"] = cleanStr(line)
                if (
                    "ADDRESS / PO BOX;" in lastLastRow
                    and "POSITION HELD" not in line
                    and "POSITION HELD" not in lastRow
                ):
                    myDict["occupational_income"][-1]["address"] += " /n " + cleanStr(
                        line
                    )

            if "STATEMENT X CANDIDATE" in line:
                myDict["candidate"] = (
                    line.replace("_", "")
                    .replace('"', "")
                    .replace("STATEMENT X CANDIDATE", "")
                )
            if "X ELECTED OFFICER" in line:
                elected_officer = (
                    line.replace("X ELECTED OFFICER", "")
                    .replace("(INDICATE OFFICE)", "")
                    .replace("_", "")
                    .replace("""\"""", "")
                )
                myDict["elected_officer"] = cleanStr(elected_officer)
                distSearch = re.search("District \d+", elected_officer, re.IGNORECASE)
                if distSearch:
                    myDict["district"] = int(re.search("\d+", distSearch[0])[0])
                distHDSearch = re.search(" HD\s?\d+", elected_officer, re.IGNORECASE)
                if distHDSearch:
                    myDict["district"] = int(re.search("\d+", distHDSearch[0])[0])
                distSDSearch = re.search(" SD\s?\d+", elected_officer, re.IGNORECASE)
                if distSDSearch:
                    myDict["district"] = int(re.search("\d+", distSDSearch[0])[0])

            # STOCKS
            if "STOCKPART 2" in currentPart:
                if "BUSINESS ENTITY NAME" in lastRow:
                    myDict["stocks"].append({"name": cleanStr(line)})
                if "STOCK HELD OR" in lastRow:
                    myDict["stocks"][-1]["held_by"] = getOwner(line)

                if "NUMBER OF SHARES" in lastRow:
                    myDict["stocks"][-1]["num_shares"] = getChecked(
                        line,
                        ["LESS THAN 100", "100 TO 499", "500 TO 999", "1,000 TO 4,999"],
                    )
                if (
                    "NUMBER OF SHARES" in lastLastRow
                    and not myDict["stocks"][-1]["num_shares"]
                ):
                    myDict["stocks"][-1]["num_shares"] = getChecked(
                        line, ["LESS THAN 10K", "10,000 OR MORE"]
                    )

                if lastRow == "4,IF SOLD X NET GAIN":
                    myDict["stocks"][-1]["net_gain"] = getChecked(
                        line,
                        [
                            "LESS THAN $5,000",
                            "$5,000 - $9,999",
                            "$10,000 - $24,999",
                            "$25,000--OR MORE",
                        ],
                    )
                if line == '"",X NET LOSS':
                    myDict["stocks"][-1]["net_loss"] = getChecked(
                        lastRow,
                        [
                            "LESS THAN $5,000",
                            "$5,000 - $9,999",
                            "$10,000 - $24,999",
                            "$25,000--OR MORE",
                        ],
                    )

            if "INTERESTS IN REAL PROPERTYPART 7A" in currentPart:
                if "HELD OR ACQUIRED BY" in lastRow:
                    myDict["property"].append({"held_by": getOwner(line)})
                if (
                    "STREET ADDRESS STREET ADDRESS, INCLUDING CITY, COUNTY, AND STATE"
                    in lastRow
                ):
                    myDict["property"][-1]["address"] = cleanStr(
                        line.replace("NOT AVAILABLE", "")
                    )
                if "X CHECK IF FILER" in line:
                    myDict["property"][-1]["home_address"] = True
                if "HOME ADDRESS" in line:
                    if "address" in myDict["property"][-1]:
                        myDict["property"][-1]["address"] += " \n " + cleanStr(
                            line.replace("HOME ADDRESS", "  ")
                        )
                    else:
                        myDict["property"][-1]["address"] = cleanStr(
                            line.replace("HOME ADDRESS", "  ")
                        )
                if "LOTS " in line and "DESCRIPTION" not in line:
                    lotsLine = line.replace("LOTS", "")
                    lotsNum = re.search("\d+\.?\,?\d+", lotsLine)
                    if "lots" in lotsLine and lotsNum:
                        myDict["property"][-1]["lots"] = float(lotsNum[0])
                    if "acres" in lotsLine and lotsNum:
                        myDict["property"][-1]["acres"] = float(lotsNum[0])
                if "ACRES " in line:
                    myDict["property"][-1]["county"] = cleanStr(
                        line.replace("ACRES", "")
                    )

            # MUTUAL
            if "MUTUAL FUNDSPART 4" in currentPart:
                if "MUTUAL FUND NAME" in lastRow:
                    currentMF = {"name": line}
                if "SHARES OF MUTUAL FUND" in lastRow and "ACQUIRED BY " in line:
                    currentMF["held_by"] = getOwner(line)

                if "NUMBER OF SHARES" in lastRow:
                    currentMF["num_shares"] = getChecked(
                        line,
                        ["LESS THAN 100", "100 TO 499", "500 TO 999", "1,000 TO 4,999"],
                    )
                if "NUMBER OF SHARES" in lastLastRow:
                    # currentMF["num_shares"] = getChecked(line, ['LESS THAN 10K', '10,000 OR MORE'])
                    if "X LESS THAN 10K" in line:
                        currentMF["num_shares"] = "LESS THAN 10K"
                    if "X 10,000 OR MORE" in line:
                        currentMF["num_shares"] = "10,000 OR MORE"

                if "IF SOLD X NET GAIN" in lastRow:
                    currentMF["net_gain"] = getChecked(
                        line,
                        [
                            "LESS THAN $5,000",
                            "$5,000 - $9,999",
                            "$10,000 - $24,999",
                            "$25,000--OR MORE",
                        ],
                    )
                if line == '"",X NET LOSS':
                    currentMF["net_loss"] = getChecked(
                        lastRow,
                        [
                            "LESS THAN $5,000",
                            "$5,000 - $9,999",
                            "$10,000 - $24,999",
                            "$25,000--OR MORE",
                        ],
                    )

                if "NET LOSS" in line:
                    if (
                        len(myDict["mutual_fund"]) == 0
                        or myDict["mutual_fund"][-1]["name"] != currentMF["name"]
                        and currentMF["name"]
                    ):
                        myDict["mutual_fund"].append(currentMF)
                        currentMF = {"name": ""}

            if "GIFTSPART 8" in currentPart:
                if "DONOR NAME AND ADDRESS" in lastRow:
                    myDict["gifts"].append({"name": cleanStr(line)})
                if "RECIPIENT" in lastRow:
                    myDict["gifts"][-1]["recipient"] = getOwner(line)
                if "DESCRIPTION OF GIFT" in line:
                    myDict["gifts"][-1]["description"] = cleanStr(
                        line.replace("DESCRIPTION OF GIFT", "").replace("3", "")
                    )

            # BOARDS
            if "BOARDS AND EXECUTIVE POSITIONSPART 12" in currentPart:
                if "ORGANIZATION" in line:
                    myDict["boards"].append(
                        {
                            "name": re.sub(
                                "^\d, ", "", cleanStr(line.replace("ORGANIZATION", ""))
                            )
                        }
                    )

                if "POSITION HELD BY" not in line and "POSITION HELD" in line:
                    myDict["boards"][-1]["position"] = re.sub(
                        "^\d, ", "", cleanStr(line.replace("POSITION HELD", ""))
                    )
                if "POSITION HELD BY" in lastRow:
                    myDict["boards"][-1]["held_by"] = getOwner(line)

            if "INTEREST IN BUSINESS IN COMMON WITH LOBBYISTPART 14" in currentPart:
                if "BUSINESS ENTITY NAME AND ADDRESS" in lastRow:
                    myDict["lobbyists"].append(
                        {
                            "name": line,
                        }
                    )

                if "INTEREST HELD BY" in lastRow:
                    myDict["lobbyists"][-1]["held_by"] = getOwner(line)

            if "INTEREST IN BUSINESS ENTITIESPART 7B" in currentPart:
                section = myDict["business_interests"]
                if "HELD OR ACQUIRED BY" in lastRow:
                    section.append({"held_by": getOwner(line)})
                if "DESCRIPTION NAME AND ADDRESS" in lastLastRow:
                    section[-1]["name"] = line
                if "X (Check If Filer's Home Address)" in line:
                    section[-1]["home_address"] = True

            if "TO A LOBBYIST OR LOBBYIST'S EMPLOYER PART 15" in currentPart:
                section = myDict["lobbyists_fees"]
                if "PERSON OR ENTITY " in line:
                    section.append({"name": line.replace("PERSON OR ENTITY ", "")})
                if "FEE CATEGORY" in lastRow:
                    section[-1]["amount"] = getChecked(
                        line,
                        [
                            "LESS THAN $5,000",
                            "$5,000 - $9,999",
                            "$10,000 - $24,999",
                            "$25,000--OR MORE",
                        ],
                    )

            if "CONTRACTS TO SELL GOODS OR SERVICES TO A PART 19" in currentPart:
                section = myDict["gov_contracts"]
                if "FILER PARTIES " in line:
                    section.append({"held_by": getOwner(line)})
                if "BUSINESS PARTIES NAME AND ADDRESS" in lastLastRow:
                    section[-1]["business_parties"] = line
                if (
                    "GOVERNMENTAL PARTIES" in lastLastRow
                    and "NAME AND ADDRESS" in lastRow
                ):
                    section[-1]["gov_parties"] = line

            if "BOND COUNSEL SERVICES PROVIDED BY A LEGISLATORPART 20" in currentPart:
                section = myDict["bond_counsel"]
                if "ISSUER NAME " in line:
                    section.append(
                        {"issuer": line.replace("ISSUER NAME", "").replace("1,", "")}
                    )
                if "ISSUANCE DATE" in line:
                    section[-1]["issuance_date"] = line.replace(
                        "ISSUANCE DATE", ""
                    ).replace("2,", "")
                if "ISSUANCE AMOUNT " in line:
                    section[-1]["issuance_amount"] = line.replace(
                        '3,"ISSUANCE AMOUNT', ""
                    ).replace("ISSUANCE AMOUNT ", "")
                if "FEES PAID TO FILER" in line:
                    section[-1]["fees_paid_to_filer"] = getChecked(
                        line,
                        [
                            "LESS THAN $5,000",
                            "$5,000 - $9,999",
                            "$10,000 - $24,999",
                            "$25,000--OR MORE",
                        ],
                    )
                if (
                    "FEES PAID TO FILER'S FIRM NAME AND ADDRESS OF FIRM" in lastRow
                    and "YES X"
                ):
                    section[-1]["fees_paid_to_files_firm"] = True
                if (
                    len(section) > 0
                    and "fees_paid_to_files_firm" in section[-1]
                    and section[-1]["fees_paid_to_files_firm"]
                    and "LESS THAN $5,000" in line
                ):
                    section[-1]["fees_paid_to_files_firm"] = getChecked(
                        line,
                        [
                            "LESS THAN $5,000",
                            "$5,000 - $9,999",
                            "$10,000 - $24,999",
                            "$25,000--OR MORE",
                        ],
                    )

            if "PART 11A" in currentPart:
                section = myDict["owned_businesses"]
                if "BUSINESS ASSOCIATION NAME AND ADDRESS" in lastLastRow:
                    section.append({"name": line})
                if "BUSINESS TYPE " in line:
                    section[-1]["type"] = getChecked(
                        line,
                        [
                            "Corporation",
                            "Limited Partnership",
                            "Profesional Association",
                        ],
                    )
                    # not work, not sure why
                if "BUSINESS TYPE " in lastRow and not section[-1]["type"]:
                    section[-1]["type"] = getChecked(
                        lastRow,
                        ["Firm" "Limited Liability Partnership" "Joint Venture"],
                    )
                if "BUSINESS TYPE " in lastLastRow and not section[-1]["type"]:
                    section[-1]["type"] = getChecked(
                        lastLastRow,
                        ["Partnership", "Professional Corporation", "O__th_e_r"],
                    )
                if (
                    len(section) > 0
                    and "HELD, ACQUIRED," in lastRow
                    and "OR SOLD BY " in line
                ):
                    section[-1]["held_by"] = getOwner(line)

            i = i + 1
            lastLastRow = lastRow
            lastRow = line


for file in rawFiles:
    if ".csv" in file["filename"]:
        parseFile(file)


def cleanStrObj(obj):
    print(str)
    for key in obj:
        obj[key] = cleanStr(obj[key])
    return obj


with open("parsedOutput.json", "w") as outfile:
    for rep in fullDict:
        for key in fullDict[rep]:
            myValue = fullDict[rep][key]
            if isinstance(myValue, str):
                fullDict[rep][key] = cleanStr(myValue)
            if isinstance(myValue, list):
                map(lambda a: cleanStrObj(a), myValue)
    json.dump(list(fullDict.values()), outfile, indent=4)
