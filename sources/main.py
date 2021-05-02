
from .argsparser import get_arguments
from .utils import google_this, is_not_garbage, url_threading, duckduckgo_this

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, CancelledError, thread

def main() -> None:
    args = get_arguments()

    title = args.title
    search = title + " streaming vf"
    urls_temp = set()
    
    urls = google_this(search , 1, 15)
    for res in urls:
        urls_temp.add(res)

    urls_temp |= duckduckgo_this(search)
    urls = set()
    for url in urls_temp:
        if is_not_garbage(url):
            urls.add(url)
    print(f"Found {len(urls)} urls")
    executor = ThreadPoolExecutor(max_workers=5)
    futures = set()
    futures.update({ executor.submit(url_threading, url) for url in urls})
    final_urls = set()
    while futures:
        done, futures = wait(futures, return_when=FIRST_COMPLETED)
        for futu in done:
            for url in futu.result():
                if is_not_garbage(url) and not url in final_urls:
                    final_urls.add(url)
                    print(f"{title=!s}, link: \033[1;35;40m##### {url}\033[0m")
    return
