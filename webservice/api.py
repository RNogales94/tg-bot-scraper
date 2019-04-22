from flask import Flask, Response, request, render_template
from flask_cors import CORS

import json

xbot_webservice = Flask(__name__, static_url_path="", static_folder="static")
CORS(xbot_webservice)



@xbot_webservice.route("/")
def hello():
    return render_template('index.html')


@xbot_webservice.route("/dev/myip")
def myip():
    return request.remote_addr


@xbot_webservice.route("/api/products")
def get_products():
    skip = int(request.args.get('skip') or 0)
    limit = int(request.args.get('limit') or 0)
    origin = request.args.get('origin')


    js = json.dumps('')
    resp = Response(js, status=200, mimetype='application/json')

    return resp


if __name__ == '__main__':
    xbot_webservice.run(debug=True)
