from flask import Flask, Response
import bart
import stations
import json

app = Flask(__name__)

def jsonResp(input, status):
    # Helper function to create JSON responses for API methods
    return Response(json.dumps(input), content_type="application/json"), status

@app.route('/')
def home():
    return jsonResp({"error": False, "message": "Check out bart.trentwil.es for documentation"})

@app.route("/api/v1/getPredictions/<station>")
def getPred(station):
    try:
        bart.getEnglishStationNameFromAbbreviation(station)
    except:
        return jsonResp({"error": True, "message": "Invalid station name, use /api/v1/getStations to get the list of BART stations"})
    return Response(bart.getDataStation(station), content_type="application/json")

@app.route("/api/v1/getStations")
def getStations():
    return Response(stations.getStations(), content_type="application/json")

if __name__ == '__main__':
    app.run()
