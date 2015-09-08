__author__ = 'Hongyi'

import re
import time
import socket
import socks
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup


def next_page(soup):
    """
    Generate link to the next page
    :param soup: The HTML page
    :return: The URL to next page
    """
    query_base = "http://patft.uspto.gov/netacgi/nph-Parser?"

    # Retrieve the right form, break if found
    for f in soup.find_all('form'):
        if "Next" in f.find_all('input')[-1]['name']:
            form = f
            break

    # find all the parameters and generate the url
    input_list = form.find_all('input')
    str_list = [(x['name'] + "=" + x['value']).replace("/", "%2F").replace("(", "%28").replace(")", "%29")\
                       .replace(" ", "+").replace("\"", "%22").replace("$", "%24") for x in input_list]

    query_str = "&".join(str_list)
    return query_base + query_str


def analyze(soup, patent_list):
    """
    Analyze the patent page and extract the patent number
    :param soup: HTML page
    :param patent_list: patent list of the keyword
    :return:
    """
    tr_list = soup.find_all('table')[1].find_all('tr')[1:]
    for tr in tr_list:
        patent_list.append(tr.find_all('td')[1].text)


def analyze_url(url):
    """
    Analyze the query page and gather patent information
    :param url: the query link
    :return: pat_list: a list of patents containing keyword
    """
    # routing through tor network
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket

    page = urlopen(url)
    soup = BeautifulSoup(page)
    totalnumber = 0
    patent_list = []

    # get general number of patents
    m = re.search(": (\\d+) patents", soup.text)
    if m is not None:
        totalnumber = int(m.group(1))
    print("%s patents in total" % str(totalnumber))

    # no result => return a null list
    if totalnumber == 0:
        return patent_list
    # else parse through the webpage
    else:
        pagenum = 1

        # analyze the table elements
        print("Analyzing page %s" % str(pagenum))
        analyze(soup, patent_list)

        # flip to new pages if needed
        while pagenum * 50 < totalnumber:
            pagenum += 1
            # get url to nex page
            newurl = next_page(soup)

            # analyze pages one by one
            time.sleep(1)
            page = urlopen(newurl)
            soup = BeautifulSoup(page)
            print("Analyzing page %s" % str(pagenum))
            analyze(soup, patent_list)

    # return after traverse
    return patent_list

def get_amount(url):
    """
    Analyze the query page and gather patent information
    :param url: the query link
    :return: number of total patents
    """
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket

    page = urlopen(url)
    soup = BeautifulSoup(page)
    totalnumber = 0

    # get general number of patents
    m = re.search(": (\\d+) patents", soup.text)
    if m is not None:
        totalnumber = int(m.group(1))
    
    return(totalnumber)
