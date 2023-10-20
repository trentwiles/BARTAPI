from flask import Flask, Response, make_response
import bart
import stations
import alerts
import schedule
import bartLogs
import json

app = Flask(__name__)

def jsonResp(input, status):
    # Helper function to create JSON responses for API methods
    return Response(json.dumps(input), content_type="application/json"), status

@app.route('/')
def home():
    return jsonResp({"error": False, "message": "Check out bart.trentwil.es for documentation"}, 200)

@app.route("/api/v1/getPredictions/<station>")
def getPred(station):
    requestID = bartLogs.createRequestID()
    try:
        bart.getEnglishStationNameFromAbbreviation(station)
    except:
        return jsonResp({"error": True, "message": "Invalid station name, use /api/v1/getStations to get the list of BART stations"})
    
    
    m = make_response(Response(bart.getDataStation(station), content_type="application/json"))
    m.headers["x-request-id"] = requestID
    return m

@app.route("/api/v1/getStations")
def getStations():
    return Response(stations.getStations(), content_type="application/json")

@app.route("/api/v1/getAlerts")
def getAlerts():
    return Response(alerts.getAlerts(), content_type="application/json")

@app.route("/api/v1/getSchedule/<abv>/<month>/<day>/<year>/<time>/<amPM>")
def getSchedule(abv, month, day, year, time, amPM):
    if bart.getEnglishStationNameFromAbbreviation(abv.upper()) != None:
        return Response(schedule.getSchedule(abv, month, day, year, time, amPM), content_type="application/json")
    return jsonResp({"error": True, "message": "Invalid station"}, 400)

if __name__ == '__main__':
    app.run()
