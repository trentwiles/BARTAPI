import requests
from bs4 import BeautifulSoup
import re

def getAlerts():
    r = requests.get("https://www.bart.gov/schedules/advisories")
    soup = BeautifulSoup(r.text, 'html.parser')

    generalAlerts = soup.find("table", {"class": "alerts-table"})
    escAlerts = soup.find("div", {"class": "advisories-table"})

    ga = []
    for x in generalAlerts.find_all("tr"):
        ga.append(x.text.strip())
    
    ea = []
    for x in escAlerts.find_all("tr"):
        # website does this weird thing where it adds random \n characters
        ea.append(re.sub(r'\n', ' ', x.text.strip()))
    
    return {"generalAlerts": ga, "escalatorAlerts": ea}

print(getAlerts())