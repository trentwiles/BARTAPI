from flask import Flask, Response, render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return "hey"

@app.route('/s/<station>', methods=["GET"])
def hello_world(station):
    r = requests.get("https://bart.trentwil.es/api/v1/getPredictions/" + station, headers={"user-agent": "BART Board Project"})
    api = r.json()["estimates"]
    operations = len(api)
    if operations == 0:
        return render_template("board.html", hasTrains=False)
    
    html = ""
    for line in api:
        html += f"<p>{line['lineTerminus'].upper()}</p>"

        if len(line["estimates"]) > 1:
            html += f"<p>{line['estimates']['formatted'][:-len(' train')]} - {str(line['estimates'][0]['time'])},{str(line['estimates'][1]['time'])}</p>"
        else:
            html += f"<p>{line['estimates']['formatted'][:-len(' train')]} - {str(line['estimates'][0]['time'])}</p>"

    print(html)
    return render_template("board.html")

if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')