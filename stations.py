import bart
import json
import requests
from bs4 import BeautifulSoup
import re

ua = json.loads(open("config.json").read())["user_agent"]

def getStations():
    stationDict = bart.getStationAbbreviations()
    stations = []
    for x in stationDict:
        stations.append({"stationName": x, "stationAbreviation": stationDict[x]})
    return json.dumps({"error": False, "stations": stations})

# New way: scrape from BART website

def getStationsByAbvLive(abv):

    if bart.getEnglishStationNameFromAbbreviation(abv.upper()) == None:
        return json.dumps({"error": True, "message": "Invalid station name"})

    r = requests.get(f"https://www.bart.gov/stations/{abv.lower()}", headers={"User-agent": ua})
    soup = BeautifulSoup(r.text, 'html.parser')

    addy = soup.find("div", {"class": "field field--field-station-address field--address"})
    desc = soup.find("div", {"class": "field field--field-body field--text-long"})
    img = "https://www.bart.gov" + soup.find("div", {"class": "field field--field-station-main-image field--entity-reference"}).find("img").get("src")

    lines = soup.find("div", {"class": "schedule-platform"}).find_all("li")
    servedLines = []
    for line in lines:
        pattern = r'schedule-route-title--([a-zA-Z]+)'
        servedLines.append({"line": re.search(pattern, line.find("span").get("class")[1]).group(1).capitalize(), "name": line.text.strip()})

    address = addy.text.strip()
    description = desc.find_all("p")[0].text.strip()
    map = "https://www.bart.gov" + desc.find_all("a")[1].get("href")

    return json.dumps({"error": False, "address": address, "description": description, "map": map, "image": img, "lines": servedLines})