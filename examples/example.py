import requests

r = requests.get("https://bart.trentwil.es/api/v1/getAlerts")
if not r.json()["error"]:
    
    print("========== Current BART Alerts ==========")
    for x in r.json()["currentAlerts"]:
        print(x)
        print("---------------------------------------------------")

    print("========== Planned Service Alerts ==========")
    for x in r.json()["plannedAlerts"]:
        print(x["message"] + " - Learn more: " + x["url"])
        print("---------------------------------------------------")

r = requests.get("https://bart.trentwil.es/api/v1/getPredictions/FTVL")
if not r.json()["error"]:

    print("========== Trains at Fruitvale Station ==========")
    for lines in r.json()["estimates"]:
        print(lines["lineTerminus"] + "(" + lines["lineColor"] + " Line)")
        print("========================")
        for train in lines["estimates"]:
            print(train["formatted"] + " in " + train["timeFormatted"])