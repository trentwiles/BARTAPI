from flask import Flask, Response, make_response, render_template, request
import bart
import stations
import alerts
import schedule
import bartLogs
import json
import time

app = Flask(__name__)

def jsonResp(input, status):
    # Helper function to create JSON responses for API methods
    return Response(json.dumps(input), content_type="application/json"), status

def userAgent():
    try:
        return request.headers.get('User-Agent')
    except:
        return ""

@app.route('/')
def home():
    return render_template("index.html")
    #return jsonResp({"error": False, "message": "Check out bart.trentwil.es for documentation"}, 200)

@app.route("/api/v1/getPredictions/<station>")
def getPred(station):
    requestID = bartLogs.createRequestID()
    try:
        bart.getEnglishStationNameFromAbbreviation(station)
        rsp = bart.getDataStation(station)
    except:
        rsp = json.dumps({"error": True, "message": "Invalid station name, use /api/v1/getStations to get the list of BART stations"})
    
    print(rsp)

    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), f"/api/v1/getPredictions/{station}", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getStations")
def getStations():
    requestID = bartLogs.createRequestID()
    rsp = stations.getStations()
    m =  make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), "/api/v1/getStations", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getAlerts")
def getAlerts():
    requestID = bartLogs.createRequestID()
    rsp = alerts.getAlerts()
    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), "/api/v1/getAlerts", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getSchedule/<abv>/<month>/<day>/<year>/<time>/<amPM>")
def getSchedule(abv, month, day, year, time, amPM):
    requestID = bartLogs.createRequestID()
    if bart.getEnglishStationNameFromAbbreviation(abv.upper()) != None:
        rsp = schedule.getSchedule(abv, month, day, year, time, amPM)
    rsp = {"error": True, "message": "Invalid station"}
    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), f"/api/v1/getSchedule/{abv}/{month}/{day}/{year}/{time}/{amPM}", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getStation/<station>")
def getStation(station):
    requestID = bartLogs.createRequestID()
    station = station.upper()
    rsp = stations.getStationsByAbvLive(station)
    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), f"/api/v1/getStation/{station}", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

if __name__ == '__main__':
    app.run()
