from flask import Flask, Response, request
from amazon.scraper import AmazonScraper
from flask_cors import CORS

import json

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)

def is_valid_url(url):
    return True


@xbot_webservice.route("/")
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
        return Response(json.dumps({'Error': 'Parameter url not found'}), status=400, mimetype='application/json')
    if is_valid_url(url):
        try:
            data = AmazonScraper(url).to_dict()
            response = json.dumps(data)
            status = 200
        except:
            response = json.dumps({'Error': f'Cannot scrape this valid url {url} (probably due to a CAPTCHA)'})
            status = 409
    else:
        response = json.dumps({'Error': f'{url} is not valid product URL'})
        status = 412

    return Response(response, status=status, mimetype='application/json')


if __name__ == '__main__':
    xbot_webservice.run(debug=True)
