from flask import Flask, Response, make_response, render_template, request
import bart
import stations
import alerts
import schedule
import bartLogs
import json
import time
import metrics
import news

app = Flask(__name__)

def jsonResp(input, status):
    # Helper function to create JSON responses for API methods
    return Response(json.dumps(input), content_type="application/json"), status

def userAgent():
    try:
        return request.headers.get('User-Agent')
    except:
        return ""

def convert_bytes(bytes):
    # Define the denominations and their respective sizes in bytes
    denominations = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    sizes = [1, 1024, 1024**2, 1024**3, 1024**4, 1024**5]

    # Find the appropriate denomination
    for i in range(len(sizes)):
        if bytes < sizes[i] * 1024 or i == len(sizes) - 1:
            return f"{bytes / sizes[i]:.2f} {denominations[i]}"

@app.route('/')
def home():
    return render_template("index.html", varnish=metrics.combine(), convert_bytes=convert_bytes)
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
    try:
        rsp = stations.getStations()
    except:
        rsp = json.dumps({"error": True, "message": "Internal error/BART website error"})
    m =  make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), "/api/v1/getStations", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getAlerts")
def getAlerts():
    requestID = bartLogs.createRequestID()
    try:
        rsp = alerts.getAlerts()
    except:
        rsp = json.dumps({"error": True, "message": "Internal error/BART website error"})
    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), "/api/v1/getAlerts", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getSchedule/<abv>/<month>/<day>/<year>/<tme>/<amPM>")
def getSchedule(abv, month, day, year, tme, amPM):
    requestID = bartLogs.createRequestID()
    if bart.getEnglishStationNameFromAbbreviation(abv.upper()) != None:
        try:
            rsp = schedule.getSchedule(abv, month, day, year, tme, amPM)
        except:
            rsp = json.dumps({"error": True, "message": "Internal error/BART website error"})
    else:
        rsp = json.dumps({"error": True, "message": "Invalid station"})
    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), f"/api/v1/getSchedule/{abv}/{month}/{day}/{year}/{tme}/{amPM}", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getStation/<station>")
def getStation(station):
    requestID = bartLogs.createRequestID()
    station = station.upper()
    try:
        rsp = stations.getStationsByAbvLive(station)
    except:
        rsp = json.dumps({"error": True, "message": "Internal error/BART website error"})
    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), f"/api/v1/getStation/{station}", round(time.time()), requestID, json.loads(rsp)["error"])
    return m

@app.route("/api/v1/getNewsTitles")
def getNT():
    requestID = bartLogs.createRequestID()
    try:
        station = news.getLatestTitles()
    except:
        rsp = json.dumps({"error": True, "message": "Internal error/BART website error"})
    m = make_response(Response(rsp, content_type="application/json"))
    m.headers["x-request-id"] = requestID
    bartLogs.writeToLogsFile(request.headers.get('X-Forwarded-For'), userAgent(), f"/api/v1/getNews", round(time.time()), requestID, json.loads(rsp)["error"])
    return m


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow:", content_type="text/plain")

@app.errorhandler(404)
def page_not_found(error):
    return jsonResp({"error": True, "message": "Route not found"}, 404)

if __name__ == '__main__':
    app.run()
