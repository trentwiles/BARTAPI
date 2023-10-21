import string
import secrets
import json


def createRequestID():
    characters = string.ascii_letters + string.digits  # You can customize this as needed

    # Use secrets.token_urlsafe() to generate a URL-safe random string
    random_string = ''.join(secrets.choice(characters) for _ in range(16))

    return random_string

def writeToLogsFile(ip, ua, path, timestamp, requestID, error):
    hadError = not error
    logFile = json.loads(open("config.json").read())["logFile"]
    with open(logFile, "a") as l:
        l.write(f"{ip} - {path} @ {timestamp} - had errors: {hadError} - {ua} - {requestID}\n")
    return True