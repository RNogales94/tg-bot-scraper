# import re
# import json
# from utils.url_utils import expand_url, is_amazon
#
# from amazon.scraper import AmazonScraper
#
#
# class AmazonTools:
#     @classmethod
#     def is_valid_url(cls, url):
#         return is_amazon(url)
#
#     @classmethod
#     def modify_url(cls, url, tag):
#         url = expand_url(url)
#         tag_pattern = r'tag=[^&]+'
#
#         if re.search(tag_pattern, url):
#             print('Real modification')
#             url = re.sub(tag_pattern, 'tag=' + tag, url)
#         else:
#             if '?' in url:
#                 url = url + '&tag=' + tag
#             else:
#                 url = url + '?tag=' + tag
#         return url
#
#     @classmethod
#     def scrape(cls, url):
#         try:
#             data = AmazonScraper().scrape(url).to_dict()
#             response = json.dumps(data)
#             print(response)
#             status = 200
#         except Exception as e:
#             print(e)
#             response = json.dumps({'Error': f'Cannot scrape this Amazon url {url}'})
#             print(response)
#             status = 409
#
#         return response, status
