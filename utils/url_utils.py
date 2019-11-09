import re
import requests
import urllib


def capture_urls(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


def contain_urls(text):
    return len(capture_urls(text)) > 0


def expand_url(url):
    session = requests.Session()  # so connections are recycled
    try:
        resp = session.head(url, allow_redirects=True)
    except requests.exceptions.MissingSchema as e:
        print(f'----> MissingSchema Error {e}')
        print(f'URL {url} cannot be expanded, probably this is not a valid URL, return None')
        return url
    except requests.exceptions.ConnectionError as e:
        print(f'----> Connection Error {e}')
        print(f'URL {url} cannot be expanded, probably this is not a valid URL, return None')
        return url
    return resp.url


def get_app_name(scraper_address):
    return urllib.parse.urlparse(scraper_address).hostname.split('.')[0]


def is_aliexpress(url):
    if url is None:
        return False
    try:
        url = expand_url(url)
    except requests.exceptions.ConnectionError:
        print(f'Exception: Connection refused {url}')
        return False
    return 'aliexpress' in urllib.parse.urlparse(url).hostname


def is_amazon(url):
    if url is None:
        return False
    try:
        url = expand_url(url)
    except requests.exceptions.ConnectionError:
        print(f'Exception: Connection refused {url}')
        return False
    return 'amazon' in urllib.parse.urlparse(url).hostname
