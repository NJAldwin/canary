# Canary v0.12.0
# Nick Aldwin
# https://github.com/NJAldwin/canary

from flask import Flask, jsonify, render_template, request, g, make_response
import fjson
from urlparse import urlparse
import glob
import os
from functools import wraps

def make_app(import_name, **kwargs):
    return fjson.make_json_app(import_name, **kwargs)

app = make_app(__name__)
import settings
app.config.from_object(settings)
app.config.from_envvar('CANARY_SETTINGS', silent=True)

config = app.config

__all__ = ['app', 'config']

import serverutils

def cors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        origin = request.headers.get('Origin')
        g.corsallowed = origin in config['CORS_ALLOWED']
        if request.method == 'OPTIONS':
            response = make_response('')
            response.headers['Access-Control-Allow-Origin'] = origin
            return response
        return f(*args, **kwargs)
    return wrapper

@app.before_request
def before_cors():
    g.corsallowed = False

@app.after_request
def after_cors(response):
    if g.corsallowed:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    return response

@app.before_first_request
def initialize():
    if not os.path.exists(config['STORE_DIR']):
        os.mkdir(config['STORE_DIR'])
    # clear out old lockfiles
    for f in glob.iglob(os.path.join(config['STORE_DIR'], "*.lock")):
        os.remove(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/s/<server>")
def server(server):
    try:
        u = urlparse(server)
        data = serverutils.check(u.path)
        return jsonify(**data)
    except Exception as ex:
        return jsonify(error="Problems getting status")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
