from bs4 import BeautifulSoup
from datetime import datetime
import os
import json


def process_inventors(inventors):
    pass


def process_assignees(assignees):
    pass


def extract_claim_id(js):
    try:
        return int(js['id'].split("-")[-1])
    except KeyError:
        return 0


for root, dirs, files in os.walk("E:/Patent2017"):
    for name in files:
        filepath = os.path.join(root, name)
        js = json.load(open(filepath, encoding="utf8"))
        # patentId
        patentID = js['documentId'][2:]
        # issueDate
        temp = js['publishedDate']['raw']
        issueDate = datetime.strptime(temp, "%Y%m%d").strftime("%Y-%m-%d")
        # title
        title = js['title']
        # abstract
        abstract = js['abstract']['plain'].rstrip()
        # inventors
        inventors = js['inventors']
        # assignee
        assignees = js['assignees']
        # application number
        temp = js['applicationId'][2:]
        applNo = temp[:2] + "/" + temp[2:5] + "," + temp[5:]
        # fileDate
        temp = js['applicationDate']['raw']
        fileDate = datetime.strptime(temp, "%Y%m%d").strftime("%Y-%m-%d")
        # usClass
        # intlClass
        # field of search
        # references
        # examiners
        primary_examiner = "-"
        assistant_examiner = "-"
        examiners = js['examiners']
        for ex in examiners:
            if ex['type'] == "PRIMARY":
                primary_examiner = ex['name'].replace(",", ";")
            else:
                assistant_examiner = ex['name'].replace(",", ";")
        # attorney
        # we skip this field for now because of the bug in the Java Parsing code
        # Please closely monitor https://github.com/USPTO/PatentPublicData/issues/61
        attorney = "-"
        # claim
        claims = js['claims']
        claims.sort(key=extract_claim_id)
        claim = ""
        for c in claims:
            s = [x.rstrip() for x in c['plain'].split(" <> ")]
        claim += " ".join(s)
        claim += "\n"
        claim.rstrip()
        # description


        process_inventors(inventors)
        process_assignees(assignees)
        break
    break