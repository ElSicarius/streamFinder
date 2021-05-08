
from sources.argsparser import get_arguments
from sources.utils import google_this, is_not_garbage, url_threading, duckduckgo_this
from sources.utils import get_external_urls
import sources.consts as consts

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, CancelledError, thread


FINAL_URLS_GARB = set()
FINAL_URLS_EXT = set()

def find_url_on_shitty_web(urls: set) -> None:
    executor = ThreadPoolExecutor(max_workers=10)
    futures = set()
    futures.update({ executor.submit(url_threading, url) for url in urls})
    global FINAL_URLS_GARB
    while futures:
        done, futures = wait(futures, return_when=FIRST_COMPLETED)
        for futu in done:
            for url in futu.result():
                if is_not_garbage(url) and not url in FINAL_URLS_GARB:
                    FINAL_URLS_GARB.add(url)

def print_urls(title: str, links:list, color: int=1) -> None:
    # color -> 1 = pink; 2 = green
    color = consts.purple if color == 1 else consts.green
    for url in sorted(list(links)):
        print(f"\033[K{color}##### {url}\033[0m")


def search_movie(title: str, sources: str="DE", lang: str="fr", nbRes=30) -> tuple:
    urls_global = set()
    global FINAL_URLS_EXT
    global FINAL_URLS_GARB
    search = f"{title} streaming {lang}"
    if "G" in sources:
        urls = google_this(search , 1, nbRes)
        for res in urls:
            urls_global.add(res)

    if "D" in sources:
        urls_global |= duckduckgo_this(search, max_results=nbRes)

    urls = set()
    for url in urls_global:
        if is_not_garbage(url):
            urls.add(url)
    print(f"Found {len(urls)} urls")
    find_url_on_shitty_web(urls)

    if "E" in sources:
        FINAL_URLS_EXT |= get_external_urls(title)

    fin_1, fin_2 = FINAL_URLS_GARB, FINAL_URLS_EXT
    FINAL_URLS_GARB, FINAL_URLS_EXT = set(), set()
    return fin_1, fin_2

def main() -> None:
    args = get_arguments()

    title = args.title
    lang = args.lang
    numberResults = args.numberResults
    if len(lang) > 2:
        exit("Lang should be 2 letters (eg: fr or en)")
    search = f"{title} streaming {lang}"
    sources = args.sources
    print(f"Using defined sources: {sources}")

    search_movie(title, sources=sources, lang=lang, nbRes=numberResults)
    print_urls(title, FINAL_URLS_GARB, color=1)
    print_urls(title, FINAL_URLS_EXT, color=2)

    return
