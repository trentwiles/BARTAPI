import requests
from bs4 import BeautifulSoup
import re
import json

# Read the bs4 string for the # of cars a train has
# Samples:
# (8 car(Three Door Train)
# (6 car(Three Door Train))
# (6 car)

def getStationAbbreviations():
    # I have about half of them
    return {
        "12th St. Oakland City Center": "12TH",
        "16th St. Mission (SF)": "16TH",
        "19th St. Oakland": "19TH",
        "24th St. Mission (SF)": "24TH",
        "Ashby (Berkeley)": "ASHB",
        "Antioch": "ANTC",
        "Balboa Park (SF)": "BALB",
        "Bay Fair (San Leandro)": "BAYF",
        "Castro Valley": "CAST",
        "Civic Center (SF)": "CIVC",
        "Coliseum": "COLS",
        "Colma": "COLM",
        "Concord": "CONC",
        "Daly City": "DALY",
        "Downtown Berkeley": "DBRK",
        "Dublin/Pleasanton": "DUBL",
        "El Cerrito del Norte": "DELN",
        "El Cerrito Plaza": "PIZA",
        "Embarcadero (SF)": "EMBR",
        "Fremont": "FRMT",
        "Fruitvale (Oakland)": "FTVL",
        "Glen Park (SF)": "GLEN",
        "Hayward": "HAYW",
        "Lafayette": "LAFY",
        "Lake Merritt (Oakland)": "LAKE",
        "MacArthur (Oakland)": "MCAR",
        "Millbrae": "MIBR",
        "Montgomery St. (SF)": "MONT",
        "North Berkeley": "NBRK",
        "North Concord/Martinez": "NCON",
        "Oakland Int'l Airport": "OAKL",
        "Orinda": "ORIN",
        "Pittsburg/Bay Point": "PITT",
        "Pittsburg Center": "PCTR",
        "Pleasant Hill": "PHIL",
        "Powell St. (SF)": "POWL",
        "Richmond": "RICH",
        "Rockridge (Oakland)": "ROCK",
        "San Bruno": "SBRN",
        "San Leandro": "SANL",
        "South San Fransisco": "SSAN",
        "Union City": "UCTY",
        "Warm Springs/South Fremont": "WARM",
        "Walnut Creek": "WCRK",
        "West Dublin": "WDUB",
        "West Oakland": "WOAK"
    }

def getStationAbbreviationByName(name):
    return getStationAbbreviations()[name]

def getEnglishStationNameFromAbbreviation(name):
    list = []
    for x in getStationAbbreviations().items():
        if name == x[1]:
            return x[0]
    return None

def processTimeString(timeString):
    time = 0
    stringNumbers = "0123456789"
    for x in stringNumbers:
        if(timeString[0] == x):
            time = int(timeString[0])
    for x in stringNumbers:
        if(timeString[1] == x):
            time = int(timeString[0:2])  
    # I don't think they have predictions beyond 100 minutes, but it can't hurt
    for x in stringNumbers:
        if(timeString[2] == x):
            time = int(timeString[0:3]) 
    return time

def processCarString(trainString, time):
    numberCars = trainString[1:6]

    formatted = numberCars + ", unknown door train"
    doors = -1
    cars = int(trainString[1:3])
    if "Three Door Train" in trainString:
        formatted = numberCars + ", " + "3 door train"
        doors = 3
    if "Two Door Train" in trainString:
        formatted = numberCars + ", " + "2 door train"
        doors = 2


    return {"formatted": formatted, "doors": doors, "cars": cars, "timeFormatted": time, "time": processTimeString(time)}

def getDataStation(abv):
    r = requests.get(f"https://www.bart.gov/schedules/eta/{abv}")
    soup = BeautifulSoup(r.text, 'html.parser')
    abv = abv.upper()
    if r.status_code != 200:
        return json.dumps({"error": True, "message": "BART website returned a non-200 status code. Check back later."})
    

    lines = ["orange", "yellow", "blue", "red", "green", "white"]
    leaveTimesDivs = soup.findAll("span")
    allLineLeaveTimes = soup.findAll("span", {"class": "schedule-route-stops"})


    servedLines = []
    servedLinesColors = []
    for div in leaveTimesDivs:
        for line in lines:
            if div.get("class") != None:
                if len(div.get("class")) > 1:
                    if line in div.get("class")[1]:
                        pattern = r'schedule-route-title--([a-zA-Z]+)'
                        # Extract the end words from the input strings
                        regex = re.search(pattern, div.get("class")[1])
                        lineColor = regex.group(1)

                        servedLinesColors.append(lineColor.capitalize())
                        servedLines.append(div.text)

    #print(servedLines)
    timings = []
    cars = []
    for div in allLineLeaveTimes:
        timingList = []
        carsList = []

        for times in div.find_all("strong"):
            timingList.append(times.text.strip())

        for car in div.find_all("span", {"class": "schedule-route-cars"}):
            carsList.append(car.text.strip())

        timings.append(timingList)
        cars.append(carsList)


    preFormatedJson = []
    for number in range(len(timings)):
        timingsToInsert = []
        for x in range(len(timings[number])):
            timingsToInsert.append(processCarString(cars[number][x], timings[number][x]))
            
        
        preFormatedJson.append({"lineTerminus": servedLines[number], "lineColor": servedLinesColors[number], "estimates": timingsToInsert})
    #print(preFormatedJson)
    if getEnglishStationNameFromAbbreviation(abv) == None:
        return json.dumps({"error": True, "message": "Invalid station name"})
    return json.dumps({"error": False, "station": getEnglishStationNameFromAbbreviation(abv), "estimates": preFormatedJson})
