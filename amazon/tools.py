import re
import requests


def expand_url(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


class AmazonTools:
    @staticmethod
    def is_amazon_url(text):
        url_pattern = re.compile('http[s]?://(www.)?amazon\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        if re.match(pattern=url_pattern, string=text):
            return True
        else:
            return False

    @staticmethod
    def modify_url(url, tag):
        url = expand_url(url)
        tag_pattern = r'tag=[^&]+'

        if re.search(tag_pattern, url):
            print('Real modification')
            url = re.sub(tag_pattern, 'tag=' + tag, url)
        else:
            if '?' in url:
                url = url + '&tag=' + tag
            else:
                url = url + '?tag=' + tag
        return url

