from flask import Flask, jsonify
import fjson
import settings
import serverutils
from urlparse import urlparse

app = fjson.make_json_app(__name__)

@app.route("/")
def index():
    return "Index"

@app.route("/s/<server>")
def server(server):
    try:
        u = urlparse(server)
        data = serverutils.check(u.path)
        return jsonify(**data)
    except Exception as ex:
        return jsonify(error="Problems getting status")

if __name__ == "__main__":
    app.run(debug=settings.DEBUG, host='0.0.0.0')
