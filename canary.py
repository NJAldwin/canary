from flask import Flask
import fjson
app = fjson.make_json_app(__name__)

DEBUG = True

@app.route("/")
def index():
    return "Index"

if __name__ == "__main__":
    app.run(debug=DEBUG, host='0.0.0.0')
