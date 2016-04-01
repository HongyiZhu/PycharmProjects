from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from NIPScrawler.src.ViewPage import ViewPage

browser = webdriver.PhantomJS()

root = 'http://papers.nips.cc'

browser.get('http://papers.nips.cc/book/advances-in-neural-information-processing-systems-27-2014')
soup = BeautifulSoup(browser.page_source, 'lxml')
anchor_list = soup.find_all('a')
paper_link = [x.get('href') for x in anchor_list if "paper" in x.get('href')]

test = ViewPage(urljoin(root, paper_link[0]), r'D:/NIPS/paper')
test.parse_page()

browser.quit()
