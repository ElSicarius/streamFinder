

import sources.consts as consts

from urllib import error
from googlesearch import search
import requests
import bs4
import re
import time

from urllib.parse import unquote

def duckduckgo_this(keywords, max_results=15):
    url = 'https://duckduckgo.com/html/?q='

    url = url+keywords.replace(" ","+")

    res = requests.get(url, headers={"User-Agent":"curl"})
    doc = bs4.BeautifulSoup(res.text, 'html.parser')

    results = doc.find_all("a", class_="result__a")
    res = set()
    for result in results:
        res.add( unquote(result["href"].split("uddg=")[1].split("&rut=")[0] ) )
        time.sleep(0.1)

    return res

def google_this(what, row, n, offset=0, SafeSearch="off", lang="fr", tld="fr"):
    print(f"Searching for {what}")
    try:
        res = search(what, tld=tld, num=row, start=offset, stop=n, pause=5, lang=lang, safe=SafeSearch, extra_params={'filter': '0'})
    except error.HTTPError:
        print("Google cooldown... you need a to change your IP")
    return res


def is_not_garbage(url):
    if any([True for element in consts.black_list_websites if element in url ]):
        return False
    return True


def url_threading(url):
    if url == "":
        return set()
    #print(f"requesting {url!s}")
    try:
        content = requests.get(url)
    except:
        return set()
    res = set()
    doc = bs4.BeautifulSoup(content.text, 'html.parser')
    ifr = doc.find_all("iframe")
    for iframe in ifr:
        for url in re.findall(consts.reg_url, iframe.__str__()):
            res.add(url)
    return res
