from bs4 import BeautifulSoup
from urllib.request import urlopen
from MISQsearch.dbconnection import databaseWrapper
import pickle

db = databaseWrapper()
cur = db.get_cursor()

f = open("MISQ_paper_list.pkl", "rb")
paperURL = pickle.load(f)
paperURL = [x for x in paperURL if ".pdf" not in x]

for i in range(1217, len(paperURL)):
    paper = paperURL[i]
    print("Reading URL {0}".format(paper))
    response = urlopen(paper)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    title = db.conn.escape(soup.find("h3", {"class": "product-name"}).text.strip())
    abstract = db.conn.escape(soup.find("div", {"class": "product-specs"}).text.strip().split("\n")[0])

    data = soup.find_all("td", {"class": "data"})

    author = db.conn.escape(data[0].text.strip())
    year = data[1].text.strip()
    volume = data[2].text.strip()
    issue = data[3].text.strip()
    keyword = db.conn.escape(data[4].text.strip())
    if len(data) > 5:
        pg = data[5].text.strip().split(";")[0]
        doi = data[5].text.strip().split("DOI: ")[1].strip() if len(data[5].text.strip().split("DOI: ")) > 1 else ""
    else:
        pg = ""
        doi = ""

    sql = "INSERT INTO `paper` (Title, Abstract, Author, Year, Volume, Issue, Keyword, Page, DOI, URL) VALUES (%s, %s, %s, '%s', '%s', '%s', %s, '%s', '%s', '%s')" % (title, abstract, author, year, volume, issue, keyword, pg, doi, db.conn.escape(paper))
    print(sql)
    cur.execute(sql)
