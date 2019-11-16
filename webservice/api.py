from flask import Flask, Response, request
from flask_cors import CORS
from utils.url_utils import is_amazon, expand_url
from amazon.scraper import AmazonScraper

import json

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)


def is_valid_url(url):
    return is_amazon(url)


def scrape_url(url):
    amazon_scraper = AmazonScraper()

    print(url)
    if url is None:
        print('Parameter url not found: 400 Error')
        response = json.dumps({'Error': 'Parameter url not found'})
        status = 400
        return response, status

    if url == '':
        print('url empty')
        response = json.dumps({'Error': 'url is empty'})
        status = 400
        return response, status

    url = expand_url(url)
    if '/offer-listing/' in url:
        response = json.dumps({'Error': f'XBot - This link {url} contains multiple products, please choose only one'})
        status = 400
        return response, status

    if is_valid_url(url):
        try:
            data = amazon_scraper.scrape(url)
            response = json.dumps(data)
            status = 200
        except Exception as e:
            response = json.dumps({'Error': f'{e}'})
            print(response)
            status = 500
    # elif AliexpressTools.is_valid_url(url):
    #     response, status = AliexpressTools.scrape(url)
    else:
        response = json.dumps({'Error': f'{url} is not valid Amazon/Aliexpress product URL'})
        print(response)
        status = 412

    return response, status


@xbot_webservice.route("/")
def index():
    return 'xbot01'


@xbot_webservice.route("/ping")
def ping():
    return Response(json.dump({'Message': 'Scraper instance'}), status=200, mimetype='application/json')


@xbot_webservice.route("/dev/myip")
def myip():
    return request.remote_addr


@xbot_webservice.route("/api/scrape", methods=['POST'])
def scrape():

    print('-------------------------------------------------')
    print("Scraping")
    if request.json is None:
        error = {"Error": "Missing url"}
        return Response(json.dumps(error), status=400, mimetype='application/json')

    url = request.json.get('url', None)
    response, status = scrape_url(url)

    if status == 200:
        if json.loads(response)['is_captcha']:
            error = {"Error": "Amazon is blocking the bot with a CAPTCHA, try again later"}
            return Response(json.dumps(error), status=503, mimetype='application/json')

    print('*************************************************')
    return Response(response, status=status, mimetype='application/json')


if __name__ == '__main__':
    xbot_webservice.run(debug=True)


#
# # Test
# test = False
# if test:
#     ali_urls = [
#      'http://s.click.aliexpress.com/e/cmKQ0LEo',
#      'http://s.click.aliexpress.com/e/b4dj7tZA',
#      'http://s.click.aliexpress.com/e/bSNeQdbK',
#      'http://s.click.aliexpress.com/e/cODenJTK',
#      'http://s.click.aliexpress.com/e/fo3wXms',
#      'http://s.click.aliexpress.com/e/ff3wCU0',
#      'http://s.click.aliexpress.com/e/IptPVuM',
#      'http://s.click.aliexpress.com/e/bKU0YC0s',
#      'http://s.click.aliexpress.com/e/e0tM9Gy',
#      'http://s.click.aliexpress.com/e/NK8ProG',
#      'http://s.click.aliexpress.com/e/bCCZGVI0',
#      'http://s.click.aliexpress.com/e/TbQAfrK',
#      'http://s.click.aliexpress.com/e/cmKQ0LEo',
#      'http://s.click.aliexpress.com/e/cdcN96Y',
#      'http://s.click.aliexpress.com/e/bALHPYFq',
#      'http://s.click.aliexpress.com/e/bSYmNaFA',
#      'http://s.click.aliexpress.com/e/b8a71yYo',
#      'http://s.click.aliexpress.com/e/i7yUpLE',
#      'http://s.click.aliexpress.com/e/c3Ad6Blq',
#      'http://s.click.aliexpress.com/e/Yzt0YjA',
#      'http://s.click.aliexpress.com/e/SBhzjyy',
#      'http://s.click.aliexpress.com/e/bypOmruM',
#      'http://s.click.aliexpress.com/e/b5H42QBq',
#      'http://s.click.aliexpress.com/e/nkaA3rE',
#      'http://s.click.aliexpress.com/e/bAMSokla',
#      'http://s.click.aliexpress.com/e/gREJ2ne',
#      'http://s.click.aliexpress.com/e/c47PIFxS',
#      'http://s.click.aliexpress.com/e/ckrkSLBE',
#      'http://s.click.aliexpress.com/e/cfu1GiaG',
#      'http://s.click.aliexpress.com/e/ihX7NHW',
#      'http://s.click.aliexpress.com/e/bzHIKg0',
#      'http://s.click.aliexpress.com/e/fYWI86M',
#      'http://s.click.aliexpress.com/e/bBuI2d9O',
#      'http://s.click.aliexpress.com/e/cWBBzVnK',
#      'http://s.click.aliexpress.com/e/bEUwmKPO',
#      'http://s.click.aliexpress.com/e/b1mo3doM',
#      'http://s.click.aliexpress.com/e/24tkFTS',
#      'http://s.click.aliexpress.com/e/c3whEN0c',
#      'http://s.click.aliexpress.com/e/cdcN96Y',
#      'http://s.click.aliexpress.com/e/bALHPYFq',
#      'http://s.click.aliexpress.com/e/bSYmNaFA',
#      'http://s.click.aliexpress.com/e/b8a71yYo',
#      'http://s.click.aliexpress.com/e/i7yUpLE',
#      'http://s.click.aliexpress.com/e/biLR0IAk',
#      'http://s.click.aliexpress.com/e/c3Ad6Blq',
#      'http://s.click.aliexpress.com/e/Yzt0YjA',
#      'http://s.click.aliexpress.com/e/cC5LBGSG',
#      'http://s.click.aliexpress.com/e/SBhzjyy',
#      'http://s.click.aliexpress.com/e/b5H42QBq',
#      'http://s.click.aliexpress.com/e/cNKj8U0u',
#      'http://s.click.aliexpress.com/e/nkaA3rE',
#      'http://s.click.aliexpress.com/e/b1ZNqSyC',
#      'http://s.click.aliexpress.com/e/bAMSokla',
#      'http://s.click.aliexpress.com/e/gREJ2ne',
#      'http://s.click.aliexpress.com/e/ckrkSLBE',
#      'http://s.click.aliexpress.com/e/cfu1GiaG',
#      'http://s.click.aliexpress.com/e/ihX7NHW',
#      'http://s.click.aliexpress.com/e/bzHIKg0',
#      'http://s.click.aliexpress.com/e/fYWI86M',
#      'http://s.click.aliexpress.com/e/clYB9Ay0',
#      'http://s.click.aliexpress.com/e/bBuI2d9O',
#      'http://s.click.aliexpress.com/e/FgLs5n2',
#      'http://s.click.aliexpress.com/e/b3Tju7yU'
#      ]
#
#     amazon_urls = [
#     'https://www.amazon.es/gp/product/B014GXQ3JS?psc=1',
#     'https://amzn.to/2ZopoCS',
#     'https://amzn.to/2UJlMZd',
#     'https://amzn.to/2GMRalY',
#     'https://amzn.to/2LaDKEo',
#     'https://amzn.to/2GMRaT0',
#     'https://amzn.to/2GPq65t',
#     'https://amzn.to/2GOLeJb',
#     'https://amzn.to/2GOLlEB',
#     'https://amzn.to/2XUQfpj',
#     'https://amzn.to/2XUT21L',
#     'https://amzn.to/2PxKDOE',
#     'https://amzn.to/2ZEGoFL',
#     'https://amzn.to/2GNn1CO',
#     'https://amzn.to/2GNB5MK',
#     'https://amzn.to/2L8kFTw',
#     'https://amzn.to/2XQmkON',
#     'https://amzn.to/2GOOHr7',
#     'https://amzn.to/2DBgadQ',
#     'https://amzn.to/2GRAE4h',
#     'https://amzn.to/2GQmuQR',
#     'https://amzn.to/2GRg3gp',
#     'https://amzn.to/2DzvMhW',
#     ]
#
#     import random
#
#     urls = ali_urls.extend(amazon_urls)
#     random.shuffle(urls)
#
#     for url in urls:
#         response, status = scrape_url(url)
#         print(status)
#         print(response)
