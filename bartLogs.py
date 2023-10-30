import string
import secrets
import json
import time
import random


def createRequestID():
    characters = string.ascii_letters + string.digits  # You can customize this as needed

    # Use secrets.token_urlsafe() to generate a URL-safe random string
    random_string = ''.join(secrets.choice(characters) for _ in range(16))

    return random_string

def writeToLogsFile(ip, ua, path, timestamp, requestID, error):
    logFile = json.loads(open("config.json").read())["logFile"]
    with open(logFile, "a") as l:
        try:
            l.write(f"{ip[0]} - {path} @ {timestamp} - had errors: {error} - {ua} - {requestID}\n")
        except:
            l.write(f"UNKNOWN - {path} @ {timestamp} - had errors: {error} - {ua} - {requestID}\n")
    return True

def rotateLogs():
    def get_current_date():
        current_time = time.localtime()
        return current_time.tm_mday, current_time.tm_mon, current_time.tm_year

    
    day, month, year = get_current_date()
    with open(f"archives/{month}-{day}-{year}-" + str(random.randint(0,100000000)) + "-bart.log") as w:
        w.write(open("bart.log").read())
    
    