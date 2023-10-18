import requests
from bs4 import BeautifulSoup
import re

# Read the bs4 string for the # of cars a train has
# Samples:
# (8 car(Three Door Train)
# (6 car(Three Door Train))
# (6 car)
def processCarString(trainString):
    numberCars = trainString[1:6]
    if "Three Door Train" in trainString:
        return numberCars + "," + "3 door"
    if "Two Door Train" in trainString:
        return numberCars + "," + "2 door"
    return numberCars + ", unknown door"

soup = BeautifulSoup(requests.get("https://www.bart.gov/schedules/eta/MCAR").text, 'html.parser')

lines = ["orange", "yellow", "blue", "red", "green"]
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

print(servedLines)
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



for number in range(len(timings)):
    print(f"=== {servedLines[number]} trains ===")
    for x in range(len(cars[number])):
        print(cars[number][x])

# print(leaveTimesDivs.findAll("span"))
# for x in soup.findAll("div", {"class": "schedule-route schedule-route--style-long"}):
#     soup2 = BeautifulSoup(x.text, 'html.parser')
#     print(x)
#     print("========================")