from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from NIPScrawler.src.ParsePage import ParsePage

browser = webdriver.PhantomJS()

root = 'http://papers.nips.cc'

number = 27
year = 2014

browser.get('http://papers.nips.cc/book/advances-in-neural-information-processing-systems-'
            + str(number) + '-' + str(year))
soup = BeautifulSoup(browser.page_source, 'lxml')
anchor_list = soup.find_all('a')
paper_link = [x.get('href') for x in anchor_list if "paper" in x.get('href')]

test = ParsePage(urljoin(root, paper_link[0]), r'C:/Users/zhuhy/Documents/NIPS/paper', year)
test.parse_page()

browser.quit()
