import varnishStat

# Legacy file for getting metrics from Varnish cache
# As of October 2024, no longer in use

def combine():
    # prepares a response for the API
    return {"error": False, "varnish": {"space": varnishStat.space(), "stats": varnishStat.cacheMissHit()}, "websiteStatus": "none"}