__author__ = 'hzhu'

import os, urllib.request, urllib3, re

#meta-info
toc = "/content/21/6.toc"
base = "http://jamia.bmj.com"
folderbase = "c:/Users/hzhu/JAMIA/"
if not os.path.exists(folderbase):
    os.mkdir(folderbase)
listPdf = []
listToc = []

#prepare for connection
http = urllib3.PoolManager()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

#Page connection
def getContentList():
    test = http.request('GET',base+toc,None,headers)
    regPdf = re.compile(r'</span><a href="(/content/.{12,40}pdf)\+html')
    regToc = re.compile(r'"(/content/.{1,12}toc)"')
    listPdf = re.findall(regPdf,str(test.data))
    listToc = re.findall(regToc, str(test.data))

#Download Content
def getContent():
    content = []



# print(test.data)
print(listToc)