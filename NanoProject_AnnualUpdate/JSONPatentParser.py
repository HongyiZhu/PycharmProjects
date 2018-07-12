from datetime import datetime
from DBConnection import DBConnection
import os
import re
import json


def process_inventors(patentID, inventors, cur):
    for i, inv in enumerate(inventors):
        fName = inv['name']['firstName'].rstrip() if inv['name']['firstName'] != "" else "-"
        mName = inv['name']['middleName'].rstrip() if inv['name']['middleName'] != "" else "-"
        lName = inv['name']['lastName'].rstrip() if inv['name']['lastName'] != "" else "-"
        try:
            city = inv['address']['city'].rstrip() if inv['address']['city'] != "" else "-"
        except KeyError:
            city = "-"
        try:
            state = inv['address']['state'].rstrip() if inv['address']['state'] != "" else "-"
        except KeyError:
            state = "-"
        try:
            country = inv['address']['country'].rstrip() if inv['address']['country'] != "" else "-"
        except KeyError:
            country = "-"
        rank = str(i)
        # print("{} {}, {}, {}, {}".format(fName, lName, city, state, country))
        cur.execute("USP_InsertInventors ?,?,?,?,?,?,?,?", [patentID, lName, mName, fName, city, state, country, rank])
        cur.commit()


def process_assignees(patentID, assignees, cur):
    for i, assi in enumerate(assignees):
        name = assi['name']['raw'].rstrip()
        try:
            city = assi['address']['city'].rstrip() if assi['address']['city'] != "" else "-"
        except KeyError:
            city = "-"
        try:
            state = assi['address']['state'].rstrip() if assi['address']['state'] != "" else "-"
        except KeyError:
            state = "-"
        try:
            country = assi['address']['country'].rstrip() if assi['address']['country'] != "" else "-"
        except KeyError:
            country = "-"
        rank = str(i)
        cur.execute("USP_InsertAssignees ?,?,?,?,?,?", [patentID, name, city, state, country, rank])
        cur.commit()


def process_citations(patentID, citations, cur):
    for c in citations:
        if c['text'][:2] == "US":
            cite = getPureID(c['text'])
            cur.execute("USP_InsertCitations ?,?,?,?", [patentID, cite, "", ""])
            cur.commit()


def getPureID(s):
    return re.findall(r'([a-zA-Z]*\d+/*\d*)([a-zA-Z]\d)*', s[2:])[0][0]


def extract_claim_id(js):
    try:
        return int(js['id'].split("-")[-1])
    except KeyError:
        return 0


conn = DBConnection()
conn.autocommit = True
cur = conn.getCursor()
count = 0
startfrom = 1

for root, dirs, files in os.walk("C:/Users/zhuhy/Desktop/Patent2017"):
    # for root, dirs, files in os.walk("C:/Users/Hongyi/Desktop/Patent2017"):
    for name in files:
        if count < startfrom - 1:
            count += 1
            continue
        else:
            filepath = os.path.join(root, name)
            js = json.load(open(filepath, encoding="utf8"))
            # patentId
            patentID = getPureID(js['documentId'])
            applType = patentID[0]
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
            description = ""
            try:
                description += js['description']['DRAWING_DESC']['plain'].rstrip() + "\n"
            except KeyError:
                pass
            try:
                description += js['description']['BRIEF_SUMMARY']['plain'].rstrip() + "\n"
            except KeyError:
                pass
            try:
                description += js['description']['DETAILED_DESC']['plain'].rstrip()
            except KeyError:
                pass

            # try:
            cur.execute("USP_InsertPatents ?,?,?,?,?,?,?,?,?,?,?,?",
                        [patentID, title, abstract, claim, description, issueDate, fileDate, applNo, applType, attorney,
                         primary_examiner, assistant_examiner])
            cur.commit()
            process_inventors(patentID, inventors, cur)
            process_assignees(patentID, assignees, cur)
            process_citations(patentID, citations, cur)
            # except pyodbc.IntegrityError:
            #     pass
            count += 1
            print("Finished {}/39874 Patents".format(str(count)))
    break

cur.close()
conn.close()
