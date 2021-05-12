
from sources.argsparser import get_arguments
from sources.utils import google_this, is_garbage, url_threading, duckduckgo_this
from sources.utils import get_external_urls
import sources.consts as consts

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, CancelledError, thread


def find_url_on_shitty_web(urls: set) -> set:
    found_urls = set()
    executor = ThreadPoolExecutor(max_workers=10)
    futures = set()
    futures.update({ executor.submit(url_threading, url) for url in urls})

    while futures:
        done, futures = wait(futures, return_when=FIRST_COMPLETED)
        for futu in done:
            for url in futu.result():
                if not url in found_urls and not is_garbage(url):
                    found_urls.add(url.replace("&amp;", "&"))
    return found_urls


def print_urls(title: str, links:list, color: int=1) -> None:
    # color -> 1 = pink; 2 = green
    if color == 1:
        color = consts.purple
    elif color == 2:
        color = consts.green
    elif color == 3:
        color = consts.dark_blue
    else:
        color = f"much color {color} yes."
    for url in sorted(list(links)):
        print(f"\033[K{color}##### {url}\033[0m")


def search_movie(title: str, sources: str="DE", lang: str="vf", nbRes=30) -> tuple:
    final_links_ext = set()
    urls_not_sorted = set()

    search_ggl = f"intext:\"{title}\"+\"streaming\" {lang}"
    search_ddg = f"{title} streaming {lang}"

    if "G" in sources:
        try:
            for res in google_this(search_ggl, nbRes):
                urls_not_sorted.add(res)
        except Exception as e:
            print(f"{e} -> Network error... do you need a to change your IP ?")
    if "D" in sources:
        try:
            urls_not_sorted |= duckduckgo_this(search_ddg, max_results=nbRes)
        except Exception as e:
            print(f"{e} -> Network error... do you need a to change your IP ?")
    if "E" in sources:
        final_links_ext |= get_external_urls(title)
    urls = set(filter(None, [url for url in urls_not_sorted if not is_garbage(url)]))

    if len(urls)>0:
        print(f"Found {len(urls)} urls")
    else:
        print(f"{consts.red}Could not find any urls ! Your IP is probably blacklisted from search engines.\033[0m")

    final_links_garb = find_url_on_shitty_web(urls)

    # cleaning sets:
    final_links_garb = set(filter(None, list(final_links_garb)))
    final_links_ext  = set(filter(None, list(final_links_ext)))

    return final_links_garb, final_links_ext, urls

def main() -> None:
    args = get_arguments()

    title = args.title
    lang = args.lang
    numberResults = args.numberResults
    if len(lang) < 2:
        exit("Lang should be 2 letters (eg: vf or vo)")
    sources = args.sources
    print(f"Using defined sources: {sources}")

    urls_garb, urls_ext, streaming_websites = search_movie(title, sources=sources, lang=lang, nbRes=numberResults)
    if len(urls_garb) > 0:
        print(f"Raw Hosted streaming videos:")
    print_urls(title, urls_garb, color=1)
    if len(urls_ext) > 0:
        print(f"External links from plugins:")
    print_urls(title, urls_ext, color=2)
    if len(streaming_websites) > 0:
        print(f"Raw streaming websites:")
    print_urls(title, streaming_websites, color=3)

    return
