import requests
import re
from bs4 import BeautifulSoup
import urllib.parse
import json
import sys

ua = json.loads(open("config.json").read())["user_agent"]
def getSchedule(abv, month, day, year, time, amOrpm):#06%3A00%3AAM
    formattedTime = urllib.parse.quote(time + "%3A" + amOrpm)
    print(f"https://www.bart.gov/schedules/stnsched/{abv.upper()}/{month}.{day}.{year}/{formattedTime}")
    r = requests.get(f"https://www.bart.gov/schedules/stnsched/{abv.upper()}/{month}.{day}.{year}/{formattedTime}", headers={"User-agent": ua})
    if r.status_code != 200:
        return json.dumps({"error": True, "message": "BART website returned a non-200 status code. Check back later."})
    
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r.status_code)
    #print(r.text)
    try:
        north_name = south = soup.find_all("div", {"class": "schedule-platform"})[0].find("h5").text
    except:
        return json.dumps({"error": True, "message": "No trains at this time"})
    north = soup.find_all("div", {"class": "schedule-platform"})[0].find_all("li")

    northTrains = []

    if "No trains" not in north[0].text:
        for train in north:
            patern = r'schedule-route-title--([a-zA-Z]+)'
            color = re.search(patern, train.find("span", {"class": "schedule-route-title"}).get("class")[1]).group(1).capitalize()


            line = train.text
            time0 = train.find("span", {"class": "schedule-route-time"}).text
            northTrains.append({"line": color, "terminus": re.sub(r"\n", " ", train.find("span", {"class": "schedule-route-title"}).text), "time": time0})

        south_name = soup.find_all("div", {"class": "schedule-platform"})[1].find("h5").text
        south = soup.find_all("div", {"class": "schedule-platform"})[1].find_all("li")

    southTrains = []

    if type(south) != str:
        for train in south:
            patern = r'schedule-route-title--([a-zA-Z]+)'
            color = re.search(patern, train.find("span", {"class": "schedule-route-title"}).get("class")[1]).group(1).capitalize()


            line = train.text
            time0 = train.find("span", {"class": "schedule-route-time"}).text
            southTrains.append({"line": color, "terminus": re.sub(r"\n", " ", train.find("span", {"class": "schedule-route-title"}).text), "time": time0})
            """
            for x in train.find_all("li"):
                print(x)
                
                
                
            """

    return json.dumps({"error": False, "north": northTrains, "south": southTrains})
#getSchedule("ROCK", "10", "19", "2023", "06:00", "AM")