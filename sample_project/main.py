from flask import Flask, Response, render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/s/<station>', methods=["GET"])
def hello_world(station):
    return render_template("index.html")

@app.route('/s/<station>', methods=["POST"])
def api(station):
    r = requests.get(f"https://bart.trentwil.es/api/v1/getPredictions/{station}")
    if r.json()["error"]:
        return Response(json.loads({"error": True}), content_type="application/json")
    return Response(json.loads({"error": False}), content_type="application/json")

if __name__ == '__main__':
    app.run()