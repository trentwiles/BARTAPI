import string
import secrets
import json
import time
import shutil


def createRequestID():
    characters = string.ascii_letters + string.digits  # You can customize this as needed

    # Use secrets.token_urlsafe() to generate a URL-safe random string
    random_string = ''.join(secrets.choice(characters) for _ in range(16))

    return random_string

def writeToLogsFile(ip, ua, path, timestamp, requestID, error):
    logFile = json.loads(open("config.json").read())["logFile"]
    with open(logFile, "a") as l:
        l.write(f"{ip[0]} - {path} @ {timestamp} - had errors: {error} - {ua} - {requestID}\n")
    return True

def rotateLogs():
    def get_current_date():
        current_time = time.localtime()
        return {"day": current_time.tm_mday, "month": current_time.tm_mon, "year": current_time.tm_year}
    
    