import requests
import re
from bs4 import BeautifulSoup
import urllib.parse
import json
import sys

def getSchedule(abv, month, day, year, time, amOrpm):#06%3A00%3AAM
    formattedTime = urllib.parse.quote(time + "%3A" + amOrpm)
    print(f"https://www.bart.gov/schedules/stnsched/{abv.upper()}/{month}.{day}.{year}/{formattedTime}")
    r = requests.get(f"https://www.bart.gov/schedules/stnsched/{abv.upper()}/{month}.{day}.{year}/{formattedTime}")
    soup = BeautifulSoup(r.text, 'html.parser')

    north_name = south = soup.find_all("div", {"class": "schedule-platform"})[0].find("h5").text
    north = soup.find_all("div", {"class": "schedule-platform"})[0].find_all("li")


    northTrains = []
    for train in north:
        patern = r'schedule-route-title--([a-zA-Z]+)'
        color = re.search(patern, train.find("span", {"class": "schedule-route-title"}).get("class")[1]).group(1).capitalize()


        line = train.text
        time = train.find("span", {"class": "schedule-route-time"}).text
        northTrains.append({"line": color, "terminus": re.sub(r"\n", " ", train.find("span", {"class": "schedule-route-title"}).text), "time": time})

    south_name = south = soup.find_all("div", {"class": "schedule-platform"})[1].find("h5").text
    south = soup.find_all("div", {"class": "schedule-platform"})[1].find_all("li")

    southTrains = []
    for train in south:
        patern = r'schedule-route-title--([a-zA-Z]+)'
        color = re.search(patern, train.find("span", {"class": "schedule-route-title"}).get("class")[1]).group(1).capitalize()


        line = train.text
        time = train.find("span", {"class": "schedule-route-time"}).text
        southTrains.append({"line": color, "terminus": re.sub(r"\n", " ", train.find("span", {"class": "schedule-route-title"}).text), "time": time})
        """
        for x in train.find_all("li"):
            print(x)
            
            
            
        """

    return json.dumps({"north": northTrains, "south": southTrains})
getSchedule("ROCK", "10", "19", "2023", "06:00", "AM")