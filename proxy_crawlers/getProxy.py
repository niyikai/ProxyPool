import requests
import bs4
import re
from lxml import etree
#
# def getHtmlTree(url, **kwargs):
#     html = requests.get(url=url).content
#     return etree.HTML(html)
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"}

def freeProxyFirst():
    url = "http://www.xicidaili.com"
    html = requests.get(url, headers = headers).content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    proxylist = [proxy.find_all("td")[1:3] for proxy in soup.find_all("tr") if len(proxy)>0]
    for p in proxylist:
        if len(p)<2: continue
        print p[0].text, p[1].text

if __name__ == '__main__':
    freeProxyFirst()