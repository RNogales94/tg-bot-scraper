from flask import Flask, Response, request
from amazon.scraper import AmazonScraper
from amazon.tools import expand_url
from flask_cors import CORS
from urllib.parse import urlparse

import json

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)


def is_valid_url(url):
    return 'amazon' in urlparse(url).netloc.split('.')


@xbot_webservice.route("/")
def index():
    return 'xbot01'


@xbot_webservice.route("/ping")
def ping():
    return Response(json.dump({'Message': 'Scraper instance'}), status=200, mimetype='application/json')


@xbot_webservice.route("/dev/myip")
def myip():
    return request.remote_addr


@xbot_webservice.route("/api/scrape")
def scrape():
    url = request.args.get('url') or ''

    print(url)
    if url == '':
        print('Parameter url not found: 400 Error')
        return Response(json.dumps({'Error': 'Parameter url not found'}), status=400, mimetype='application/json')

    url = expand_url(url)
    print(f'Expanded: {url}')

    if is_valid_url(url):
        try:
            data = AmazonScraper(url).to_dict()
            response = json.dumps(data)
            print(response)
            status = 200
        except:
            response = json.dumps({'Error': f'Cannot scrape this valid url {url} (probably due to a CAPTCHA)'})
            print(response)
            status = 409
    else:
        response = json.dumps({'Error': f'{url} is not valid Amazon product URL'})
        print(response)
        status = 412

    return Response(response, status=status, mimetype='application/json')


if __name__ == '__main__':
    xbot_webservice.run(debug=True)
