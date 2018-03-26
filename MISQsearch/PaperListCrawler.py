from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle
import re

# navigate to the an issue for a specific volume
# if it has research commentaries in it, then print it out or store it to a file
# Move onto the next issue in the volume

volume = 42
special_issue = [6, 30]
current_issue = 1

i = 1
j = 1
urllist = []

for v in range(1, volume):
    for i in range(1, 5):
        urllist.append("https://misq.org/contents-{0:02d}-{1}/".format(v, i))
    if v in special_issue:
        urllist.append("https://misq.org/contents-{0:02d}-SI/".format(v))
for i in range(1, current_issue + 1):
    urllist.append("https://misq.org/contents-{0:02d}-{1}/".format(volume, i))

paperURL = []
for url in urllist:
    print("Reading URL {0}".format(url))
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    body = soup.find("div", {"id": "main"})
    l = body.find_all("a")
    for a in l:
        paperURL.append(a['href'])
    print(len(paperURL))

f = open("MISQ_paper_list.pkl", "wb")
pickle.dump(paperURL, f)
