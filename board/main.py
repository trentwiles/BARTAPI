from flask import Flask, Response, render_template, redirect
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
    count = 0


    for x in range(operations):
        if api[x]['estimates'][0]['time'] == 0:
            html = f"<center><h1>{api[x]['lineTerminus'].upper()}</h1><p>{api[x]['estimates'][0]['formatted'][:-len(' train')].upper()}</p></center>"
            return render_template("board.html", html=html, leaving=True)




    for line in api:
        if count == 2:
            break
        html += f"<p>{line['lineTerminus'].upper()}</p>"

        if len(line["estimates"]) > 1:
            
            html += f"<p>{line['estimates'][0]['formatted'][:-len(' train')].upper()} - {str(line['estimates'][0]['time'])},{str(line['estimates'][1]['time'])}</p>"
        else:
            html += f"<p>{line['estimates'][0]['formatted'][:-len(' train')].upper()} - {str(line['estimates'][0]['time'])}</p>"
        count += 1

    print(html)
    return render_template("board.html", html=html)

@app.route('/s/<station>/time', methods=["GET"])
def stationTime(station):
    return render_template("time.html", station=station)

@app.route('/s/<station>/alerts', methods=["GET"])
def alerts(station):
    return render_template("alerts.html", alerts=requests.get("https://bart.trentwil.es/api/v1/getAlerts").json()["plannedAlerts"], station=station)

if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')