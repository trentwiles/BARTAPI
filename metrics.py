import varnishStat
import bart
import json

def combine():
    # prepares a response for the API
    return json.dumps({"error": False, "varnish": {"space": varnishStat.space(), "stats": varnishStat.cacheMissHit()}, "websiteStatus": bart.getWebsiteStatus()})