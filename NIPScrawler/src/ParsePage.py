from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
from NIPScrawler.src.Database_IO import DatabaseConnection
import re
import time
import random
import os

root = 'http://papers.nips.cc'


def get_title(page):
    subtitle = page.find('h2', {'class': 'subtitle'}).text
    return subtitle


def get_abstract(page):
    abstract = page.find('p', {'class': 'abstract'}).text
    return abstract


def get_author(page):
    ul = page.find('ul', {'class': 'authors'})
    author_dict = {}
    author_list = ul.findAll('a')
    for anchor in author_list:
        author_dict[anchor.text] = urljoin(root, anchor.get('href'))
    return author_dict


def get_id(url):
    reg = re.compile(r'paper/(\d+)-\w')
    paper_id = reg.findall(url)
    return paper_id


class ParsePage:
    def __init__(self, url, folder, year):
        self.year = year
        self.url = url
        self.folder = folder
        self.browser = webdriver.PhantomJS()
        self.browser.get(self.url)
        self.source = self.browser.page_source
        self.id = get_id(url)
        self.db = DatabaseConnection()

    def parse_page(self):
        page = BeautifulSoup(self.source, 'lxml')
        title = get_title(page)
        authors = get_author(page)
        abstract = get_abstract(page)
        event_type = self.get_event_type()
        local_filepath = self.download_file(page)
        self.db.insert(title=title,
                       authors=authors,
                       abstract=abstract,
                       event_type=event_type,
                       year=self.year,
                       local_filepath=local_filepath)
        self.db.close()

    def get_event_type(self):
        reg = re.compile(r'Conference Event Type: (.*)</h3>')
        conference_event_type = reg.findall(self.source)[0]
        return conference_event_type

    def download_file(self, page):
        pdf_href = page.find('a', href=True, text='[PDF]')['href']
        filename = os.path.join(self.folder, pdf_href.split('/')[2])
        time.sleep(random.randrange(10))
        urlretrieve(urljoin(root, pdf_href), filename)
        self.browser.close()
        return filename.replace('\\', '/')
