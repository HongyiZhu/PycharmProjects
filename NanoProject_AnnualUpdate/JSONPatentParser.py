from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import json


def process_inventors(patentID, inventors):
    for i, inv in enumerate(inventors):
        fName = inv['name']['firstName'] if inv['name']['firstName'] != "" else "-"
        mName = inv['name']['middleName'] if inv['name']['middleName'] != "" else "-"
        lName = inv['name']['lastName'] if inv['name']['lastName'] != "" else "-"
        city = inv['address']['city'] if inv['address']['city'] != "" else "-"
        state = inv['address']['state'] if inv['address']['state'] != "" else "-"
        country = inv['address']['country'] if inv['address']['country'] != "" else "-"
        rank = i

    pass


def process_assignees(patentID, assignees):
    pass


def process_citations(patentID, citations):
    for c in citations:
        if c['text'][:2] == "US":
            cite = re.split("[a-zA-Z]", c['text'][2:])[0]
            # TODO InSert into database
        else:
            pass


def extract_claim_id(js):
    try:
        return int(js['id'].split("-")[-1])
    except KeyError:
        return 0


# for root, dirs, files in os.walk("E:/Patent2017"):
for root, dirs, files in os.walk("C:/Users/Hongyi/Desktop/Patent2017"):
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
        # TODO
        # intlClass
        # TODO
        # field of search
        # TODO
        # references
        citations = js['citations']
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
        description = js['description']['DRAWING_DESC']['plain'].rstrip() + "\n" + js['description']['BRIEF_SUMMARY'][
            'plain'].rstrip() + "\n" + js['description']['DETAILED_DESC']['plain'].rstrip()

        process_inventors(inventors)
        process_assignees(assignees)
        process_citations(citations)
        break
    break
