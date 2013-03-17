# Canary v0.14.1
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
import apikeys

def cors(f):
    """Check CORS and respond to CORS OPTIONS requests."""
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

def apikey(f):
    """Allow a request if it has a valid API key; else, return an error response."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = request.args.get('apikey')
        if request.remote_addr in config['ADDRESSES_IGNORE_API_KEY'] or apikeys.validate(key, request.remote_addr):
            g.validapikey = True
            return f(*args, **kwargs)
        response = jsonify(error="Invalid API key")
        response.status_code = 401
        return response
    return wrapper

def cors_or_apikey(f):
    """Authenticate a request with API keys or CORS as necessary."""
    @cors
    @apikey
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

@app.before_request
def before_cors():
    """Initialize requests to not be authenticated yet."""
    g.corsallowed = False
    g.validapikey = False

@app.after_request
def after_cors(response):
    """Add a CORS allow header as appropriate."""
    if g.corsallowed or (config['ALLOW_CORS_WITH_VALID_API_KEY'] and g.validapikey):
        if 'Origin' in request.headers:
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    return response

@app.before_first_request
def initialize():
    if not os.path.exists(config['STORE_DIR']):
        os.mkdir(config['STORE_DIR'])
    # clear out old lockfiles
    for f in glob.iglob(os.path.join(config['STORE_DIR'], "*.lock")):
        os.remove(f)
    # make db if necessary
    if not os.path.exists(config['DB_DIR']):
        os.mkdir(config['DB_DIR'])
    apikeys.dbsetup()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/s/<server>")
@cors_or_apikey
def server(server):
    try:
        u = urlparse(server)
        data = serverutils.check(u.path)
        return jsonify(**data)
    except Exception as ex:
        return jsonify(error="Problems getting status")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
