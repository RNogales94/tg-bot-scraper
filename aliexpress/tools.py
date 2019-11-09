import re
import json
from aliexpress.scraper import AliexpressScraper
from utils.url_utils import is_aliexpress


class AliexpressTools:
    @classmethod
    def is_valid_url(cls, url):
        return is_aliexpress(url)

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
