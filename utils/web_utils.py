import requests
import re


def expand_url(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


def is_amazon(url):
    url_pattern = re.compile(
        'http[s]?://(www.)?amazon\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if re.match(pattern=url_pattern, string=url):
        return True
    else:
        return False


def is_aliexpress(url):
    url_pattern = re.compile(
        'http[s]?://(m\.)?([a-z]+)?\.?aliexpress\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if re.match(pattern=url_pattern, string=url):
        return True
    else:
        return False