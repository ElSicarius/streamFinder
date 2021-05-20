

#import sources.consts as consts

from urllib import error
from googlesearch import search
import requests
import bs4
import base64
import re
import os
import sys
import random
import importlib

from urllib.parse import unquote
import consts as consts


def get_proxies_list(num_pages: int=3, save=None) -> dict:
    url_for_proxies = "http://free-proxy.cz/fr/proxylist/country/all/all/ping/all/"
    head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
    content = list()
    for page in range(1,num_pages):
        try:
            content.append(requests.get(url_for_proxies+str(page), headers=head).text)
        except:
            print("Couldn't connect to the proxies websites, quit();")
            return dict()

    for page in content:
        doc = bs4.BeautifulSoup(page, "html.parser")
        try:
            c = doc.find_all("table", id="proxy_list")[0]
        except IndexError:
            print("Could not find table in proxy page... bad internet ?")
            continue
        col = c.find_all("td")
        col = [ele for ele in col]
        offset = 0
        item = dict()
        final_list = dict()

        for i, c in enumerate(col):
            if "adsbygoogle" in c.__str__():
                # get rid of the erf ads
                offset -= 1
                continue
            i = (i + offset) % 11 # 11 rows to get
            if i == 0:
                if len(item) > 0:
                    final_list.update({item["ip"]: item})
                item = dict({"ip":"0.0.0.0",
                            "proto": "http",
                            "port": "80"})
                item["ip"] = re.findall(r'decode\("([A-Za-z\d\/=]+)"\)', c.__str__())[0]
                try:
                    item["ip"] = base64.b64decode(item["ip"]).decode("utf-8")
                except:
                    print("bs64 error")
            elif i == 1:
                item["port"] = c.text
            elif i == 2:
                item["proto"] = c.text
            elif i == 3:
                item["country"] = c.text
            elif i == 6:
                item["level"] = c.text
            elif i == 7:
                item["speed"] = c.text
            elif i == 8:
                item["load"] = c.text
            elif i == 9:
                item["time"] = c.text
            else:
                continue
        if save:
            try:
                with open("sources/proxies.txt", "w") as f:
                    f.write(json.dumps(final_list))
            except:
                print("Error writting proxies list")
        consts.PROXY = final_list
        return final_list

def select_proxies() -> None:
    proxies = consts.PROXY
    ip = random.choice([n for n,_ in proxies.items()])
    consts.PROXIES = {proxies[ip]["proto"]: ip}


def duckduckgo_this(keywords: str, max_results: int=15) -> set:
    print(f"\033[1;35;40mSearching {keywords!r} on duckduckgo\033[0m")
    print(f"Using Proxy: {consts.PROXIES.items()}")
    url = 'https://duckduckgo.com/html/?q='
    url = url+keywords.replace(" ","+")
    res = requests.get(url, headers={"User-Agent":"curl"}, proxies=consts.PROXIES)
    doc = bs4.BeautifulSoup(res.text, 'html.parser')
    results = doc.find_all("a", class_="result__a")
    res = set()
    for result in results:
        if len(res) < max_results:
            res.add( unquote(result["href"].split("uddg=")[1].split("&rut=")[0] ) )
        else:
            break
    return res

def google_this(what: str, stop: int, lang="fr", tld="com"):
    print(f"\033[1;35;40mSearching {what!r} on google\033[0m")
    res = search(what, tld=tld, stop=stop, lang=lang, safe="off", pause=2, extra_params={'filter': '0'}, verify_ssl=False)
    return res

def is_garbage(url: str) -> bool:
    for element in consts.black_list_websites:
        if element in url:
            return True
    return False

def get_external_urls(title:str) -> set:
    links = set()
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(1, os.path.join(os.getcwd(), "sources/plugin"))
    for file in os.listdir(os.path.join(os.getcwd(), "sources/plugin")):
        if not re.match(r"^[a-zA-Z\d_]+\.py$", file):
            continue
        name = file[:-3]
        print(f"\033[K\033[1;36mRunning module {name}\033[0m")
        module = importlib.import_module(name)
        links |= module.Movie().get_movie(title)
    sys.path.insert(1, os.path.join(os.getcwd(), ""))
    return links

def url_threading(url: str) -> set:
    if url == "":
        return set()
    print(f"\033[KTrying to find iframe on {url!s}", end="\r")
    try:
        content = requests.get(url, timeout=5)
    except:
        return set()
    res = set()
    doc = bs4.BeautifulSoup(content.text, 'html.parser')
    ifr = doc.find_all("iframe")
    for iframe in ifr:
        for url in re.findall(consts.reg_url, iframe.__str__()):
            res.add(url)
    return res
