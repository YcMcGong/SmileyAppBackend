from flask import Flask
app = Flask(__name__)


@app.route("/")
def healthCheck():
    return "mapService is up and running"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
