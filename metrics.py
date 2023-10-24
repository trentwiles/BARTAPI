import varnishStat
import bart

def combine():
    # prepares a response for the API
    return {"error": False, "varnish": {"space": varnishStat.space(), "stats": varnishStat.cacheMissHit()}, "websiteStatus": bart.getWebsiteStatus()}