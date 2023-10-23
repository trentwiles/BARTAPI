import requests
from bs4 import BeautifulSoup
import json



# THIS NEEDS ERROR HANDLING
# Look on the wayback machine to see what the page looks like without any alerts
def getAlerts():
    r = requests.get("https://www.bart.gov/schedules/advisories")
    soup = BeautifulSoup(r.text, 'html.parser')

    current = soup.find_all("div", {"data-service": "current"})
    plannedAlerts = soup.find("table", {"class": "alerts-table"}) # pulls up the first one, which is pla
    escAlerts = soup.find("div", {"data-service": "bart_escalator_service_advisories"})
    elvAlerts = soup.find("div", {"data-service": "bart_elevator_service_advisories"})

    ca = []
    for x in current:
        ca.append(x.find("div", {"class": "alert"}).text.strip())

    pa = []
    for x in plannedAlerts.find_all("tr"):
        # removing the last 11 chars because that's "\nRead More"
        pa.append({"message": x.text.strip()[:-11], "url": "https://www.bart.gov" + x.find("a").get("href")})
    
    ea = []
    for x in escAlerts.find_all("tr"):
        items = x.find_all("td")
        # website does this weird thing where it adds random \n characters
        ea.append({"station": items[0].text, "location": items[1].text, "reason": items[2].text, "returnDate": items[3].text})
    
    ev = []
    for x in elvAlerts.find_all("tr"):
        items = x.find_all("td")
        ev.append({"station": items[0].text, "location": items[1].text, "reason": items[2].text, "returnDate": items[3].text})
        #ev.append(re.sub(r'\n', ' ', x.text.strip()))
    
    return json.dumps({"error": False, "currentAlerts": ca, "plannedAlerts": pa, "escalatorAlerts": ea, "elevatorAlerts": ev})