from flask import Flask, Response, render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return "hey"

@app.route('/s/<station>', methods=["GET"])
def hello_world(station):
    return render_template("index.html")

@app.route('/s/<station>', methods=["POST"])
def api(station):
    r = requests.get(f"https://bart.trentwil.es/api/v1/getPredictions/{station}")
    if not r.json()["error"]:
        return Response(json.dumps({"error": False, "trains": r.json()["estimates"]}), content_type="application/json")
    return Response(json.loads({"error": True, "message": f"Response from bart.trentwil.es: {r.status_code}"}), content_type="application/json")

if __name__ == '__main__':
    app.run()