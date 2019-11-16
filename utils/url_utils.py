import re
import requests
import urllib


def capture_urls(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


def get_ASIN(url):
    url = expand_url(url)
    if is_amazon(url):
        try:
            asin = re.match(r'(.*)\/([A-Z0-9]{10})((\/)?(.*))?', url).groups()[1]
            return asin
        except AttributeError:
            return None
    else:
        return None


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


def is_amazon(url):
    if url is None:
        return False
    try:
        url = expand_url(url)
    except requests.exceptions.ConnectionError:
        print(f'Exception: Connection refused {url}')
        return False
    return 'amazon' in urllib.parse.urlparse(url).hostname
