import re
import json
from aliexpress.scraper import AliexpressScraper


class AliexpressTools:
    @classmethod
    def is_valid_url(cls, url):
        url_pattern = re.compile('http[s]?://([a-z]+)?\.?aliexpress\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        if re.match(pattern=url_pattern, string=url):
            return True
        else:
            return False

    @classmethod
    def scrape(cls, url):
        try:
            data = AliexpressScraper(url).to_dict()
            response = json.dumps(data)
            print(response)
            status = 200
        except:
            response = json.dumps({'Error': f'Cannot scrape this Aliexpress url {url}'})
            print(response)
            status = 409

        return response, status
