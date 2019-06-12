import re
import json
from utils.web_utils import expand_url

from amazon.scraper import AmazonScraper


class AmazonTools:
    @classmethod
    def is_valid_url(cls, url):
        url_pattern = re.compile('http[s]?://(www.)?amazon\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        if re.match(pattern=url_pattern, string=url):
            return True
        else:
            return False

    @classmethod
    def modify_url(cls, url, tag):
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

    @classmethod
    def scrape(cls, url):
        try:
            data = AmazonScraper(url).to_dict()
            response = json.dumps(data)
            print(response)
            status = 200
        except:
            response = json.dumps({'Error': f'Cannot scrape this Amazon url {url}'})
            print(response)
            status = 409

        return response, status
