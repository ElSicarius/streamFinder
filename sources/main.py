
from .argsparser import get_arguments
from .utils import google_this, is_not_garbage, url_threading, duckduckgo_this
from .utils import get_external_urls

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, CancelledError, thread


FINAL_URLS = set()

def find_url_on_shitty_web(urls: set) -> None:
    executor = ThreadPoolExecutor(max_workers=10)
    futures = set()
    futures.update({ executor.submit(url_threading, url) for url in urls})

    while futures:
        done, futures = wait(futures, return_when=FIRST_COMPLETED)
        for futu in done:
            for url in futu.result():
                if is_not_garbage(url) and not url in FINAL_URLS:
                    FINAL_URLS.add(url)

def print_urls(title: str) -> None:
    for url in FINAL_URLS:
        print(f"{title=!s}, link: \033[1;35;40m##### {url}\033[0m")

def main() -> None:
    args = get_arguments()

    title = args.title
    lang = args.lang
    if len(lang) > 2:
        exit("Lang should be 2 letters (eg: fr or en)")
    search = f"{title} streaming {lang}"
    sources = args.sources
    print(f"Using defined sources: {sources}")
    urls_global = set()

    if "G" in sources:
        urls = google_this(search , 1, 15, lang=lang)
        for res in urls:
            urls_global.add(res)

    if "D" in sources:
        urls_global |= duckduckgo_this(search)

    urls = set()
    for url in urls_global:
        if is_not_garbage(url):
            urls.add(url)
    print(f"Found {len(urls)} urls")
    find_url_on_shitty_web(urls)
    if "E" in sources:
        global FINAL_URLS
        FINAL_URLS |= get_external_urls(title)
    print_urls(title)






    return
