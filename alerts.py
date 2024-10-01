import requests
from bs4 import BeautifulSoup
import json
import bart

ua = json.loads(open("config.json").read())["user_agent"]

def getAlerts():   
    current_alerts = helperCurrentAlerts()
    elevator_alerts = helperElevatorAndEscalatorAlerts("elevator")
    escalator_alerts = helperElevatorAndEscalatorAlerts("escalator")
    
    return json.dumps({"error": False, "currentAlerts": current_alerts, "elevatorAlerts": elevator_alerts, "escalatorAlerts": escalator_alerts})
    

def helperCurrentAlerts():
    r_current = requests.get("https://www.bart.gov/schedules/advisories/current", headers={"User-agent": ua})
    html = r_current.json()["html"]
    soup = BeautifulSoup(html, "html.parser")
    alerts = soup.find("div", {"class": "alerts-body"})
    
    # When there are no alerts, you'll see a message that looks like this:
    # <div class="alert"><span class="alert-inner"><strong>Service Alert</strong>: No advisories issued.</span></div>
    service_alerts = []
    for alert in alerts.find_all("div", {"class": "alert"}):
        service_alerts.append({"message": alert.text.strip()})
    
    return service_alerts

def helperElevatorAndEscalatorAlerts(type):
    # type must be either "elevator" or "escalator"
    r_elevator = requests.get(f"https://www.bart.gov/schedules/advisories_table/bart_{type}_service_advisories", headers={"User-agent": ua})
    html = r_elevator.json()["html"]
    soup = BeautifulSoup(html, "html.parser")
    alerts = soup.find("table", {"class": "alerts-table"})
    alert_holder = []
    for x in alerts.find_all("tr"):
        # <td> - #1 Station name
        # <td> - #2 Location of incident
        # <td> - #3 Type of repair
        # <td> - #4 Date
        
        counter = 1
        data_struct = {
            "station": "",
            "station_full_name": "",
            "location_in_station": "",
            "reason": "",
            "service_return_date": ""
        }
        for dataPoint in x.find_all('td'):
            if counter == 1:
                station_full_name = dataPoint.text
                station_abv = bart.getStationAbbreviationByName(station_full_name)
                    
                data_struct["station"] = station_abv
                data_struct["station_full_name"] = station_full_name
            
            if counter == 2:
                data_struct["location_in_station"] = dataPoint.text
                
            if counter == 3:
                data_struct["reason"] = dataPoint.text
            
            if counter == 4:
                data_struct["service_return_date"] = dataPoint.text
                
            counter += 1
        alert_holder.append(data_struct)
    return alert_holder