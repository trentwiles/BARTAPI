import requests
from bs4 import BeautifulSoup
import json

ua = json.loads(open("config.json").read())["user_agent"]

def getPoliceReportsByYear():
    r = requests.get("https://www.bart.gov/about/police/reports", headers={"User-agent": ua})
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Big idea:
    # We need to scrape all of the links between "<h2>Monthly Chief's Report</h2>" and "<h2>Annual Internal Affairs Reports</h2>"
    
    start_element = soup.find("h2", string="Monthly Chief's Report")
    end_element = soup.find("h2", string="Annual Internal Affairs Reports")
    
    html = ""
    if start_element and end_element:
        # Extract content between these two H2 tags
        for element in start_element.find_next_siblings():
            if element == end_element:
                break
            html += str(element)  # Get text only
        
    # now, reparse the stringified html
    newHTML = BeautifulSoup(html, "html.parser")
    allLinks = newHTML.find_all("a")
    allLinksHref = []
    for link in allLinks:
        allLinksHref.append(link.get("href"))
    
    
    return allLinksHref

print(getPoliceReportsByYear())